from flask import g
from werkzeug.exceptions import BadRequest, InternalServerError
from random import random
from backend.utils import make_thumbnail_url
from backend import db
from backend.models import Quiz, QuizNode, QuizQuestion, Node, Vernacular, QuizAnswer
from sqlalchemy import between, func, desc
from sqlalchemy.sql import text


def generate_quiz_question(quiz):
    node = (
        db.session.query(Node.id, Node.node_rgt).where(Node.ott == quiz["ott"]).first()
    )

    # Step 1: Pick two random leaves
    (leaf1, leaf2) = step1_get_random_leaves(node)

    # Step 2: Get most recent common ancestor node
    common_node = step2_get_common_ancestor(leaf1, leaf2)

    # Step 3: Climb up tree and attempt to find a named node that has a distinct other set of leaves
    ancestor_common_node = step3_climb_tree_for_second_node(
        common_node, min_node_id=node.id
    )

    # Step 4: Get third leaf from other branch
    leaf3 = step4_get_third_leaf(
        ancestor_common_node,
    )

    # Randomly pick two valid child nodes which will become node_left and node_right
    result = db.session.execute(
        text(
            """
            SELECT n.id, n.leaf_lft, n.leaf_rgt
            FROM ordered_nodes n
            JOIN quiz_nodes q on q.node_id = n.id
            WHERE n.real_parent = :parent_node_id AND q.num_quiz_leaves > 1
            ORDER BY rand()
            LIMIT 2
            """
        ),
        {"parent_node_id": parent_node.id},
    ).fetchall()

    if len(result) < 2:
        print("Selected parent node has fewer than two valid node children.")
        print(parent_node._asdict())
        raise InternalServerError()

    node_left_result, node_right_result = result
    node_left = dict(zip(["id", "leaf_left", "leaf_right"], node_left_result))
    node_right = dict(zip(["id", "leaf_left", "leaf_right"], node_right_result))

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


def step1_get_random_leaves(quiz_node):
    leaves_response = db.session.execute(
        text(
            """
            select distinct l.id, l.ott, l.name, vernacular_by_ott.vernacular, iucn.status_code, images_by_ott.src, images_by_ott.src_id, q.depth, l.popularity, l.wikidata, l.eol
            from ordered_leaves l
            join quiz_leaves_by_ott q on q.leaf_id = l.id
            join images_by_ott ON (l.ott = images_by_ott.ott AND images_by_ott.best_any = 1)
            left join vernacular_by_ott on (l.ott = vernacular_by_ott.ott and vernacular_by_ott.lang_primary = 'en' and vernacular_by_ott.preferred = 1)
            left join iucn on l.ott = iucn.ott
            where l.id between :leaf_left and :leaf_right and best_any = 1
            group by l.ott
            order by rand()
            limit 2
            """
        ),
        {
            "leaf_left": quiz_node["leaf_left"],
            "leaf_right": quiz_node["leaf_right"],
        },
    ).fetchall()

    leaves = [
        dict(
            zip(
                [
                    "id",
                    "ott",
                    "name",
                    "vernacular",
                    "iucn",
                    "img_src",
                    "img_src_id",
                    "depth",
                    "popularity",
                    "wikidata",
                    "eol",
                ],
                leaf_response,
            )
        )
        for leaf_response in leaves_response
    ]

    return leaves


def step2_get_common_ancestor(leaf1, leaf2):
    return nearest_common_ancestor(leaf1["id"], leaf2["id"])


def nearest_common_ancestor(leaf_1_id, leaf_2_id):
    response = db.session.execute(
        text(
            """
            SELECT DISTINCT n.id, n.ott, n.age, n.name, v.vernacular
            FROM (
                SELECT DISTINCT q1.id, q1.node_id
                FROM quiz_nodes q1
                JOIN (
                    SELECT *
                    FROM quiz_nodes
                    WHERE MBRIntersects(Point(0, :leaf_2_id), spatial_leaf_ids)
                ) q2 ON q1.id = q2.id
                WHERE MBRIntersects(Point(0, :leaf_1_id), q1.spatial_leaf_ids)
                ORDER BY q1.node_id DESC
                LIMIT 1
            ) q
            JOIN ordered_nodes n ON n.id = q.node_id
            LEFT JOIN vernacular_by_ott v ON v.ott = n.ott AND v.lang_primary = 'en' AND v.preferred
            """
        ),
        {"leaf_1_id": leaf_1_id, "leaf_2_id": leaf_2_id},
    ).fetchall()

    if not response:
        return None

    ancestor_node = dict(zip(["id", "ott", "age", "name", "vernacular"], response[0]))

    return ancestor_node


def step3_climb_tree_for_second_node(node, min_node_id):
    response = db.session.execute(
        text(
            """
            SELECT id
            FROM ordered_nodes 
            WHERE MBRIntersects(Point(0, :node_id), spatial_nodes) AND name IS NOT NULL AND id > :min_node_id
            ORDER BY q1.node_id DESC
            LIMIT 1
            """
        ),
        {"node_id": node["id"], "min_node_id": min_node_id},
    ).fetchall()

    if not response:
        print("No node after climbing")
        return None

    ancestor_node = dict(zip(["id"], response[0]))

    return ancestor_node


