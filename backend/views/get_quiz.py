from flask import g
from werkzeug.exceptions import BadRequest
from backend.services import quizzes, quiz_questions
from backend.db import get_db


def get_quiz(quiz_uuid):
    quiz = quizzes.get_quiz(quiz_uuid)

    quiz_data = {
        "quiz": {
            "uuid": quiz["uuid"],
            "num_questions": quiz["num_questions"],
            "name": quiz["name"],
            "vernacular": quiz["vernacular"],
            "ott": quiz["ott"],
        },
        "next_question": quiz_questions.get_next_question_for_quiz(quiz),
        "completed_questions": quiz_questions.get_completed_questions(quiz_uuid),
    }

    get_db().commit()

    return quiz_data
