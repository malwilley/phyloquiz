from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db


class Iucn(db.Model):
    __tablename__ = "iucn"

    id = db.Column(db.Integer, primary_key=True)
    ott = db.Column(db.Integer, nullable=False)
    iucn = db.Column(db.Integer)
    status_code = db.Column(db.String(10))

    def __repr__(self):
        return "<IUCN %r>" % self.status_code
