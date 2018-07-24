# -*- coding: utf-8 -*-

from flask import request
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.users import user_container_model, user_model, user_post_model
from app.extensions import db
from app.models import User

ns = Namespace('users', description='Users related operations')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API users endpoints
#
# ================================================================================================

@ns.route('/')
class UserCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_container_model)
    def get(self):
        """
        Return users list
        """

        return {'users': User.query.all()}

    @ns.marshal_with(user_model, code=201, description='User successfully added.')
    @ns.doc(response={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(user_post_model)
    def post(self):
        """
        Add user
        """

        data = request.json

        if User.query.filter_by(username=data['username']).first() is not None:
            abort(409, error='Username already exist')

        user = User(
            username=data['username'],
            secret=data['secret']
        )

        db.session.add(user)
        db.session.commit()

        return user, 201


@ns.route('/<int:id>')
@ns.response(404, 'User not found')
class UserItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_model)
    def get(self, id):
        """
        Get user
        """

        user = User.query.get_or_404(id)

        return user

    @ns.response(204, 'User successfully deleted.')
    def delete(self, id):
        """
        Delete user
        """
        user = User.query.get_or_404(id)

        db.session.delete(user)
        db.session.commit()

        return 'User successfully deleted.', 204
