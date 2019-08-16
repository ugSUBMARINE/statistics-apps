# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import numpy as np
import scipy.stats

from app import app
from apps.commons import gen_header, pdf_layout, cdf_layout, gen_dist_layout
from apps.normal_distribution import pdf_std, cdf_std

# global variables
x_max = 5.
n_points = 150
x = np.linspace(-x_max, x_max, n_points)

dof_min = 1
dof_max = 16
pdfs = {i: scipy.stats.t.pdf(x, i) for i in range(dof_min, dof_max+1)}
cdfs = {i: scipy.stats.t.cdf(x, i) for i in range(dof_min, dof_max+1)}

# components of the app
# header text plus logo
header = gen_header("Student's t-Distribution", logo='/assets/icons8-return-96.png', href='/toc')

# Plotly figures
pdf_display = dcc.Graph(id='tdist-pdf-display')
cdf_display = dcc.Graph(id='tdist-cdf-display')

# slider to choose sigma plus explanatory text
slider = html.Div([

    html.P("""
    Similar to the normal distribution, the t-distribution is symmetric and bell-shaped, but with heavier tails. It
    is defined by one parameter, the degrees of freedom \u03BD. With larger \u03BD the t-distribution resembles more
    and more a standard normal distribution. It is the central distribution for performing t-tests or estimating
    confidence intervals of sample means. 
    """),

    html.P('Use the slider to set \u03BD:',
           className="control_label"),

    dcc.Slider(
        id='dof-slider',
        min=dof_min, max=dof_max, step=1,
        marks={i: '{:d}'.format(i) for i in range(1, dof_max+1, 5)},
        value=1,
        className="dcc_control"
    ),

    html.P("""
    Click on the cumulative distribution function (cdf) to get a representation
    of the corresponding area under the probability density function (pdf).
    """),

], className="w3-container w3-col w3-mobile w3-padding", style={'width': '25%'})

layout = gen_dist_layout(header, slider, pdf_display, cdf_display)


@app.callback(
    Output('tdist-cdf-display', 'figure'),
    [Input('dof-slider', 'value')]
)
def create_cdf(dof):
    cdf_var = go.Scatter(
        x=x,
        y=cdfs[dof],  # scipy.stats.t.cdf(x, dof),
        mode='lines',
        name='t-distribution<br>(\u03BD={:d})'.format(dof),
        showlegend=True,
        line={'dash': 'solid', 'width': 3}
    )

    return go.Figure(data=[cdf_std, cdf_var], layout=cdf_layout)


@app.callback(
    Output('tdist-pdf-display', 'figure'),
    [Input('dof-slider', 'value'),
     Input('tdist-cdf-display', 'clickData')]
)
def create_pdf(dof, clickdata):
    pdf_var = go.Scatter(
        x=x,
        y=pdfs[dof],  # scipy.stats.t.pdf(x, dof),
        mode='lines',
        name='t-distribution<br>(\u03BD={:d})'.format(dof),
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
                y=pdfs[dof][:index+1],
                mode='none',
                showlegend=False,
                fill='tozeroy',
                hoveron='fills',
                text='area: {:.3f}'.format(scipy.stats.t.cdf(xval, dof)),
                hoverinfo='text'
            ))

    return go.Figure(data=data, layout=pdf_layout)


if __name__ == '__main__':
    app.title = "t-distribution"
    app.layout = layout
    app.run_server(debug=True)
