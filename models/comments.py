# coding: utf-8
from . import db, BaseModel


class Comments(BaseModel):
    __tablename__ = 'comments'

    comment_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True)
    user_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), info='评论者')
    comment_text = db.Column(db.String(1000, 'utf8mb4_0900_ai_ci'), info='内容')
    commented_type = db.Column(db.Integer, nullable=False, info='1.daily_post 2.swap_post ')
    commented_id = db.Column(db.Integer, nullable=False)
    parent_comment_id = db.Column(db.Integer, info='父评论id null表示没有父评论')
    likes = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='点赞数')
    replies = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='回复数')
    timestamp = db.Column(db.DateTime)
