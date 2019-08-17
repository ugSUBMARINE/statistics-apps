# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import numpy as np
import scipy.stats

from app import app
from apps.commons import gen_header, common_fig_layout

# global variables
x_max = 6.
n_points = 200
x = np.linspace(-x_max, x_max, n_points)

# components of the app
# header text plus logo
header = gen_header("Cohen's d-value", logo='/assets/icons8-return-96.png', href='/toc')

# Plotly figure
fig_display = dcc.Graph(id='fig-display')

# sliders for delta_mu (difference of means), sigma_1 (std-dev of 1st distribution)
# and sigma_2 (std-dev of 2nd distribution)
sliders = [
    # delta_mu
    html.Div([
        html.Label('set \u0394\u03BC:', className="control_label"),
        dcc.Slider(id='delta-mu',
                   min=0., max=5., step=0.2, value=2.0,
                   marks={i: '{:.1f}'.format(i) for i in range(0, 6)},
                   className='dcc_control')
    ], className='w3-container w3-padding w3-third'),

    # sigma_1
    html.Div([
        html.Label('set \u03C3\u2081:', className="control_label"),
        dcc.Slider(id='sigma-1',
                   min=0.5, max=2.0, step=0.1, value=1.,
                   marks={0.5: '0.5', 1: '1.0', 1.5: '1.5', 2: '2.0'},
                   className='dcc_control')
    ], className='w3-container w3-padding w3-third'),

    # sigma_2
    html.Div([
        html.Label('set \u03C3\u2082:', className="control_label"),
        dcc.Slider(id='sigma-2',
                   min=0.5, max=2.0, step=0.1, value=1.,
                   marks={0.5: '0.5', 1: '1.0', 1.5: '1.5', 2: '2.0'},
                   className='dcc_control')
    ], className='w3-container w3-padding w3-third')
]

layout = html.Div([

    html.Div(header, className='w3-row'),

    html.Div([
        html.Div([
            html.P("""
            Cohen's d-value is a measure of the effect size (e.g. difference between control and treatment group)
            calculated using the difference of means scaled by a pooled standard deviation. Using
            population parameters, it is defined as:
            """),
            html.Img(src='/assets/Cohen_d.svg', style={'display': 'block', 'margin-left': 'auto',
                                                       'margin-right': 'auto', 'width': '67%'}),
            html.P("""
            The d-value is a dimensionless quantity and can be employed across scientific disciplines. It is frequently
            used in estimating necessary sample sizes for statistical testing.
            """),
            html.P("""
            Smaller d-values indicate a stronger overlap of the distributions of measured quantities for the two groups.
            Use the sliders to change the values for \u0394\u03BC, \u03C3\u2081 and \u03C3\u2082.
            """)
        ], className='w3-container w3-col m3 w3-padding'),
        html.Div([
            fig_display,
            html.Div(sliders, className='w3-row')
        ], className='w3-container w3-col m9 w3-padding')
    ], className='w3-row'),

], className='w3-container w3-padding'
)


@app.callback(
    Output('fig-display', 'figure'),
    [Input('delta-mu', 'value'),
     Input('sigma-1', 'value'),
     Input('sigma-2', 'value')]
)
def gen_figure(delta_mu, sigma_1, sigma_2):
    control = go.Scatter(
        x=x,
        y=scipy.stats.norm.pdf(x, scale=sigma_1),
        mode='none',
        fill='tozeroy',
        fillcolor='rgba(152,78,163,0.5)',
        name='control group',
        showlegend=True,
    )

    effect = go.Scatter(
        x=x + delta_mu,
        y=scipy.stats.norm.pdf(x, scale=sigma_2),
        mode='none',
        fill='tozeroy',
        fillcolor='rgba(77,175,74,0.5)',
        name='treatment group',
        showlegend=True,
    )

    data = [control, effect]

    d = delta_mu/np.sqrt((sigma_1**2 + sigma_2**2)/2.)
    fig_title = f"Effect size: d={d:.2f}<br>" + \
                f"(\u0394\u03BC={delta_mu:.1f}, " + \
                f"\u03C3<sub>1</sub>={sigma_1:.1f}, " + \
                f"\u03C3<sub>2</sub>={sigma_2:.1f})"

    fig_layout = {
        'xaxis': {'title': {'text': 'measured quantity'}},
        'yaxis': {'title': {'text': 'pdf'}},
        'legend': {'xanchor': 'right', 'yanchor': 'top', 'x': 1, 'y': 1},
        'title': go.layout.Title(text=fig_title, xref="paper", x=0)
    }
    fig_layout.update(common_fig_layout)

    return go.Figure(data=data, layout=fig_layout)


if __name__ == '__main__':
    app.title = "Cohen's d-value"
    app.layout = layout
    app.run_server(debug=True)
