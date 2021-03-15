from flask import g
from werkzeug.exceptions import NotFound
from .utils import make_thumbnail_url
from backend.db import get_db


def get_species_info(ott):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT DISTINCT l.id, l.ott, l.name, vernacular_by_ott.vernacular, iucn.status_code, l.wikidata, l.eol, images_by_ott.src, images_by_ott.src_id
        FROM ordered_leaves l
        JOIN images_by_ott ON (l.ott = images_by_ott.ott AND images_by_ott.best_any = 1)
        LEFT JOIN vernacular_by_ott ON (l.ott = vernacular_by_ott.ott AND vernacular_by_ott.lang_primary = 'en' AND vernacular_by_ott.preferred = 1)
        LEFT JOIN iucn ON l.ott = iucn.ott
        WHERE l.ott = %(ott)s
        LIMIT 1
        """,
        {"ott": ott},
    )

    species_response = cursor.fetchall()

    if not species_response:
        raise NotFound()

    species_data = dict(
        zip(
            [
                "id",
                "ott",
                "name",
                "vernacular",
                "iucn",
                "wikidata",
                "eol",
                "img_src",
                "img_src_id",
            ],
            species_response[0],
        )
    )

    return {
        "id": species_data["id"],
        "ott": species_data["ott"],
        "name": species_data["name"],
        "vernacular": species_data["vernacular"],
        "iucn": species_data["iucn"],
        "wikidata": species_data["wikidata"],
        "eol": species_data["eol"],
        "thumbnail": make_thumbnail_url(
            species_data["img_src"], species_data["img_src_id"]
        ),
    }


def get_leaf_info(ott):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT l.id, l.ott, l.name
        FROM ordered_leaves l
        WHERE l.ott = %(ott)s
        """,
        {"ott": ott},
    )

    response = cursor.fetchall()

    if not response:
        return None

    return dict(zip(["id", "ott", "name"], response[0]))
