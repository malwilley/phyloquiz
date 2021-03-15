from flask import g
from backend.services.utils import make_thumbnail_url
from backend.db import get_db
from .sql_partials import select_node


def get_featured_nodes():
    cursor = get_db().cursor()

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

    cursor.execute(
        select_node
        + """
        WHERE n.id IN (%s, %s, %s, %s, %s, %s, %s, %s)
        GROUP BY n.id;
        """,
        tuple(featured_node_ids),
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
                    src=row[7 + (imgIndex * 2)],
                    src_id=row[8 + (imgIndex * 2)],
                )
                for imgIndex in range(8)
            ],
        }
        for row in results
    ]
