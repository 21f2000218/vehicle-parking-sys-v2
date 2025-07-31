from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from celery import Celery
from flask_caching import Cache
from flask_mail import Mail

db = SQLAlchemy()
ma = Marshmallow()
pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated="auto")
jwt = JWTManager()
cache = Cache()
mail = Mail()



