import os
from flask import Flask, request, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import traceback
from werkzeug.exceptions import HTTPException


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql+mysqlconnector://{user}:{password}@{host}/{database}".format(
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        host=os.environ.get("DATABASE_HOST"),
        database=os.environ.get("DATABASE_NAME"),
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .quiz import quiz as quiz_blueprint

    app.register_blueprint(quiz_blueprint, url_prefix="/api/quiz")

    from .nodes import nodes as nodes_blueprint

    app.register_blueprint(nodes_blueprint, url_prefix="/api/nodes")

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
        # Pass through HTTP errors
        if isinstance(e, HTTPException):
            return e

        traceback.print_exc(e)

        return {
            "code": 500,
            "name": "Internal Server Error",
            "description": "An unknown error occurred.",
        }, 500

    return app