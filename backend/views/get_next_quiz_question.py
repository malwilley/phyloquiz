from flask import g, jsonify
from werkzeug.exceptions import BadRequest
from backend.services.quiz_questions import get_next_question_for_quiz
from backend.db import get_db
from backend.services import quizzes


def get_next_question_for_quiz_uuid(quiz_uuid):
    quiz = quizzes.get_quiz(quiz_uuid)

    question = get_next_question_for_quiz(quiz)

    get_db().commit()

    return jsonify(question)
