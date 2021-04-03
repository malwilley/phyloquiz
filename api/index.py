from flask import Flask, request, g, jsonify
import json
import traceback
from werkzeug.exceptions import HTTPException

from backend.views.get_quiz import get_quiz as view_get_quiz
from backend.views.create_quiz import create_quiz as view_create_quiz
from backend.views.submit_answer import submit_answer as view_submit_answer
from backend.views.search_nodes import search_nodes as view_search_nodes
from backend.views.get_featured_nodes import (
    get_featured_nodes as view_get_featured_nodes,
)
from backend.views.get_next_quiz_question import (
    get_next_question_for_quiz_uuid as view_get_next_question,
)
from backend.views.rate_question import (
    rate_question as view_rate_question,
)

app = Flask(__name__)


@app.route("/api/generate_quiz", methods=["POST"])
def create_quiz():
    body = request.get_json()
    return view_create_quiz(body["ott"])


@app.route("/api/quiz/<uuid>")
def get_quiz(uuid):
    return view_get_quiz(uuid)


@app.route("/api/quiz/<uuid>/next_question")
def get_next_quiz_question(uuid):
    return view_get_next_question(uuid)


@app.route("/api/quiz/<uuid>/submit_answer", methods=["POST"])
def submit_answer(uuid):
    body = request.get_json()
    return view_submit_answer(
        quiz_uuid=uuid,
        selected_ott=body["selected_ott"],
        question_number=body["question_number"],
    )


@app.route(
    "/api/quiz/<uuid>/questions/<question_number>/rate_question", methods=["POST"]
)
def rate_question(uuid, question_number):
    body = request.get_json()
    return view_rate_question(
        quiz_uuid=uuid,
        question_number=int(question_number),
        is_good=body["is_good"],
    )


@app.route("/api/featured_nodes")
def get_featured_quizzes():
    return jsonify(view_get_featured_nodes())


@app.route("/api/nodes")
def search_nodes():
    query = request.args["q"]
    return jsonify(view_search_nodes(query))


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    traceback.print_exc(e)

    return {
        "code": 500,
        "name": "Internal Server Error",
        "description": "An unknown error occurred.",
    }, 500


@app.teardown_request
def close_db_connection(ex):
    db = g.pop("db", None)

    if db is not None:
        db.close()