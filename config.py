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

    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mysecretpassword')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_TABLE = os.environ.get('DB_TABLE', 'mosquitto_auth')

    SQLALCHEMY_DATABASE_URI = 'postgres://{0}:{1}@{2}/{3}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_TABLE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_PATH = os.environ.get('LOG_PATH', os.path.join(basedir, 'mosquitto_auth_service.log'))

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

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        import logging
        from logging.handlers import RotatingFileHandler

        handler_debug = logging.handlers.RotatingFileHandler(app.config['LOG_PATH'], mode="a", maxBytes=5000000,
                                                             backupCount=1, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
        handler_debug.setFormatter(formatter)

        app.logger.addHandler(handler_debug)
        app.logger.setLevel(logging.DEBUG)


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
