from flask import Flask, jsonify
from flask_cors import CORS
from flask_app.api import api
from celery import Celery
import os


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
        return jsonify("This is a template of flask-celery-rabittq-flower app")

    app.config["RESTX_MASK_SWAGGER"] = False
    app.config["RESTX_JSON"] = {"ensure_ascii": False}
    api.init_app(app)
    return app
