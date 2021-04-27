from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy.dialects import mysql
from datetime import datetime


class QuizAnswer(db.Model):
    __tablename__ = "quiz_answers"

    id = db.Column(db.Integer, primary_key=True)
    quiz_question_id = db.Column(
        db.Integer, db.ForeignKey("quiz_questions.id"), nullable=False
    )
    selected_ott = db.Column(db.Integer, nullable=False)
    correct_ott = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<QuizAnswer %r>" % self.id
