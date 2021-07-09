from db import db
from typing import List
import datetime

class TaskModel(db.Model):
    __tabletitle__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False, )
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, title, content):
        self.title = title
        self.content = content
        

    def __repr__(self):
        return 'TaskModel(title=%s, content=%s)' % (self.title, self.content)

    def json(self):
        return {'title': self.title, 'content': self.content}

    @classmethod
    def find_by_title(cls, title) -> "TaskModel":
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id) -> "TaskModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["TaskModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()