from flask import Flask
from app.celery_utils import init_celery
from app.config import Config
from app.extensions import db, jwt, cache, mail
from seed import seed_dummy_data
from flask_cors import CORS
import os
from apis.auth import auth
from apis.admin_parking import admin_parking_bp
from apis.user_parking import user_parking_bp 

config = Config()


PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

def create_app(app=PKG_NAME, **kwargs):
    app = Flask(app)
    app.config.from_object(config)
    CORS(app, origins="*")
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)
    with app.app_context():
        print(app.config)
        db.create_all()
        seed_dummy_data()
        print("Created DB")
        app.register_blueprint(auth)
        app.register_blueprint(admin_parking_bp)
        app.register_blueprint(user_parking_bp)
        for rule in app.url_map.iter_rules():
            print(rule)

    return app