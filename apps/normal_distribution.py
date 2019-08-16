# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import numpy as np
import scipy.stats

from app import app
from apps.commons import gen_header, pdf_layout, cdf_layout, gen_dist_layout

# global variables
x_max = 5.
n_points = 150
x = np.linspace(-x_max, x_max, n_points)

sigma_min = 5
sigma_max = 30
pdfs = {i: scipy.stats.norm.pdf(x, scale=i/10.) for i in range(sigma_min, sigma_max+1)}
cdfs = {i: scipy.stats.norm.cdf(x, scale=i/10.) for i in range(sigma_min, sigma_max+1)}

pdf_std = go.Scatter(
    x=x,
    y=pdfs[10],  # standard normal distribution, scipy.stats.norm.pdf(x, scale=1.0)
    mode='lines',
    name='std. normal<br>distr.',
    showlegend=True,
    line={'dash': 'dash', 'width': 1.5}
)
cdf_std = go.Scatter(
    x=x,
    y=cdfs[10],  # cdf of standard normal distribution, scipy.stats.norm.cdf(x, scale=1.0)
    mode='lines',
    name='std. normal<br>distr.',
    showlegend=True,
    line={'dash': 'dash', 'width': 1.5}
)

# components of the app
# header text plus logo
header = gen_header('Normal Distribution', logo='/assets/icons8-return-96.png', href='/toc')

# Plotly figures
pdf_display = dcc.Graph(id='normal-pdf-display')
cdf_display = dcc.Graph(id='normal-cdf-display')

# slider to choose sigma plus explanatory text
slider = html.Div([

    html.P("""
    The normal distribution is a symmetric continuous distribution defined by two parameters
    (\u03BC and \u03C3). The mean value \u03BC represents the location of the maximum
    and the standard deviation \u03C3 the width of the distribution. The so called 'standard normal
    distribution' (red dashed line) is a special case with \u03BC=0 and \u03C3=1.
    """),

    html.P('Use the slider to set \u03C3:',
           className="control_label"),

    dcc.Slider(
        id='sigma-slider',
        min=sigma_min, max=sigma_max, step=1,
        marks={i: '{:.1f}'.format(i / 10) for i in range(5, sigma_max+1, 5)},
        value=13,
        className="dcc_control"
    ),

    html.P("""
    Click on the cumulative distribution function (cdf) to get a representation
    of the corresponding area under the probability density function (pdf).
    """),

], className="w3-container w3-col w3-mobile w3-padding", style={'width': '25%'})

layout = gen_dist_layout(header, slider, pdf_display, cdf_display)


@app.callback(
    Output('normal-cdf-display', 'figure'),
    [Input('sigma-slider', 'value')]
)
def create_cdf(sigma):
    cdf_var = go.Scatter(
        x=x,
        y=cdfs[sigma],  # scipy.stats.norm.cdf(x, scale=sigma / 10.),
        mode='lines',
        name='normal distr.<br>(\u03C3={:.1f})'.format(sigma / 10.),
        showlegend=True,
        line={'dash': 'solid', 'width': 3}
    )

    return go.Figure(data=[cdf_std, cdf_var], layout=cdf_layout)


@app.callback(
    Output('normal-pdf-display', 'figure'),
    [Input('sigma-slider', 'value'),
     Input('normal-cdf-display', 'clickData')]
)
def create_pdf(sigma, clickdata):
    pdf_var = go.Scatter(
        x=x,
        y=pdfs[sigma],  # scipy.stats.norm.pdf(x, scale=sigma / 10.),
        mode='lines',
        name='normal distr.<br>(\u03C3={:.1f})'.format(sigma / 10.),
        showlegend=True,
        line={'dash': 'solid', 'width': 3}
    )

    data = [pdf_std, pdf_var]

    if clickdata is not None:
        if clickdata['points'][0]['curveNumber'] == 1:
            index = clickdata['points'][0]['pointIndex']
            xval = clickdata['points'][0]['x']
            data.append(go.Scatter(
                x=x[:index+1],
                y=pdfs[sigma][:index+1],
                mode='none',
                showlegend=False,
                fill='tozeroy',
                hoveron='fills',
                text='area: {:.3f}'.format(scipy.stats.norm.cdf(xval, scale=sigma/10.)),
                hoverinfo='text'
            ))

    return go.Figure(data=data, layout=pdf_layout)


if __name__ == '__main__':
    app.title = "Normal distribution"
    app.layout = layout
    app.run_server(debug=True)
