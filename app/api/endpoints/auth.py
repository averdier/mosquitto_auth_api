# -*- coding: utf-8 -*-

import time
import jwt
from flask import g, request, current_app
from flask_restplus import Namespace, Resource, abort, marshal
from .. import auth
from ..serializers.auth import user_model, token_encoded_model, token_unencoded_model
from ..parsers import auth_parser
from app.models import User


ns = Namespace('auth', description='Auth related operations.')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API Auth endpoints
#
# ================================================================================================


def is_authorized_client(username, secret):
    """
    Verify if is authorized client

    :param username:
    :param secret:
    :return:
    """
    u = User.query.filter_by(username=username).first()

    if u is None:
        return False

    if u.check_secret(secret):
        g.client = u
        return True

    return False


@ns.route('/token')
class TokenResource(Resource):

    @ns.marshal_with(token_unencoded_model)
    @auth.login_required
    def get(self):
        """
        Get unencoded token
        """
        try:
            return jwt.decode(g.user_token, current_app.config['PUBLIC_KEY'], audience='')

        except Exception as ex:
            abort(400, 'Invalid token')

    @ns.marshal_with(token_encoded_model)
    @ns.expect(auth_parser)
    def post(self):
        """
        Get token
        """
        data = request.form

        audience = ''

        if not is_authorized_client(data['username'], data['secret']):
            abort(401, error='Unauthorized')

        now = int(time.time())

        token = {
            'iss': 'https://localhost/public/auth',
            'aud': audience,
            'iat': now,
            'exp': now + 3600 * 24,
            'user': marshal(g.client, user_model)
        }

        token = jwt.encode(token, current_app.config['PRIVATE_KEY'], algorithm='RS512')

        return {'token': token.decode('utf-8')}