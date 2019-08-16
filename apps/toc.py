# -*- coding: utf-8 -*-
import dash_html_components as html

from app import app
from apps.commons import gen_header

# components of the app
# header text plus logo
header = gen_header('Statistics Webapps', logo='/assets/icons8-github-96.png',
                    href='https://github.com/gammaturn/statistics_apps')

layout = html.Div([

    html.Div(header, className='w3-row'),

    html.Div([
        html.A(html.H3("Normal Distribution"), href="/normal_distribution"),
        html.A(html.H3("t-Distribution"), href="/t_distribution"),
        html.A(html.H3("Cohen's d-value"), href="/cohen_d")
    ], className='w3-container w3-padding'),

], className='w3-container w3-padding'
)


if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
