# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import (toc, normal_distribution, t_distribution, cohen_d, diagnostic_tests)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/toc':
        return toc.layout
    elif pathname == '/normal_distribution':
        return normal_distribution.layout
    elif pathname == '/t_distribution':
        return t_distribution.layout
    elif pathname == '/cohen_d':
        return cohen_d.layout
    elif pathname == '/diagnostic_tests':
        return diagnostic_tests.layout
    else:
        return "404"


if __name__ == '__main__':
    app.run_server(debug=True)
