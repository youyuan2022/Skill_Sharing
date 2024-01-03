# coding: utf-8
from . import db, BaseModel


class Likes(BaseModel):
    __tablename__ = 'likes'

    like_id = db.Column(db.String(72, 'utf8mb4_0900_ai_ci'), primary_key=True)
    user_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'))
    liked_type = db.Column(db.Integer, info='1daily_post，2swap_post，3comment')
    liked_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), info='被点赞对象id')
    timestamp = db.Column(db.DateTime)
