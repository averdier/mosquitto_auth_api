import os
import psycopg2
from config import Config
from app import create_app

if __name__ == '__main__':
    con = psycopg2.connect(
        user=os.environ.get('DB_USER', 'postgres'),
        host=os.environ.get('DB_HOST', 'localhost'),
        password=os.environ.get('DB_PASSWORD', 'mysecretpassword')
    )
    con.autocommit = True

    cur = con.cursor()
    cur.execute('CREATE DATABASE {0};'.format(os.environ.get('DB_TABLE', 'mosquitto_auth')))
    cur.close()
    con.close()

    f_app = create_app(os.environ.get('APP_CONFIG', 'default'))
    with f_app.test_request_context():
        from app.models import User, MqttClient, MqttAccess
        from app.extensions import db

        db.create_all()

        if len(User.query.all()) == 0:
            admin = User(username='averdier')
            admin.secret = 'by6WqIAxG3Ah'
            db.session.add(admin)
            db.session.commit()
