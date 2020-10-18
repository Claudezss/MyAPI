from flask_restx import Namespace, Resource, abort
from flask import jsonify, render_template_string
from flask_app.model.secret import Slink, db

api = Namespace("Secret", description="private apis")


class SlinkParser:
    default_parser = api.parser()

    def __init__(self):
        self.default_parser.add_argument("code", required=True)

    def get(self):
        get_parser = self.default_parser.copy()
        get_parser.add_argument("id")
        get_parser.add_argument("name")
        get_parser.add_argument("html")
        return get_parser

    def post(self):
        post_parser = self.get().copy()
        post_parser.add_argument("link", required=True)
        post_parser.replace_argument("name", required=True)
        return post_parser


@api.route("/slink")
class SlinkAPI(Resource):

    parser = SlinkParser()

    @api.response(200, "Success")
    @api.expect(parser.get(), validate=False)
    def get(self):
        args = self.parser.get().parse_args()
        slinks = Slink.query.all()

        if not args.get("code", None):
            raise abort(400, "Could not find access code")

        if args.get("id", None):
            slinks.filter(id=args["id"])
        if args.get("name", None):
            slinks.filter(name=args["name"])

        rsp = [{"name": slink.name, "link": slink.link} for slink in slinks]

        if args.get("html", None):
            html = ""
            for slink in slinks:
                html += f"<a href='{slink.link}' target='_blank'>{slink.name}</a>"
            return render_template_string(html)

        return jsonify(rsp)

    @api.response(200, "Success")
    @api.expect(parser.post(), validate=False)
    def post(self):
        args = self.parser.post().parse_args()
        link = args.get("link", None)
        name = args.get("name", None)

        if not name or not link:
            return jsonify("Need name and link")

        exists = Slink.query.filter_by(link=link).scalar() is not None

        if exists:
            raise abort(400, "Link already exists")

        new_slink = Slink(name=name, link=link)

        try:
            db.session.add(new_slink)
            db.session.commit()
        except Exception:
            return jsonify("Failed to save link")

        return jsonify("Succeed")
