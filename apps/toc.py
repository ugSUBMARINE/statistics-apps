# -*- coding: utf-8 -*-
import dash_html_components as html

from app import app

# components of the app
# header text plus logo
header = html.Div([
    html.Div([
        html.H2('Statistics Webapps', style={'margin-left': '16px'})
    ], className='w3-display-left'),

    html.Div([
        html.A(
            html.Img(
                src='/assets/icons8-github-96.png',
                style={'height': '50px',
                       'margin-right': '16px'}
            ),
            href="https://github.com/gammaturn/statistics_apps"
        )
    ], className='w3-display-right')
], className='w3-display-container', style={'height': '60px'})

layout = html.Div([

    html.Div(header, className='w3-row'),

    html.Div([
        html.A(html.H3("Normal Distribution"), href="/normal_distribution"),
        html.A(html.H3("t-Distribution"), href="/t_distribution")
    ], className='w3-container w3-padding'),

], className='w3-container w3-padding'
)


if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
