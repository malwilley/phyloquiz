from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy.dialects import mysql


class Leaf(db.Model):
    __tablename__ = "ordered_leaves"

    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer, nullable=False)
    real_parent = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(190))
    extinction_date = db.Column(db.Float)
    ott = db.Column(db.Integer)
    wikidata = db.Column(db.Integer)
    wikipedia_lang_flag = db.Column(db.Integer)
    eol = db.Column(db.Integer)
    iucn = db.Column(mysql.LONGTEXT)
    raw_popularity = db.Column(db.Float)
    popularity = db.Column(db.Float)
    popularity_rank = db.Column(db.Integer)
    ncbi = db.Column(db.Integer)
    ifung = db.Column(db.Integer)
    worms = db.Column(db.Integer)
    gbif = db.Column(db.Integer)
    ipni = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __repr__(self):
        return "<Leaf %r>" % self.name
