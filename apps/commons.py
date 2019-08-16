# -*- coding: utf-8 -*-
# common layout functions
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


# common figure layouts
common_fig_layout = {
    'margin': {'t': 80, 'b': 20, 'l': 10, 'r': 10},
    'template': 'ggplot2',
    'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33',
                 '#a65628', '#f781bf', '#999999'],
}

pdf_layout = {
    'xaxis': {'title': {'text': 'random variable'}},
    'yaxis': {'title': {'text': 'pdf'}},
    'legend': {'xanchor': 'right', 'yanchor': 'top', 'x': 1, 'y': 1},
    'title': go.layout.Title(text="Probability density function", xref="paper", x=0)
}
pdf_layout.update(common_fig_layout)

cdf_layout = {
    'xaxis': {'title': {'text': 'random variable'}},
    'yaxis': {'title': {'text': 'cdf'}},
    'legend': {'xanchor': 'right', 'yanchor': 'bottom', 'x': 1, 'y': 0.05},
    'title': go.layout.Title(text="Cumulative distribution function", xref="paper", x=0)
}
cdf_layout.update(common_fig_layout)


def gen_header(title, logo=None, href=None):
    """
    generate the header of the page containing a title and potentially a logo
    """

    left = html.Div([
        html.H2(title, style={'margin-left': '16px'})
    ], className='w3-display-left')

    if logo is not None:
        header = html.Div([
            left,
            html.Div([
                html.A(
                    html.Img(src=logo, style={'height': '24px', 'margin-right': '16px'}),
                    href=href
                )
            ], className='w3-display-right')
        ], className='w3-display-container', style={'height': '60px'})
    else:
        header = html.Div([
            left
            ], className='w3-display-container', style={'height': '60px'})

    return header


def gen_dist_layout(header, slider, pdf_display, cdf_display):
    return html.Div([
        html.Div(header, className='w3-row'),
        html.Div([
            slider,
            html.Div([
                pdf_display
            ], className='w3-container w3-col w3-mobile w3-padding', style={'width': '37.5%'}),
            html.Div([
                cdf_display
            ], className='w3-container w3-col w3-mobile w3-padding', style={'width': '37.5%'})
        ], className='w3-row')
    ], className='w3-container w3-padding')
