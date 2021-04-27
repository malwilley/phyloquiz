from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy.dialects import mysql


class Vernacular(db.Model):
    __tablename__ = "vernacular_by_ott"

    id = db.Column(db.Integer, primary_key=True)
    ott = db.Column(db.Integer, nullable=False)
    vernacular = db.Column(db.String(190))
    lang_primary = db.Column(db.String(3), nullable=False)
    lang_full = db.Column(db.String(20), nullable=False)
    preferred = db.Column(db.Boolean, nullable=False)
    src = db.Column(db.Integer, nullable=False)
    src_id = db.Column(db.Integer, nullable=True)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return "<Vernacular %r>" % self.vernacular
