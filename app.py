# -*- coding: utf-8 -*-
import dash

external_stylesheets = ['https://www.w3schools.com/w3css/4/w3.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[
                    {
                        'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'
                    }
                ]
                )

app.title = "Biostatistics"
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

