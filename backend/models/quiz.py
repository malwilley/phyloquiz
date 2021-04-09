from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import text
from datetime import datetime
from sqlalchemy.dialects import mysql


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.CHAR(8), nullable=False, unique=True)
    ott = db.Column(db.Integer, nullable=False)
    num_questions = db.Column(db.Integer, nullable=False, default=5)
    session_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Quiz %r>" % self.uuid
