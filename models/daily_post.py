# coding: utf-8
from . import db, BaseModel


class DailyPost(BaseModel):
    __tablename__ = 'daily_post'

    daily_post_id = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), primary_key=True)
    user_id = db.Column(db.Integer)
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
