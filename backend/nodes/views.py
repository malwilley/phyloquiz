from flask import Blueprint, request, jsonify
from backend.utils import make_thumbnail_url
from sqlalchemy import bindparam
from sqlalchemy.sql import text
from backend import db
from backend.models import (
    Quiz,
    QuizNode,
    QuizQuestion,
    Node,
    Vernacular,
    QuizAnswer,
    Image,
)

nodes = Blueprint("nodes", __name__)

select_node_sql = """
    SELECT n.id, n.ott, popularity, age, name, v.vernacular, q.num_quiz_leaves, i1.src, i1.src_id, i2.src, i2.src_id,  i3.src, i3.src_id,  i4.src, i4.src_id,  i5.src, i5.src_id,  i6.src, i6.src_id,  i7.src, i7.src_id,  i8.src, i8.src_id
    FROM ordered_nodes n
    JOIN quiz_nodes q on q.node_id = n.id
    JOIN vernacular_by_ott v ON v.ott = n.ott and v.lang_primary = 'en' and v.preferred
    JOIN images_by_ott i1 ON i1.overall_best_any AND i1.ott = n.rep1
    JOIN images_by_ott i2 ON i2.overall_best_any AND i2.ott = n.rep2
    JOIN images_by_ott i3 ON i3.overall_best_any AND i3.ott = n.rep3
    JOIN images_by_ott i4 ON i4.overall_best_any AND i4.ott = n.rep4
    JOIN images_by_ott i5 ON i5.overall_best_any AND i5.ott = n.rep5
    JOIN images_by_ott i6 ON i6.overall_best_any AND i6.ott = n.rep6
    JOIN images_by_ott i7 ON i7.overall_best_any AND i7.ott = n.rep7
    JOIN images_by_ott i8 ON i8.overall_best_any AND i8.ott = n.rep8
    """


@nodes.route("/")
def search_nodes():
    query = request.args["q"]

    results = db.session.execute(
        text(
            select_node_sql
            + """
            WHERE (v.vernacular LIKE :query OR n.name LIKE :query) AND q.category_node
            GROUP BY n.id
            LIMIT 5
            """
        ),
        {"query": f"%{query}%"},
    ).fetchall()

    response = [
        {
            **dict(
                zip(
                    [
                        "id",
                        "ott",
                        "popularity",
                        "age",
                        "name",
                        "vernacular",
                        "num_species",
                    ],
                    row,
                )
            ),
            "images": [
                make_thumbnail_url(
                    src=row[7 + (imgIndex * 2)], src_id=row[8 + (imgIndex * 2)]
                )
                for imgIndex in range(8)
            ],
        }
        for row in results
    ]

    return jsonify(response)


@nodes.route("/featured")
def get_featured_quizzes():
    featured_node_ids = [
        884807,
        890106,
        837081,
        900106,
        122295,
        60924,  # eukaryotes
        876129,  # amphibians
        1082584,  # arthropods
    ]

    results = db.session.execute(
        text(
            select_node_sql
            + """
            WHERE n.id IN :node_ids
            GROUP BY n.id;
            """
        ).bindparams(bindparam("node_ids", expanding=True)),
        {"node_ids": featured_node_ids},
    ).fetchall()

    response = [
        {
            **dict(
                zip(
                    [
                        "id",
                        "ott",
                        "popularity",
                        "age",
                        "name",
                        "vernacular",
                        "num_species",
                    ],
                    row,
                )
            ),
            "images": [
                make_thumbnail_url(
                    src=row[7 + (imgIndex * 2)],
                    src_id=row[8 + (imgIndex * 2)],
                )
                for imgIndex in range(8)
            ],
        }
        for row in results
    ]

    return jsonify(response)
