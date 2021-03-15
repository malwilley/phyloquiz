from flask import g
from werkzeug.exceptions import BadRequest
from nanoid import generate
from backend.db import get_db


def create_quiz(quiz_ott):
    connection = get_db()
    cursor = connection.cursor()

    # Create quiz record
    quiz_uuid = generate(size=8)
    cursor.execute(
        """
        INSERT INTO quizzes (uuid, ott)
        VALUES (%s, %s)
        """,
        (quiz_uuid, quiz_ott),
    )
    quiz_id = cursor.lastrowid

    # Get node data for the passed in OTT
    cursor.execute(
        """
        SELECT n.id, n.name, n.node_rgt, v.vernacular
        FROM ordered_nodes n
        JOIN vernacular_by_ott v ON v.ott = n.ott AND v.preferred = 1 AND v.lang_primary = 'en'
        WHERE n.ott = %s
        """,
        (quiz_ott,),
    )
    top_node_response = cursor.fetchall()

    if not top_node_response:
        raise BadRequest("No node found with that ott.")

    top_node = dict(zip(["id", "name", "node_rgt", "vernacular"], top_node_response[0]))

    connection.commit()

    return {
        "uuid": quiz_uuid,
        "title": top_node["vernacular"],
        "num_questions": 5,
    }