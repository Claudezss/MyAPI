from flask import Flask, jsonify
from flask_cors import CORS
from flask_app.model.db import main_db
from celery import Celery
import os
from flask_app.api.register import register_apis

USER = os.environ.get("USER", "postgres")
PASS = os.environ.get("PASS", "1234")
IP = os.environ.get("IP", "0.0.0.0")
PORT = os.environ.get("PORT", "5432")
DB = os.environ.get("DB", "postgres")

CONFIG = f"postgresql://postgres:{PASS}@{IP}:{PORT}/{DB}"


def create_celery(app=None):
    app = app or create_app()
    celery = Celery(
        app.import_name, backend="amqp", broker=os.environ["CELERY_BROKER_URL"]
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def home():
        return jsonify("Claude Zhang's APIs")

    app.config["RESTX_MASK_SWAGGER"] = False
    app.config["RESTX_JSON"] = {"ensure_ascii": False}
    if os.environ.get("ENV", "") == "TEST":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = CONFIG
    main_db.init_app(app)
    app = register_apis(app)
    with app.app_context():
        main_db.create_all()
    return app
