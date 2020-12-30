from flask_restx import Namespace, Resource, abort
from flask import jsonify
from flask_app.model.blog import Article, Category, Tag, db
from flask_app.api import create_instances

api = Namespace("Blog", description="Blog apis")


class BlogParser:
    default_parser = api.parser()

    def get(self):
        get_parser = self.default_parser.copy()
        get_parser.add_argument("id", type=int)
        get_parser.add_argument("title")
        get_parser.add_argument("category")
        get_parser.add_argument("tags", action="append")
        return get_parser

    def post(self):
        post_parser = self.get().copy()
        post_parser.add_argument("title", required=True)
        post_parser.add_argument("body", required=True)
        post_parser.replace_argument("category", required=True)
        return post_parser


@api.route("/")
class BlogAPI(Resource):

    parser = BlogParser()

    @api.response(200, "Success")
    @api.expect(parser.get(), validate=False)
    def get(self):

        articles_query = db.session.query(Article)

        articles = articles_query.all()

        rsp = [
            {
                "title": article.title,
                "tags": [{"name": tag.name, "id": tag.id} for tag in article.tags],
                "category": {"name": article.category.name, "id": article.category.id},
            }
            for article in articles
        ]

        return jsonify(rsp)

    @api.response(200, "Success")
    @api.expect(parser.post(), validate=True)
    def post(self):
        args = self.parser.post().parse_args()
        title = args.get("title", None)
        body = args.get("body", None)
        category = args.get("category", None)
        tags = args.get("tags", None)

        tag_objs = Tag.query.filter(Tag.name.in_(tags)).all()

        category_id = Category.query.filter_by(name=category).first().id

        exists = Article.query.filter_by(title=title).scalar() is not None

        if exists:
            raise abort(400, "Title already exists")

        new_article = Article(
            title=title, body=body, category_id=category_id, tags=tag_objs
        )

        create_instances(new_article, "article")

        return jsonify("Succeed")


class TagParser:
    default_parser = api.parser()

    def get(self):
        get_parser = self.default_parser.copy()
        return get_parser

    def post(self):
        post_parser = self.get().copy()
        post_parser.add_argument("name", required=True)
        return post_parser


@api.route("/tag")
class TagAPI(Resource):

    parser = TagParser()

    @api.response(200, "Success")
    @api.expect(parser.get(), validate=False)
    def get(self):
        tags = Tag.query.all()
        rsp = [{"name": tag.name, "id": tag.id} for tag in tags]
        return jsonify(rsp)

    @api.response(200, "Success")
    @api.expect(parser.post(), validate=True)
    def post(self):
        args = self.parser.post().parse_args()
        name = args.get("name", None)

        exists = Tag.query.filter_by(name=name).scalar() is not None

        if exists:
            raise abort(400, "Tag already exists")

        new_tag = Tag(name=name)

        create_instances(new_tag, "tag")

        return jsonify("Succeed")


class CategoryParser:
    default_parser = api.parser()

    def get(self):
        get_parser = self.default_parser.copy()
        return get_parser

    def post(self):
        post_parser = self.get().copy()
        post_parser.add_argument("name", required=True)
        return post_parser


@api.route("/category")
class CategoryAPI(Resource):

    parser = CategoryParser()

    @api.response(200, "Success")
    @api.expect(parser.get(), validate=False)
    def get(self):
        categories = Category.query.all()
        rsp = [{"name": category.name, "id": category.id} for category in categories]
        return jsonify(rsp)

    @api.response(200, "Success")
    @api.expect(parser.post(), validate=True)
    def post(self):
        args = self.parser.post().parse_args()
        name = args.get("name", None)

        exists = Category.query.filter_by(name=name).scalar() is not None

        if exists:
            raise abort(400, "Tag already exists")

        new_category = Category(name=name)

        create_instances(new_category, "category")

        return jsonify("Succeed")
