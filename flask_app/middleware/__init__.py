from werkzeug.wrappers import Request, Response
import os


class Middleware:
    def __init__(self, app):
        self.app = app
        self.userName = "Tony"
        self.password = "IamIronMan"

    def __call__(self, environ, start_response):
        request = Request(environ)
        code_in_header = request.headers.get("Secret-Code", None)
        code_in_args = request.args.get("code", None)
        path = request.path
        secret_code = os.environ.get("SECRET_CODE", "")

        if "/sc" in path:
            if code_in_header and code_in_header == secret_code:
                pass
            elif code_in_args and code_in_args == secret_code:
                pass
            else:
                res = Response(
                    u"Authorization failed, Need Token to Access Private APIs",
                    mimetype="text/plain",
                    status=401,
                )

                return res(environ, start_response)

        return self.app(environ, start_response)
