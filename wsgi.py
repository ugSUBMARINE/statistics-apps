# -*- coding: utf-8 -*-
from index import app

application = app.server

if __name__ == '__main__':
    # application.run(debug=True)
    app.run_server(debug=True)
