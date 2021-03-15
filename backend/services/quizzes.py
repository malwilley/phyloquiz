from flask import g
from werkzeug.exceptions import NotFound
from backend.db import get_db


def get_quiz(quiz_uuid):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT DISTINCT q.id, q.uuid, q.ott, q.num_questions, n.name, v.vernacular
        FROM quizzes q
        JOIN ordered_nodes n ON n.ott = q.ott
        LEFT JOIN vernacular_by_ott v ON (q.ott = v.ott and v.lang_primary = 'en' and v.preferred = 1)
        WHERE q.uuid = %(quiz_uuid)s
        """,
        {"quiz_uuid": quiz_uuid},
    )

    quiz_response = cursor.fetchall()

    if not quiz_response:
        raise NotFound()

    quiz = dict(
        zip(
            ["id", "uuid", "ott", "num_questions", "name", "vernacular"],
            quiz_response[0],
        )
    )

    return quiz