def step4_get_third_leaf(node, min_filtered_leaf_id, max_filtered_leaf_id):
    leaves_response = db.session.execute(
        text(
            """
            select distinct l.id, l.ott, l.name, vernacular_by_ott.vernacular, iucn.status_code, images_by_ott.src, images_by_ott.src_id, q.depth, l.popularity, l.wikidata, l.eol
            FROM ordered_nodes n
            JOIN ordered_leaves l ON MBRContains(Point(0, l.id), n.leaves)
            join images_by_ott ON (l.ott = images_by_ott.ott AND images_by_ott.best_any = 1)
            left join vernacular_by_ott on (l.ott = vernacular_by_ott.ott and vernacular_by_ott.lang_primary = 'en' and vernacular_by_ott.preferred = 1)
            left join iucn on l.ott = iucn.ott
            WHERE l.valid_quiz_leaf AND MBRContains(Point(0, l.id), n.leaves)
            where l.id between :leaf_left and :leaf_right and best_any = 1
            group by l.ott
            order by rand()
            limit 1
            """
        ),
        {
            "node_id": node["id"],
            "min_filtered_leaf_id": min_filtered_leaf_id,
            "max_filtered_leaf_id": max_filtered_leaf_id,
        },
    ).fetchall()

    leaves = [
        dict(
            zip(
                [
                    "id",
                    "ott",
                    "name",
                    "vernacular",
                    "iucn",
                    "img_src",
                    "img_src_id",
                    "depth",
                    "popularity",
                    "wikidata",
                    "eol",
                ],
                leaf_response,
            )
        )
        for leaf_response in leaves_response
    ]

    return leaves


def generate_quiz_leaf(node, weight_depth, blacklisted_leaf_id=None):
    node_data = get_depth_popularity_info(node)

    weight_high_depth_query = "power(((l.popularity -:min_popularity + 1) / (:max_popularity - :min_popularity)) + 4 * ((q.depth - :min_depth) / (:max_depth - :min_depth)), 0.5)"
    weight_low_depth_query = "power(((l.popularity - :min_popularity + 1) / (:max_popularity - :min_popularity)) + 4 * (1 -((q.depth - :min_depth) / (:max_depth - :min_depth))), 0.5)"

    score_query = weight_high_depth_query if weight_depth else weight_low_depth_query

    leaf_response = db.session.execute(
        text(
            "select distinct l.id, l.ott, l.name, vernacular_by_ott.vernacular, iucn.status_code, images_by_ott.src, images_by_ott.src_id, "
            + score_query
            + " as score, q.depth, l.popularity, l.wikidata, l.eol"
            """
            from ordered_leaves l
            join quiz_leaves_by_ott q on q.leaf_id = l.id
            join images_by_ott ON (l.ott = images_by_ott.ott AND images_by_ott.best_any = 1)
            left join vernacular_by_ott on (l.ott = vernacular_by_ott.ott and vernacular_by_ott.lang_primary = 'en' and vernacular_by_ott.preferred = 1)
            left join iucn on l.ott = iucn.ott
            where l.id between :leaf_left and :leaf_right and best_any = 1 and l.id != :blacklisted_leaf_id
            group by l.ott
            order by rand() * score desc
            limit 1
            """
        ),
        {
            "leaf_left": node["leaf_left"],
            "leaf_right": node["leaf_right"],
            "min_depth": node_data["min_depth"],
            "max_depth": node_data["max_depth"],
            "min_popularity": node_data["min_popularity"],
            "max_popularity": node_data["max_popularity"],
            "blacklisted_leaf_id": blacklisted_leaf_id or 0,
        },
    ).fetchall()

    if not leaf_response:
        print("Leaf generation failed.")
        print(node, node_data, blacklisted_leaf_id)
        raise InternalServerError("Leaf generation failed.")

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
    node_data_response = db.session.execute(
        text(
            """
            select min(quiz_leaves_by_ott.depth), max(quiz_leaves_by_ott.depth), min(ordered_leaves.popularity), max(ordered_leaves.popularity)
            from ordered_nodes
            join quiz_leaves_by_ott on quiz_leaves_by_ott.leaf_id between :leaf_left and :leaf_right
            join ordered_leaves on ordered_leaves.id = quiz_leaves_by_ott.leaf_id
            where ordered_nodes.id = :node_id
            """
        ),
        {
            "node_id": node["id"],
            "leaf_left": node["leaf_left"],
            "leaf_right": node["leaf_right"],
        },
    ).fetchall()
    node_data = dict(
        zip(
            ["min_depth", "max_depth", "min_popularity", "max_popularity"],
            node_data_response[0],
        )
    )
    return node_data


def save_question_to_db(quiz_id, leaf_compare, leaf_1, leaf_2):
    db.session.execute(
        text(
            """
            INSERT INTO quiz_questions (quiz_id, compare_ott, option_1_ott, option_2_ott)
            VALUES (:quiz_id, :leaf_compare_ott, :leaf_1_ott, :leaf_2_ott)
            """
        ),
        {
            "quiz_id": quiz_id,
            "leaf_compare_ott": leaf_compare["ott"],
            "leaf_1_ott": leaf_1["ott"],
            "leaf_2_ott": leaf_2["ott"],
        },
    )
