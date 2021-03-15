from flask import g
import mysql.connector
import os


def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=os.environ["DATABASE_HOST"],
            user=os.environ["DATABASE_USER"],
            database=os.environ["DATABASE_NAME"],
            password=os.environ["DATABASE_PASSWORD"],
        )

    return g.db