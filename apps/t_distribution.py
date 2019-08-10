# -*- coding: utf-8 -*-
# import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import numpy as np
import scipy.stats

from app import app

# global variables
x_max = 5.
n_points = 150
x = np.linspace(-x_max, x_max, n_points)

dof_min = 1
dof_max = 16
pdfs = {i: scipy.stats.t.pdf(x, i) for i in range(dof_min, dof_max+1)}
cdfs = {i: scipy.stats.t.cdf(x, i) for i in range(dof_min, dof_max+1)}

pdf_std = go.Scatter(
    x=x,
    y=scipy.stats.norm.pdf(x, scale=1.0),  # standard normal distribution
    mode='lines',
    name='std. normal<br>distr.',
    showlegend=True,
    line={'dash': 'dash', 'width': 1.5}
)
cdf_std = go.Scatter(
    x=x,
    y=scipy.stats.norm.cdf(x, scale=1.0),  # cdf of standard normal distribution
    mode='lines',
    name='std. normal<br>distr.',
    showlegend=True,
    line={'dash': 'dash', 'width': 1.5}
)

# components of the app
# header text plus logo
header = html.Div([
    html.Div([
        html.H2("Student's t-Distribution", style={'margin-left': '16px'})
    ], className='w3-display-left'),

    html.Div([
        html.A(
            html.Img(
                src='/assets/gammaturn.png',
                style={'height': '50px',
                       'margin-right': '16px'}
            ),
            href="/toc"
        )
    ], className='w3-display-right')
], className='w3-display-container', style={'height': '60px'})

# Plotly figures
pdf_display = dcc.Graph(id='tdist-pdf-display')
cdf_display = dcc.Graph(id='tdist-cdf-display')

# slider to choose sigma plus explanatory text
slider = html.Div([

    html.P("""
    The normal distribution is a symmetric continuous distribution and is defined by two parameters
    (\u03BC and \u03C3). The mean value \u03BC represents the location of the maximum
    and the standard deviation \u03C3 the width of the distribution. The so called 'standard normal
    distribution' (red dashed line) is a special case with \u03BC=0 and \u03C3=1.
    """),

    html.P('Use the slider to set the degrees of freedom:',
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

layout = html.Div([

    html.Div(header, className='w3-row'),

    html.Div([
        slider,
        html.Div([
            pdf_display
        ], className='w3-container w3-col w3-mobile w3-padding', style={'width': '37.5%'}),
        html.Div([
            cdf_display
        ], className='w3-container w3-col w3-mobile w3-padding', style={'width': '37.5%'})
    ], className='w3-row'),

], className='w3-container w3-padding'
)


@app.callback(
    Output('tdist-cdf-display', 'figure'),
    [Input('dof-slider', 'value')]
)
def create_cdf(dof):
    cdf_var = go.Scatter(
        x=x,
        y=cdfs[dof],  # scipy.stats.t.cdf(x, dof),
        mode='lines',
        name='t-distribution<br>(dof={:d})'.format(dof),
        showlegend=True,
        line={'dash': 'solid', 'width': 3}
    )

    return go.Figure(data=[cdf_std, cdf_var],
                     layout={
                         'xaxis': {'title': {'text': 'random variable'}},
                         'yaxis': {'title': {'text': 'cdf'}},
                         'margin': {'t': 60, 'b': 20, 'l': 10, 'r': 10},
                         'template': 'ggplot2',
                         'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                                      '#ff7f00', '#ffff33', '#a65628', '#f781bf',
                                      '#999999'],
                         'legend': {'xanchor': 'right', 'yanchor': 'bottom', 'x': 1, 'y': 0.05},
                         'title': go.layout.Title(text="Cumulative distribution function", xref="paper", x=0)
                     })


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
        name='t-distribution<br>(dof={:d})'.format(dof),
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

    return go.Figure(data=data,
                     layout={
                         'xaxis': {'title': {'text': 'random variable'}},
                         'yaxis': {'title': {'text': 'pdf'}},
                         'margin': {'t': 60, 'b': 20, 'l': 10, 'r': 10},
                         'template': 'ggplot2',
                         'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                                      '#ff7f00', '#ffff33', '#a65628', '#f781bf',
                                      '#999999'],
                         'legend': {'xanchor': 'right', 'yanchor': 'top', 'x': 1, 'y': 1},
                         'title': go.layout.Title(text="Probability density function", xref="paper", x=0)
                     })


if __name__ == '__main__':
    app.title = "t-distribution"
    app.layout = layout
    app.run_server(debug=True)
