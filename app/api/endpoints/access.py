# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.access import access_post_model, access_container_model, access_model, access_patch_model
from app.extensions import db
from app.models import MqttAccess, MqttClient

ns = Namespace('access', description='accesses related operations')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API accesses endpoints
#
# ================================================================================================

@ns.route('/')
class AccessCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(access_container_model)
    def get(self):
        """
        Return list of mqtt access
        """
        return {'accesses': MqttAccess.query.all()}

    @ns.marshal_with(access_model, code=201, description='Access successfully added.')
    @ns.doc(response={
        404: 'Client not found'
    })
    @ns.expect(access_post_model)
    def post(self):
        """
        Add mqtt access to user
        """
        data = request.json

        client = MqttClient.query.filter_by(username=data['username']).first()
        if client is None:
            abort(404, error='Client not found')

        access = MqttAccess()
        access.username = data['username']
        access.topic = data['topic']
        access.access = data['access']

        db.session.add(access)
        db.session.commit()

        return access, 201


@ns.route('/<int:id>')
@ns.response(404, 'Access not found')
class AccessItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(access_model)
    def get(self, id):
        """
        Get mqtt access
        """
        access = MqttAccess.query.get_or_404(id)

        return access

    @ns.response(204, 'Access successfully patched.')
    @ns.expect(access_patch_model)
    def patch(self, id):
        """
        Patch mqtt access
        """
        access = MqttAccess.query.get_or_404(id)

        data = request.json

        patched = False
        if data.get('topic', None) is not None:
            access.topic = data['topic']
            patched = True

        if data.get('access', None) is not None:
            access.access = data['access']
            patched = True

        if patched:
            db.session.add(access)
            db.session.commit()

        return 'Access successfully patched.', 204

    @ns.response(204, 'Access successfully deleted.')
    def delete(self, id):
        """
        Delete mqtt access
        """

        access = MqttAccess.query.get_or_404(id)

        db.session.delete(access)
        db.session.commit()

        return 'Access successfully deleted.', 204
