from flask_restx import Namespace, Resource
from flask_app.schema.response.example import register_example_response_models

api = Namespace("Example", description="an example of api doc")

register_example_response_models(api)


@api.route("")
class Example(Resource):
    @api.response(200, "Success", api.models["example_response_model"])
    @api.marshal_with(api.models["example_response_model"], skip_none=True)
    def get(self):
        rsp = {"message": "Api message for GET", "results": "Success"}
        return rsp

    @api.response(200, "Success", api.models["example_response_model"])
    @api.marshal_with(api.models["example_response_model"], skip_none=True)
    def patch(self):
        rsp = {"message": "Api message for Patch", "results": "Success"}
        return rsp

    @api.response(200, "Success", api.models["example_response_model"])
    @api.marshal_with(api.models["example_response_model"], skip_none=True)
    def delete(self):
        rsp = {"message": "Api message for Delete", "results": "Success"}
        return rsp

    @api.response(200, "Success", api.models["example_response_model"])
    @api.marshal_with(api.models["example_response_model"], skip_none=True)
    def post(self):
        rsp = {"message": "Api message for Post", "results": "Success"}
        return rsp
