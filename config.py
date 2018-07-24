# -*- coding: utf-8 -*-
import os

basedir = os.path.dirname(__file__)


class Config:
    """
    Base configuration
    """
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY',
                                 os.path.join(basedir, 'privkey.pem'))
    PUBLIC_KEY = os.environ.get('PUBLIC_KEY',
                                os.path.join(basedir, 'pubkey.pem'))

    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False

    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """
        Init app

        :param app: Flask app
        :type app: Flask
        """
        with open(app.config['PRIVATE_KEY']) as f:
            app.config['PRIVATE_KEY'] = f.read()

        with open(app.config['PUBLIC_KEY']) as f:
            app.config['PUBLIC_KEY'] = f.read()


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgres://postgres:mysecretpassword@localhost/mosquitto_auth'
    )


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
