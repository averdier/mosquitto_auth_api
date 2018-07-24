# -*- coding: utf-8 -*-

import jwt
from flask import Blueprint, current_app, g
from flask_restplus import Api
from flask_httpauth import HTTPTokenAuth
from app.models import User

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='Mosquitto Auth service',
          version='0.1',
          description='Python auth micro service',
          doc='/',
          authorizations={
              'tokenKey': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization'
              }
          },
          security='tokenKey'
          )

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    """
    Verify authorization token

    :param token: Token
    :type token: str

    :return: True if valid token, else False
    :rtype: bool
    """
    try:
        response = jwt.decode(
            token,
            current_app.config['PUBLIC_KEY'],
            audience=''
        )
        u = User.query.get(int(response['user']['id']))

        if u:
            g.user = u
            g.user_token = token
            return True

        return False

    except Exception as ex:
        current_app.logger.warning('Unable to verify token [{0}], reason : {1}'.format(
            token, ex
        ))

        return False


from .endpoints.clients import ns as client_namespace
from .endpoints.access import ns as access_namespace
from .endpoints.auth import ns as auth_namespace

api.add_namespace(auth_namespace)
api.add_namespace(client_namespace)
api.add_namespace(access_namespace)
