from http.server import BaseHTTPRequestHandler
from datetime import datetime
import mysql.connector
import json
import os
from random import random


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        body_json = json.loads(post_body)
        top_ott = body_json['ott']

        connection = mysql.connector.connect(
            host=os.environ['DATABASE_HOST'],
            user=os.environ['DATABASE_USER'],
            database=os.environ['DATABASE_NAME'],
            password=os.environ['DATABASE_PASSWORD']
        )

        try:
            cursor = connection.cursor()

            # Get node data for the passed in OTT
            cursor.execute(
                """
                SELECT n.id, n.name, n.node_rgt, v.vernacular
                FROM ordered_nodes n
                JOIN vernacular_by_ott v ON v.ott = n.ott AND v.preferred = 1 AND v.lang_primary = 'en'
                WHERE n.ott = %s
                """,
                (top_ott,)
            )
            top_node_response = cursor.fetchall()[0]
            top_node = dict(
                zip(["id", "name", "node_rgt", "vernacular"], top_node_response))

            # Find a parent node which has at least two direct valid quiz nodes
            cursor.execute(
                """
                select a.id, a.ott, a.name, (select count(*) from ordered_nodes d where d.real_parent = a.id and d.num_quiz_leaves > 1) as num_valid_children
                from ordered_nodes a
                join quiz_nodes q on q.node_id = a.id
                where a.id between %(left_node_id)s and %(right_node_id)s and popularity > 0 and real_parent >= 0
                having num_valid_children > 1
                order by power(popularity, 0.08) * rand() desc
                limit 1
                """,
                {
                    'left_node_id': top_node['id'],
                    'right_node_id': top_node['node_rgt']
                }
            )
            parent_node_response = cursor.fetchall()[0]
            parent_node = dict(
                zip(["id", "ott", "name"], parent_node_response))

            # Randomly pick two valid child nodes which will become node_left
            # and node_right
            cursor.execute(
                """
                SELECT n.id, n.leaf_lft, n.leaf_rgt
                FROM ordered_nodes n
                JOIN quiz_nodes q on q.node_id = n.id
                WHERE n.real_parent = %(parent_node_id)s AND q.num_quiz_leaves > 1
                ORDER BY rand()
                LIMIT 2
                """,
                {
                    'parent_node_id': parent_node['id']
                }
            )
            node_left_response, node_right_response = cursor.fetchall()
            node_left = dict(
                zip(["id", "leaf_left", "leaf_right"], node_left_response))
            node_right = dict(
                zip(["id", "leaf_left", "leaf_right"], node_right_response))

            leaf_left_1 = generate_quiz_leaf(cursor, node_left, False)
            leaf_left_2 = generate_quiz_leaf(
                cursor, node_left, True, leaf_left_1['id'])
            leaf_right = generate_quiz_leaf(cursor, node_right, True)

            swap = random() > 0.5

            response = {
                'quiz_title': top_node['vernacular'],
                'parent_node': parent_node,
                'leaf_compare': leaf_left_1,
                'leaf_1': leaf_left_2 if swap else leaf_right,
                'leaf_2': leaf_right if swap else leaf_left_2
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode(encoding='utf_8'))

        except BaseException as ex:
            print(ex)
            self.send_response(500)
            self.end_headers()

        connection.close()
        return


def generate_quiz_leaf(cursor, node, weight_depth, blacklisted_leaf_id=None):
    node_data = get_depth_popularity_info(cursor, node)

    weight_high_depth_query = "power(((l.popularity - %(min_popularity)s + 1) / (%(max_popularity)s - %(min_popularity)s)) + 4 * ((q.depth - %(min_depth)s) / (%(max_depth)s - %(min_depth)s)), 0.5)"
    weight_low_depth_query = "power(((l.popularity - %(min_popularity)s + 1) / (%(max_popularity)s - %(min_popularity)s)) + 4 * (1 -((q.depth - %(min_depth)s) / (%(max_depth)s - %(min_depth)s))), 0.5)"

    score_query = weight_high_depth_query if weight_depth else weight_low_depth_query

    cursor.execute(
        "select distinct l.id, l.ott, l.name, vernacular_by_ott.vernacular, iucn.status_code, images_by_ott.src, images_by_ott.src_id, " +
        score_query +
        " as score, q.depth, l.popularity, l.wikidata, l.eol"
        """
        from ordered_leaves l
        join quiz_leaves_by_ott q on q.leaf_id = l.id
        join images_by_ott on l.ott = images_by_ott.ott
        left join vernacular_by_ott on (l.ott = vernacular_by_ott.ott and vernacular_by_ott.lang_primary = 'en' and vernacular_by_ott.preferred = 1)
        left join iucn on l.ott = iucn.ott
        where l.id between %(leaf_left)s and %(leaf_right)s and best_any = 1 and l.id != %(blacklisted_leaf_id)s
        group by l.ott
        order by rand() * score desc
        limit 1
        """,
        {
            'leaf_left': node['leaf_left'],
            'leaf_right': node['leaf_right'],
            'min_depth': node_data['min_depth'],
            'max_depth': node_data['max_depth'],
            'min_popularity': node_data['min_popularity'],
            'max_popularity': node_data['max_popularity'],
            'blacklisted_leaf_id': blacklisted_leaf_id or 0})
    leaf_response = cursor.fetchall()
    leaf = dict(zip(["id",
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
                     "eol"],
                    leaf_response[0]))

    leaf['thumbnail'] = make_thumbnail_url(
        leaf['img_src'], leaf['img_src_id'])
    return leaf


def get_depth_popularity_info(cursor, node):
    cursor.execute(
        """
        select min(quiz_leaves_by_ott.depth), max(quiz_leaves_by_ott.depth), min(ordered_leaves.popularity), max(ordered_leaves.popularity)
        from ordered_nodes
        join quiz_leaves_by_ott on quiz_leaves_by_ott.leaf_id between %(leaf_left)s and %(leaf_right)s
        join ordered_leaves on ordered_leaves.id = quiz_leaves_by_ott.leaf_id
        where ordered_nodes.id = %(node_id)s
        """,
        {
            'node_id': node['id'],
            'leaf_left': node['leaf_left'],
            'leaf_right': node['leaf_right'],
        }
    )
    node_data_response = cursor.fetchall()
    node_data = dict(zip(["min_depth",
                          "max_depth",
                          "min_popularity",
                          "max_popularity"],
                         node_data_response[0]))
    return node_data


def make_thumbnail_url(src, src_id):
    return f"https://images.onezoom.org/{src}/{str(src_id)[-3:]}/{src_id}.jpg"
