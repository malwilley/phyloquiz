from http.server import BaseHTTPRequestHandler
import os
import mysql.connector
import json
import sys


def make_thumbnail_url(src, src_id):
    return f"https://images.onezoom.org/{src}/{str(src_id)[-3:]}/{src_id}.jpg"


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        body_json = json.loads(post_body)

        query = body_json['query']

        connection = mysql.connector.connect(
            host=os.environ['DATABASE_HOST'],
            user=os.environ['DATABASE_USER'],
            database=os.environ['DATABASE_NAME'],
            password=os.environ['DATABASE_PASSWORD']
        )

        try:

            cursor = connection.cursor()
            cursor.execute(
                '''
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
                WHERE v.vernacular LIKE %(query)s OR n.name LIKE %(query)s
                GROUP BY n.id
                LIMIT 5
                ''',
                {'query': f'%{query}%'}
            )
            results = cursor.fetchall()

            response = [{**dict(zip(["id",
                                     "ott",
                                     "popularity",
                                     "age",
                                     "name",
                                     "vernacular",
                                     "num_species"],
                                    row)),
                         "images": [make_thumbnail_url(src=row[7 + (imgIndex * 2)],
                                                       src_id=row[8 + (imgIndex * 2)]) for imgIndex in range(8)]} for row in results]

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
