# coding: utf-8
from . import db, BaseModel


class DailyPost(BaseModel):
    __tablename__ = 'daily_post'

    daily_post_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True)
    user_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'))
    post_title = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='标题')
    post_text = db.Column(db.String(1000, 'utf8mb4_0900_ai_ci'), info='内容')
    images = db.Column(db.JSON, info='图片')
    topic = db.Column(db.String(64, 'utf8mb4_0900_ai_ci'), info='主题')
    likes = db.Column(db.Integer, default=0, info='点赞数')
    comments = db.Column(db.Integer, default=0, info='评论数')
    timestamp = db.Column(db.DateTime)
