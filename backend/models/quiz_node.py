from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy.dialects import mysql
from datetime import datetime
from geoalchemy2 import Geometry


# Subset of ordered_nodes which only includes nodes that are valid for use in quizzes.
class QuizNode(db.Model):
    __tablename__ = "quiz_nodes"

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey("ordered_nodes.id"), nullable=False)
    num_quiz_leaves = db.Column(db.Integer, nullable=False, default=0)

    # Node has at least 1 descendant with can_branch=True, and will show up as a quiz option
    category_node = db.Column(db.Boolean, nullable=False, default=False)

    # Node has at least 2 children which are also valid quiz nodes
    can_branch = db.Column(db.Boolean, nullable=False, default=False)

    # Same as [leaf_lft, leaf_rgt], but much more performant when querying all children for multiple nodes
    # See https://explainextended.com/2009/09/29/adjacency-list-vs-nested-sets-mysql/
    spatial_leaf_ids = db.Column(Geometry("LINESTRING"), nullable=False)

    def __repr__(self):
        return "<QuizNode %r>" % self.node_id
