from flask_restx import Api
from .example import api as example_api_ns


api = Api(title="Example API Docs", version="1.0", doc="/doc/", ordered=True)

# add namespace to api
api.add_namespace(example_api_ns, path="/example")
