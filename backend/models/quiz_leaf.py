from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy.dialects import mysql
from datetime import datetime


# Subset of ordered_leaves which only includes leaves that are valid for use in quizzes.
class QuizLeaf(db.Model):
    __tablename__ = "quiz_leaves_by_ott"

    id = db.Column(db.Integer, primary_key=True)
    ott = db.Column(db.Integer, db.ForeignKey("ordered_leaves.ott"), nullable=False)
    depth = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<QuizLeaf %r>" % self.ott
