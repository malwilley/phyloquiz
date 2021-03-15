from flask import g
from werkzeug.exceptions import BadRequest
from random import random
from nanoid import generate
from backend.services.ordered_leaves import get_leaf_info
from backend.db import get_db


def submit_answer(quiz_uuid, selected_ott, question_number):
    connection = get_db()
    cursor = connection.cursor()

    question = get_question(quiz_uuid, question_number)
    leaf_compare = get_leaf_info(question["compare_ott"])
    leaf_1 = get_leaf_info(question["option_1_ott"])
    leaf_2 = get_leaf_info(question["option_2_ott"])

    if (
        selected_ott != question["option_1_ott"]
        and selected_ott != question["option_2_ott"]
    ):
        raise BadRequest("selected_ott does not match one of the options.")

    nearest_common_ancestor_1 = nearest_common_ancestor(
        leaf_compare["id"], leaf_1["id"]
    )
    nearest_common_ancestor_2 = nearest_common_ancestor(
        leaf_compare["id"], leaf_2["id"]
    )

    correct_leaf = (
        leaf_1
        if nearest_common_ancestor_1["id"] > nearest_common_ancestor_2["id"]
        else leaf_2
    )
    correct = correct_leaf["ott"] == selected_ott

    close_ancestors = other_common_ancestors(
        min_node_id=min(
            nearest_common_ancestor_1["id"], nearest_common_ancestor_2["id"]
        ),
        max_node_id=max(
            nearest_common_ancestor_1["id"], nearest_common_ancestor_2["id"]
        ),
        leaf_1_id=correct_leaf["id"],
        leaf_2_id=leaf_compare["id"],
    )

    far_ancestors = other_common_ancestors(
        min_node_id=0,
        max_node_id=min(
            nearest_common_ancestor_1["id"], nearest_common_ancestor_2["id"]
        ),
        leaf_1_id=correct_leaf["id"],
        leaf_2_id=leaf_compare["id"],
    )

    save_answer_to_db(
        question_id=question["id"],
        selected_ott=selected_ott,
        correct_ott=correct_leaf["ott"],
    )

    connection.commit()

    return {
        "correct": correct,
        "leaf_1_ancestor": nearest_common_ancestor_1,
        "leaf_2_ancestor": nearest_common_ancestor_2,
        "close_ancestors": close_ancestors,
        "far_ancestors": far_ancestors,
    }


def get_question(quiz_uuid, question_number):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT q.id, q.compare_ott, q.option_1_ott, q.option_2_ott, a.id
        FROM quizzes
        JOIN quiz_questions q ON q.quiz_id = quizzes.id
        LEFT join quiz_answers a ON q.id = a.quiz_question_id
        WHERE quizzes.uuid = %(quiz_uuid)s
        ORDER BY q.created_at
        """,
        {"quiz_uuid": quiz_uuid, "offset": question_number - 1},
    )

    questions_response = cursor.fetchall()

    question_response = questions_response[question_number - 1]

    if question_response[4] is not None:
        raise BadRequest("Question has already been answered.")

    question = dict(
        zip(["id", "compare_ott", "option_1_ott", "option_2_ott"], question_response)
    )

    return question


def other_common_ancestors(min_node_id, max_node_id, leaf_1_id, leaf_2_id):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT DISTINCT n.id, n.ott, n.age, n.name, v.vernacular
        FROM (
            SELECT n1.id, n1.ott, n1.age, n1.name
            FROM ordered_nodes n1
            JOIN (
              SELECT id, ott, age, name
              FROM ordered_nodes
              WHERE MBRIntersects(Point(0, %(leaf_2_id)s), leaves) AND real_parent >= 0 AND id > %(min_node_id)s AND id <= %(max_node_id)s AND ott IS NOT NULL
            ) n2 ON n1.id = n2.id
            WHERE MBRIntersects(Point(0, %(leaf_1_id)s), leaves) AND real_parent >= 0 AND n1.id > %(min_node_id)s AND n1.id <= %(max_node_id)s AND n1.ott IS NOT NULL
            ORDER BY n1.id DESC
            LIMIT 2
        ) n
        LEFT JOIN vernacular_by_ott v ON v.ott = n.ott AND v.lang_primary = 'en' AND v.preferred
        GROUP BY n.id
        ORDER BY n.id DESC
        """,
        {
            "min_node_id": min_node_id,
            "max_node_id": max_node_id,
            "leaf_1_id": leaf_1_id,
            "leaf_2_id": leaf_2_id,
        },
    )

    response = cursor.fetchall()

    nodes = [
        dict(zip(["id", "ott", "age", "name", "vernacular"], node)) for node in response
    ]

    return nodes


def nearest_common_ancestor(leaf_1_id, leaf_2_id):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT n.id, n.ott, n.age, n.name, v.vernacular
        FROM (
            SELECT distinct n1.id, n1.ott, n1.age, n1.name
            FROM ordered_nodes n1
            JOIN (
              SELECT id, ott, age, name
              FROM ordered_nodes
              WHERE MBRIntersects(Point(0, %(leaf_2_id)s), leaves) AND real_parent >= 0
            ) n2 ON n1.id = n2.id
            WHERE MBRIntersects(Point(0, %(leaf_1_id)s), leaves) AND real_parent >= 0
            ORDER BY id DESC
            LIMIT 1
        ) n
        LEFT JOIN vernacular_by_ott v ON v.ott = n.ott AND v.lang_primary = 'en' AND v.preferred
        """,
        {"leaf_1_id": leaf_1_id, "leaf_2_id": leaf_2_id},
    )
    response = cursor.fetchall()

    if not response:
        return None

    ancestor_node = dict(zip(["id", "ott", "age", "name", "vernacular"], response[0]))

    return ancestor_node


def save_answer_to_db(question_id, selected_ott, correct_ott):
    cursor = get_db().cursor()

    cursor.execute(
        """
        INSERT INTO quiz_answers (quiz_question_id, selected_ott, correct_ott)
        VALUES (%(quiz_question_id)s, %(selected_ott)s, %(correct_ott)s)
        """,
        {
            "quiz_question_id": question_id,
            "selected_ott": selected_ott,
            "correct_ott": correct_ott,
        },
    )
