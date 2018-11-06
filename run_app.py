# -*- coding: utf-8 -*-

import os
from app import create_app


app = create_app(os.environ.get('APP_CONFIG', 'default'))


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5552'))
    except ValueError:
        PORT = 5552

    app.run(HOST, PORT, debug=True) # On Windows
    #app.run(HOST, PORT, debug=True, processes=3) # On Linux
    #app.run('0.0.0.0', 8000, processes=3) # On docker