from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy.dialects import mysql
from datetime import datetime


class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    compare_ott = db.Column(db.Integer, nullable=False)
    option_1_ott = db.Column(db.Integer, nullable=False)
    option_2_ott = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    good_question = db.Column(db.Boolean)

    def __repr__(self):
        return "<QuizQuestion %r>" % self.id
