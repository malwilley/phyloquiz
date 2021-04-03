from flask import g
from werkzeug.exceptions import BadRequest, NotFound
from .ordered_leaves import get_species_info
from .generate import generate_quiz_question
from backend.db import get_db


def get_question_species_info(question):
    return {
        "compare": get_species_info(question["compare_ott"]),
        "option1": get_species_info(question["option_1_ott"]),
        "option2": get_species_info(question["option_2_ott"]),
    }


def make_question_record_from_response(question_response):
    return dict(zip(["compare_ott", "option_1_ott", "option_2_ott"], question_response))


def get_completed_questions(quiz_uuid):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT q.compare_ott, q.option_1_ott, q.option_2_ott, a.selected_ott, a.correct_ott
        FROM quizzes
        JOIN quiz_questions q ON q.quiz_id = quizzes.id
        JOIN quiz_answers a ON a.quiz_question_id = q.id
        WHERE quizzes.uuid = %(quiz_uuid)s
        """,
        {"quiz_uuid": quiz_uuid},
    )

    response = cursor.fetchall()

    return [
        {
            **get_question_species_info(make_question_record_from_response(q)),
            "selected": q[3],
            "correct": q[3] == q[4],
        }
        for q in response
    ]


def get_next_question_for_quiz(quiz):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT q.compare_ott, q.option_1_ott, q.option_2_ott, a.id
        FROM quizzes
        JOIN quiz_questions q ON q.quiz_id = quizzes.id
        LEFT JOIN quiz_answers a ON a.quiz_question_id = q.id
        WHERE quizzes.uuid = %(quiz_uuid)s
        ORDER BY q.created_at
        """,
        {"quiz_uuid": quiz["uuid"]},
    )

    questions = [
        dict(zip(["compare_ott", "option_1_ott", "option_2_ott", "answer_id"], q))
        for q in cursor.fetchall()
    ]

    if len(questions) >= quiz["num_questions"]:
        return None

    # Need to generate a question when there aren't any unanswered ones left
    if not questions or questions[-1]["answer_id"]:
        return generate_quiz_question(quiz)

    return {
        "compare": get_species_info(questions[-1]["compare_ott"]),
        "option1": get_species_info(questions[-1]["option_1_ott"]),
        "option2": get_species_info(questions[-1]["option_2_ott"]),
    }


def get_quiz_question_by_number(quiz_uuid, question_number):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT q.id
        FROM quizzes
        JOIN quiz_questions q ON q.quiz_id = quizzes.id
        LEFT JOIN quiz_answers a ON a.quiz_question_id = q.id
        WHERE quizzes.uuid = %(quiz_uuid)s
        ORDER BY q.created_at
        LIMIT 1
        OFFSET %(question_index)s
        """,
        {"quiz_uuid": quiz_uuid, "question_index": question_number - 1},
    )

    response = cursor.fetchall()

    if not response:
        raise NotFound()

    return {"id": response[0][0]}
