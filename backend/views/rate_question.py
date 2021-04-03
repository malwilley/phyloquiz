from flask import g
from werkzeug.exceptions import BadRequest
from nanoid import generate
from backend.db import get_db
from backend.services import quiz_questions


def rate_question(quiz_uuid, question_number, is_good):
    connection = get_db()
    cursor = connection.cursor()

    question = quiz_questions.get_quiz_question_by_number(quiz_uuid, question_number)

    cursor.execute(
        """
        UPDATE quiz_questions
        SET good_question = %(is_good)s
        WHERE id = %(question_id)s
        """,
        {"question_id": question["id"], "is_good": is_good},
    )

    connection.commit()

    return {"is_good": is_good}
