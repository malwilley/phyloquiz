from flask import g
from backend.services.utils import make_thumbnail_url
from .sql_partials import select_node
from backend.db import get_db


def search_nodes(query):
    cursor = get_db().cursor()

    cursor.execute(
        select_node
        + """
        WHERE (v.vernacular LIKE %(query)s OR n.name LIKE %(query)s) AND q.category_node
        GROUP BY n.id
        LIMIT 5
        """,
        {"query": f"%{query}%"},
    )
    results = cursor.fetchall()

    return [
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
