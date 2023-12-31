# coding: utf-8
from . import db, BaseModel
from sqlalchemy.inspection import inspect


class DailyPost(BaseModel):
    __tablename__ = 'daily_post'

    daily_post_id = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), primary_key=True)
    # user_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'))
    post_title = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    post_text = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    images = db.Column(db.JSON)
    topic = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    timestamp = db.Column(db.DateTime)
    # 为 likes 和 comments 设置默认值为 0
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    # likes = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    # comments = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))

    def to_dict(self):
        """将模型转换为字典"""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
