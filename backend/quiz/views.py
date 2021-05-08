from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound
from nanoid import generate
from sqlalchemy import and_
from sqlalchemy.sql import text
from backend.quiz.submit_answer import submit_answer
from backend.quiz import quiz_questions
from backend import db
from backend.models import Quiz, Node, Vernacular

quiz = Blueprint("quiz", __name__)


@quiz.route("/", methods=["POST"])
def create_quiz():
    body = request.get_json()
    quiz_ott = body["ott"]

    # Create quiz record
    quiz_uuid = generate(size=8)
    quiz = Quiz(uuid=quiz_uuid, ott=quiz_ott, num_questions=5)
    db.session.add(quiz)
    db.session.flush()

    # Get node data for  the passed in OTT
    top_node = (
        db.session.query(Node.id, Node.name, Vernacular.vernacular)
        .join(
            Vernacular,
            and_(
                Vernacular.ott == Node.ott,
                Vernacular.lang_primary == "en",
                Vernacular.preferred,
            ),
            isouter=True,
        )
        .where(Node.ott == quiz_ott)
        .first()
    )

    if not top_node:
        raise BadRequest("No node found with that ott.")

    db.session.commit()

    return {
        "uuid": quiz.uuid,
        "title": top_node.vernacular or top_node.name,
        "num_questions": quiz.num_questions,
    }


@quiz.route("/<uuid>")
def get_quiz(uuid):
    quiz = (
        db.session.query(
            Quiz.id,
            Quiz.uuid,
            Quiz.num_questions,
            Quiz.ott,
            Node.name,
            Vernacular.vernacular,
        )
        .join(Node, Node.ott == Quiz.ott)
        .join(
            Vernacular,
            and_(
                Vernacular.ott == Node.ott,
                Vernacular.lang_primary == "en",
                Vernacular.preferred,
            ),
            isouter=True,
        )
        .where(Quiz.uuid == uuid)
        .first()
    )

    if not quiz:
        raise NotFound()

    response = {
        "quiz": quiz._asdict(),
        "next_question": quiz_questions.get_next_question_for_quiz(quiz._asdict()),
        "completed_questions": quiz_questions.get_completed_questions(uuid),
    }

    db.session.commit()

    return response


@quiz.route("/<uuid>/next_question")
def get_next_quiz_question(uuid):
    quiz = (
        db.session.query(Quiz.id, Quiz.uuid, Quiz.num_questions, Quiz.ott)
        .where(Quiz.uuid == uuid)
        .first()
    )

    question = quiz_questions.get_next_question_for_quiz(quiz._asdict())

    db.session.commit()

    return jsonify(question)


@quiz.route("/<uuid>/submit_answer", methods=["POST"])
def view_submit_answer(uuid):
    body = request.get_json()
    response = submit_answer(
        quiz_uuid=uuid,
        selected_ott=body["selected_ott"],
        question_number=body["question_number"],
    )
    db.session.commit()

    return response


@quiz.route("/<uuid>/questions/<question_number>/rate_question", methods=["POST"])
def rate_question(uuid, question_number):
    body = request.get_json()
    is_good = body["is_good"]

    question = quiz_questions.get_quiz_question_by_number(uuid, int(question_number))

    db.session.execute(
        text(
            """
            UPDATE quiz_questions
            SET good_question = :is_good
            WHERE id = :question_id
            """
        ),
        {"question_id": question["id"], "is_good": is_good},
    )

    db.session.commit()

    return {"is_good": is_good}
