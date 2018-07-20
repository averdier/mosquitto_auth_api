# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='Mosquitto Auth service',
          version='0.1',
          description='Python auth micro service',
          doc='/'
          )

from .endpoints.clients import ns as client_namespace
from .endpoints.access import ns as accesses_namespace

api.add_namespace(client_namespace)
api.add_namespace(accesses_namespace)
