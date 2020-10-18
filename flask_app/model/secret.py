from flask_app.model.db import main_db as db
import datetime


class SecretCode(db.Model):

    __tablename__ = "secret_code"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(125))

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Slink(db.Model):

    __tablename__ = "secret_link"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255))

    link = db.Column(db.String(255))

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
