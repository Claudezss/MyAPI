from flask_app.model.blog import db
from flask import jsonify


def create_instances(instances: list or object, model_type: str):
    try:
        if isinstance(instances, list):
            db.session.add_all(instances)
        else:
            db.session.add(instances)
        db.session.commit()

    except Exception:
        return jsonify(f"Failed to create new {model_type}")
