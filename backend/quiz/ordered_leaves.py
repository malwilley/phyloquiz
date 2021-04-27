from flask import g
from werkzeug.exceptions import NotFound
from backend.utils import make_thumbnail_url
from backend import db
from backend.models import Leaf, Vernacular, Image, Iucn
from sqlalchemy import distinct


def get_species_info(ott):
    species = (
        db.session.query(Leaf, Image, Vernacular, Iucn)
        .distinct(Leaf.id)
        .join(Image, Image.ott == Leaf.ott)
        .join(Vernacular, Vernacular.ott == Leaf.ott, isouter=True)
        .join(Iucn, Iucn.ott == Leaf.ott, isouter=True)
        .where(Leaf.ott == ott)
        .where(Vernacular.lang_primary == "en")
        .where(Vernacular.preferred)
        .first()
    )

    if not species:
        raise NotFound()

    (leaf, image, vernacular, iucn) = species

    return {
        "id": leaf.id,
        "ott": leaf.ott,
        "name": leaf.name,
        "vernacular": vernacular.vernacular if vernacular else None,
        "iucn": iucn.status_code if iucn else None,
        "wikidata": leaf.wikidata,
        "eol": leaf.eol,
        "thumbnail": make_thumbnail_url(image.src, image.src_id),
    }


def get_leaf_info(ott):
    leaf = db.session.query(Leaf.id, Leaf.ott, Leaf.name).where(Leaf.ott == ott).first()

    if not leaf:
        return None

    return leaf._asdict()
