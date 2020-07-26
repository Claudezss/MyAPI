from flask_restx import Model, fields, Namespace

example_response_model = Model(
    "example_response_model",
    {
        "message": fields.String(exapmle="a response example"),
        "results": fields.String(exanple="Success", enum=["Success", "Fail"]),
    },
)


def register_example_response_models(api: Namespace):
    api.add_model("example_response_model", example_response_model)
