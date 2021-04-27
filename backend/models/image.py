from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db


class Image(db.Model):
    __tablename__ = "images_by_ott"

    id = db.Column(db.Integer, primary_key=True)
    ott = db.Column(db.Integer, nullable=False)
    src = db.Column(db.Integer, nullable=False)
    src_id = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Integer)
    best_any = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<Image %r>" % self.id
