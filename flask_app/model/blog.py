from flask_app.model.db import main_db as db
import datetime

tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
)


class Article(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)

    body = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    tags = db.relationship(
        "Tag",
        secondary=tags,
        lazy="subquery",
        backref=db.backref("articles", lazy=True),
    )

    created_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )


class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    articles = db.relationship("Article", backref="category")

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
