# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go

import numpy as np
import scipy.stats

from app import app
from apps.commons import gen_header

# global variables
x_max = 5.
n_points = 200
x = np.linspace(-x_max, x_max, n_points)
y = scipy.stats.norm.pdf(x)

# components of the app
# header text plus logo
header = gen_header("Diagnostic tests", logo='/assets/icons8-return-96.png', href='/toc')

# Plotly figures
dist_display = dcc.Graph(id='dist-display')

roc_display = dcc.Graph(id='roc-display')

# sliders for 'dist_display'
sliders = [
    # difference
    html.Div([
        html.Label('separation:', className="control_label"),
        dcc.Slider(id='difference',
                   min=0., max=5., step=0.2, value=2.0,
                   className='dcc_control')
    ], className='w3-container w3-padding w3-half'),

    # cutoff
    html.Div([
        html.Label('cutoff value:', className="control_label"),
        dcc.Slider(id='cutoff',
                   min=-4., max=4., step=0.2, value=1.,
                   className='dcc_control')
    ], className='w3-container w3-padding w3-half'),
]

# TODO: add a slider for prior probability (prevalence)
#  show posterior probability for being sick if tested positive
#  show contingency matrix e.g. with 10000 samples

layout = html.Div([

    html.Div(header, className='w3-row'),

    html.Div([
        html.Div([
            dist_display,
            html.Div(sliders, className='w3-row')
        ], className='w3-container w3-col m8 w3-padding'),
        html.Div([
            roc_display,
        ], className='w3-container w3-col m4 w3-padding'),
    ], className='w3-row'),

], className='w3-container w3-padding'
)


@app.callback(
    [Output('cutoff', 'max'),
     Output('cutoff', 'value')],
    [Input('difference', 'value')],
    [State('cutoff', 'value')]
)
def update_slider(diff_value, cutoff_old):
    new_max = 4. + diff_value
    return new_max, min(cutoff_old, new_max)


@app.callback(
    Output('dist-display', 'figure'),
    [Input('difference', 'value'),
     Input('cutoff', 'value')]
)
def gen_dist_figure(diff_value, cutoff_value):

    spec = scipy.stats.norm.cdf(cutoff_value)
    fn = scipy.stats.norm.cdf(cutoff_value, loc=diff_value)
    fp = 1. - spec
    sens = 1. - fn

    healthy = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line={'dash': 'solid', 'width': 3, 'color': '#377eb8'},
        name='healthy',
        showlegend=True,
    )

    sick = go.Scatter(
        x=x + diff_value,
        y=y,
        mode='lines',
        line={'dash': 'solid', 'width': 3, 'color': '#e41a1c'},
        name='sick',
        showlegend=True,
    )

    selected = (x + diff_value) <= cutoff_value
    false_negatives = go.Scatter(
        x=x[selected] + diff_value,
        y=y[selected],
        mode='none',
        fill='tozeroy',
        fillcolor='rgba(228,26,28, 0.3)',
        name='false negatives',
        showlegend=False,
        hoveron='fills',
        text='false negative<br>rate: {:.1f}%'.format(fn * 100.),
        hoverinfo='text'
    )

    selected = x >= cutoff_value
    false_positives = go.Scatter(
        x=x[selected],
        y=y[selected],
        mode='none',
        fill='tozeroy',
        fillcolor='rgba(55, 126, 184, 0.3)',
        name='false positives',
        showlegend=False,
        hoveron='fills',
        text='false positive<br>rate: {:.1f}%'.format(fp * 100.),
        hoverinfo='text'
    )

    data = [false_negatives, false_positives, healthy, sick]

    fig_layout = {
        'xaxis': dict(ticks='', showticklabels=False, title=dict(text='diagnostic marker')),
        'yaxis': dict(ticks='', showticklabels=False),
        'legend': {'xanchor': 'right', 'yanchor': 'top', 'x': 1, 'y': 1},
        'margin': dict(l=25, r=25, t=25, b=50),
        'template': 'ggplot2',
    }

    fig_layout.update({
        'shapes': [
            go.layout.Shape(
                type="line",
                xref="x", yref="paper",
                x0=cutoff_value, x1=cutoff_value,
                y0=0, y1=1,
                line=dict(
                    color="#4daf4a",
                    width=3, dash='dash'
                )),
        ],
        'annotations': [
            go.layout.Annotation(x=0.01, y=0.99, xref="paper", yref="paper", showarrow=False,
                                 text=f"sensitivity: {sens:.3f}<br>" +
                                      f"specificity: {spec:.3f}<br>" +
                                      f"fp-rate: {fp:.3f}<br>" +
                                      f"fn-rate: {fn:.3f}",
                                 font=dict(size=14), xanchor="left", yanchor="top",
                                 align="left", bgcolor='rgba(255, 255, 255, 0.8)', borderpad=3,
                                 )
        ]
    })

    return go.Figure(data=data, layout=fig_layout)


@app.callback(
    Output('roc-display', 'figure'),
    [Input('difference', 'value'),
     Input('cutoff', 'value')]
)
def gen_roc_figure(diff_value, cutoff_value):
    n_roc = int((8 + diff_value)/0.2) + 1  # number of points in the ROC curve
    x_roc = np.linspace(-4., 4.+diff_value, n_roc)

    fp = 1. - scipy.stats.norm.cdf(x_roc)  # false positives
    tp = 1. - scipy.stats.norm.cdf(x_roc, loc=diff_value)  # true positives

    auc = -np.trapz(tp, fp)  # area under the curve

    roc = go.Scatter(
        x=fp,
        y=tp,
        mode='lines',
        line={'dash': 'solid', 'width': 3, 'color': '#984ea3'},
        name='roc',
        showlegend=False,
    )

    cutoff_marker = go.Scatter(
        x=(1. - scipy.stats.norm.cdf(cutoff_value),),
        y=(1. - scipy.stats.norm.cdf(cutoff_value, loc=diff_value),),
        mode='markers',
        marker=dict(
            symbol='circle',
            color='#4daf4a',
            opacity=0.5,
            size=20,
        ),
        showlegend=False,
    )

    data = [roc, cutoff_marker]

    fig_layout = {
        'xaxis': dict(scaleanchor='y', scaleratio=1.,
                      ticktext=["0.0", "", "1.0"],
                      tickvals=[0.0, 0.5, 1.0],
                      title=dict(text='1-specificity<br>(false positive rate)')
                      ),
        'yaxis': dict(ticktext=["0.0", "", "1.0"],
                      tickvals=[0.0, 0.5, 1.0],
                      title=dict(text='sensitivity<br>(true positive rate)')
                      ),
        'margin': dict(l=25, r=25, t=50, b=50),
        'template': 'ggplot2',
        'title': go.layout.Title(text="ROC curve", xref="paper", x=0),
        'annotations': [
            go.layout.Annotation(x=0.75, y=0.25, xref="paper", yref="paper",
                                 text=f"AUC: {auc:.3f}<br>(area under<br>the curve)", showarrow=False,
                                 font=dict(size=14), xanchor="center", yanchor="middle",
                                 align="center", bgcolor='rgba(255, 255, 255, 0.8)', borderpad=3,
                                 )
        ]
    }

    return go.Figure(data=data, layout=fig_layout)


if __name__ == '__main__':
    app.title = "Diagnostic tests"
    app.layout = layout
    app.run_server(debug=True)
