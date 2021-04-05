from flask import g
from werkzeug.exceptions import BadRequest, InternalServerError
from random import random
from .utils import make_thumbnail_url
from backend.db import get_db


def generate_quiz_question(quiz):
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT n.id, n.node_rgt
        FROM ordered_nodes n WHERE n.ott = %(ott)s
        """,
        {"ott": quiz["ott"]},
    )

    node = dict(zip(["id", "node_rgt"], cursor.fetchall()[0]))

    # Find a parent node which has at least two direct valid quiz nodes
    cursor.execute(
        """
        SELECT a.id, a.ott, a.name
        FROM ordered_nodes a
        JOIN quiz_nodes q ON q.node_id = a.id
        WHERE a.id BETWEEN %(left_node_id)s AND %(right_node_id)s AND q.can_branch
        ORDER BY power(popularity, 0.08) * rand() DESC
        LIMIT 1
        """,
        {"left_node_id": node["id"], "right_node_id": node["node_rgt"]},
    )
    parent_node_response = cursor.fetchall()

    if not parent_node_response:
        raise InternalServerError(
            f"No suitable parent nodes for the ott: {quiz['ott']}"
        )

    parent_node = dict(zip(["id", "ott", "name"], parent_node_response[0]))

    # Randomly pick two valid child nodes which will become node_left and node_right
    cursor.execute(
        """
        SELECT n.id, n.leaf_lft, n.leaf_rgt
        FROM ordered_nodes n
        JOIN quiz_nodes q on q.node_id = n.id
        WHERE n.real_parent = %(parent_node_id)s
        ORDER BY rand()
        LIMIT 2
        """,
        {"parent_node_id": parent_node["id"]},
    )
    response = cursor.fetchall()

    if len(response) < 2:
        print("Selected parent node has fewer than two valid node children.")
        print(parent_node)
        raise InternalServerError()

    node_left_response, node_right_response = response
    node_left = dict(zip(["id", "leaf_left", "leaf_right"], node_left_response))
    node_right = dict(zip(["id", "leaf_left", "leaf_right"], node_right_response))

    leaf_left_1 = generate_quiz_leaf(node_left, False)
    leaf_left_2 = generate_quiz_leaf(node_left, True, leaf_left_1["id"])
    leaf_right = generate_quiz_leaf(node_right, True)

    swap = random() > 0.5

    question = {
        "compare": leaf_left_1,
        "option1": leaf_left_2 if swap else leaf_right,
        "option2": leaf_right if swap else leaf_left_2,
    }

    save_question_to_db(
        quiz_id=quiz["id"],
        leaf_compare=question["compare"],
        leaf_1=question["option1"],
        leaf_2=question["option2"],
    )

    return question


def generate_quiz_leaf(node, weight_depth, blacklisted_leaf_id=None):
    cursor = get_db().cursor()

    node_data = get_depth_popularity_info(node)

    weight_high_depth_query = "power(((l.popularity - %(min_popularity)s + 1) / (%(max_popularity)s - %(min_popularity)s)) + 4 * ((q.depth - %(min_depth)s) / (%(max_depth)s - %(min_depth)s)), 0.5)"
    weight_low_depth_query = "power(((l.popularity - %(min_popularity)s + 1) / (%(max_popularity)s - %(min_popularity)s)) + 4 * (1 -((q.depth - %(min_depth)s) / (%(max_depth)s - %(min_depth)s))), 0.5)"

    score_query = weight_high_depth_query if weight_depth else weight_low_depth_query

    cursor.execute(
        "select distinct l.id, l.ott, l.name, vernacular_by_ott.vernacular, iucn.status_code, images_by_ott.src, images_by_ott.src_id, "
        + score_query
        + " as score, q.depth, l.popularity, l.wikidata, l.eol"
        """
        from ordered_leaves l
        join quiz_leaves_by_ott q on q.leaf_id = l.id
        join images_by_ott ON (l.ott = images_by_ott.ott AND images_by_ott.best_any = 1)
        left join vernacular_by_ott on (l.ott = vernacular_by_ott.ott and vernacular_by_ott.lang_primary = 'en' and vernacular_by_ott.preferred = 1)
        left join iucn on l.ott = iucn.ott
        where l.id between %(leaf_left)s and %(leaf_right)s and best_any = 1 and l.id != %(blacklisted_leaf_id)s
        group by l.ott
        order by rand() * score desc
        limit 1
        """,
        {
            "leaf_left": node["leaf_left"],
            "leaf_right": node["leaf_right"],
            "min_depth": node_data["min_depth"],
            "max_depth": node_data["max_depth"],
            "min_popularity": node_data["min_popularity"],
            "max_popularity": node_data["max_popularity"],
            "blacklisted_leaf_id": blacklisted_leaf_id or 0,
        },
    )
    leaf_response = cursor.fetchall()
    leaf = dict(
        zip(
            [
                "id",
                "ott",
                "name",
                "vernacular",
                "iucn",
                "img_src",
                "img_src_id",
                "score",
                "depth",
                "popularity",
                "wikidata",
                "eol",
            ],
            leaf_response[0],
        )
    )

    leaf["thumbnail"] = make_thumbnail_url(leaf["img_src"], leaf["img_src_id"])
    return leaf


def get_depth_popularity_info(node):
    cursor = get_db().cursor()

    cursor.execute(
        """
        select min(quiz_leaves_by_ott.depth), max(quiz_leaves_by_ott.depth), min(ordered_leaves.popularity), max(ordered_leaves.popularity)
        from ordered_nodes
        join quiz_leaves_by_ott on quiz_leaves_by_ott.leaf_id between %(leaf_left)s and %(leaf_right)s
        join ordered_leaves on ordered_leaves.id = quiz_leaves_by_ott.leaf_id
        where ordered_nodes.id = %(node_id)s
        """,
        {
            "node_id": node["id"],
            "leaf_left": node["leaf_left"],
            "leaf_right": node["leaf_right"],
        },
    )
    node_data_response = cursor.fetchall()
    node_data = dict(
        zip(
            ["min_depth", "max_depth", "min_popularity", "max_popularity"],
            node_data_response[0],
        )
    )
    return node_data


def save_question_to_db(quiz_id, leaf_compare, leaf_1, leaf_2):
    cursor = get_db().cursor()

    cursor.execute(
        """
        INSERT INTO quiz_questions (quiz_id, compare_ott, option_1_ott, option_2_ott)
        VALUES (%(quiz_id)s, %(leaf_compare_ott)s, %(leaf_1_ott)s, %(leaf_2_ott)s)
        """,
        {
            "quiz_id": quiz_id,
            "leaf_compare_ott": leaf_compare["ott"],
            "leaf_1_ott": leaf_1["ott"],
            "leaf_2_ott": leaf_2["ott"],
        },
    )
