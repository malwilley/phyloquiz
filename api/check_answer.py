import sys
import json
import mysql.connector
import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        body_json = json.loads(post_body)

        leaf_compare_id = body_json['leaf_compare_id']
        leaf_1_id = body_json['leaf_1_id']
        leaf_2_id = body_json['leaf_2_id']
        user_choice = body_json['user_choice']

        connection = mysql.connector.connect(
            host=os.environ['DATABASE_HOST'],
            user=os.environ['DATABASE_USER'],
            database=os.environ['DATABASE_NAME'],
            password=os.environ['DATABASE_PASSWORD']
        )

        try:
            cursor = connection.cursor()

            nearest_common_ancestor_1 = nearest_common_ancestor(
                cursor, leaf_compare_id, leaf_1_id)
            nearest_common_ancestor_2 = nearest_common_ancestor(
                cursor, leaf_compare_id, leaf_2_id)

            correct_leaf_id = leaf_1_id if nearest_common_ancestor_1[
                "id"] > nearest_common_ancestor_2["id"] else leaf_2_id
            correct = correct_leaf_id == user_choice

            close_ancestors = other_common_ancestors(
                cursor,
                min_node_id=min(
                    nearest_common_ancestor_1['id'],
                    nearest_common_ancestor_2['id']),
                max_node_id=max(
                    nearest_common_ancestor_1['id'],
                    nearest_common_ancestor_2['id']),
                leaf_1_id=correct_leaf_id,
                leaf_2_id=leaf_compare_id)

            far_ancestors = other_common_ancestors(
                cursor,
                min_node_id=0,
                max_node_id=min(
                    nearest_common_ancestor_1['id'],
                    nearest_common_ancestor_2['id']),
                leaf_1_id=correct_leaf_id,
                leaf_2_id=leaf_compare_id)

            response = {
                'correct': correct,
                'leaf_1_ancestor': nearest_common_ancestor_1,
                'leaf_2_ancestor': nearest_common_ancestor_2,
                'close_ancestors': close_ancestors,
                'far_ancestors': far_ancestors
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


def other_common_ancestors(
        cursor,
        min_node_id,
        max_node_id,
        leaf_1_id,
        leaf_2_id):
    cursor.execute(
        """
        SELECT DISTINCT n.id, n.ott, n.age, n.name, v.vernacular
        FROM (
            SELECT n1.id, n1.ott, n1.age, n1.name
            FROM ordered_nodes n1
            JOIN (
              SELECT id, ott, age, name
              FROM ordered_nodes
              WHERE MBRIntersects(Point(0, %(leaf_2_id)s), leaves) AND real_parent >= 0 AND id > %(min_node_id)s AND id <= %(max_node_id)s AND ott IS NOT NULL
            ) n2 ON n1.id = n2.id
            WHERE MBRIntersects(Point(0, %(leaf_1_id)s), leaves) AND real_parent >= 0 AND n1.id > %(min_node_id)s AND n1.id <= %(max_node_id)s AND n1.ott IS NOT NULL
            ORDER BY n1.id DESC
            LIMIT 2
        ) n
        LEFT JOIN vernacular_by_ott v ON v.ott = n.ott AND v.lang_primary = 'en' AND v.preferred
        GROUP BY n.id
        ORDER BY n.id DESC
        """,
        {
            'min_node_id': min_node_id,
            'max_node_id': max_node_id,
            'leaf_1_id': leaf_1_id,
            'leaf_2_id': leaf_2_id,
        }
    )

    response = cursor.fetchall()

    nodes = [dict(
        zip(["id",
             "ott",
             "age",
             "name",
             "vernacular"],
            node)) for node in response]

    return nodes


def nearest_common_ancestor(
        cursor,
        leaf_1_id,
        leaf_2_id):
    cursor.execute(
        """
        SELECT n.id, n.ott, n.age, n.name, v.vernacular
        FROM (
            SELECT distinct n1.id, n1.ott, n1.age, n1.name
            FROM ordered_nodes n1
            JOIN (
              SELECT id, ott, age, name
              FROM ordered_nodes
              WHERE MBRIntersects(Point(0, %(leaf_2_id)s), leaves) AND real_parent >= 0
            ) n2 ON n1.id = n2.id
            WHERE MBRIntersects(Point(0, %(leaf_1_id)s), leaves) AND real_parent >= 0
            ORDER BY id DESC
            LIMIT 1
        ) n
        LEFT JOIN vernacular_by_ott v ON v.ott = n.ott AND v.lang_primary = 'en' AND v.preferred
        """,
        {
            'leaf_1_id': leaf_1_id,
            'leaf_2_id': leaf_2_id
        })
    response = cursor.fetchall()

    if not response:
        return None

    ancestor_node = dict(
        zip(["id",
             "ott",
             "age",
             "name",
             "vernacular"],
            response[0]))

    return ancestor_node
