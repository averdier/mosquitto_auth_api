# -*- coding: utf-8 -*-

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app
from app.extensions import db
from .utils import hash_sha256
from plugins.hashing_passwords import make_hash


class User(db.Model):
    """
    Represent user of API
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(128))

    def hash_password(self, password):
        """
        Set new user passsword

        :param password: New password to hash
        :type password: str
        """
        self.password = hash_sha256(password)

    def verify_password(self, password, verify_hash=True):
        """
        Verify if password is user password

        :param password: Password to test
        :type password: str
        :param verify_hash: Verify hash of password or not (default True)
        :type verify_hash: bool

        :return: True if is user password, False else
        :rtype: bool
        """

        if verify_hash:
            return self.password == hash_sha256(password)
        else:
            return self.password == password

    def generate_auth_token(self, expiration=None):
        """
        Generate token for user authentification

        :param expiration: Auth expiration
        :type expiration: int

        :return: Auth token
        :rtype: str
        """

        if expiration is None:
            expiration = current_app.config['TOKEN_EXPIRATION_TIME']

        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        Return user form token

        :param token: Token
        :type token: str

        :return: User if valid token, else None
        :rtype: User|None
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = serializer.loads(token)
        except SignatureExpired:
            print('SignatureExpired')
            return None
        except BadSignature:
            print('BadSignature')
            return None

        user = User.query.get(data['id'])

        return user


class MqttClient(db.Model):
    """
    Represent MQTT client
    """
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    access = db.relationship('MqttAccess', lazy='dynamic',
                             backref=db.backref('clients', lazy=True))

    def hash_password(self, password):
        """
        Set new client password

        :param password:
        :return:
        """
        self.password = make_hash(password)


class MqttAccess(db.Model):
    """
    Represent MQTT access
    """
    __tablename__ = 'access'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    topic = db.Column(db.String(256), nullable=False)
    access = db.Column(db.Integer, nullable=False, default=1)
    username = db.Column(db.String(32), db.ForeignKey('clients.username'))
