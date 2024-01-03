# coding: utf-8
from . import db, BaseModel


class SwapPost(BaseModel):
    __tablename__ = 'swap_post'

    swap_post_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True)
    user_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), info='发帖者id')
    swap_method = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='交换方法（线上线下）')
    post_text = db.Column(db.String(1000, 'utf8mb4_0900_ai_ci'), info='正文内容')
    images = db.Column(db.JSON, info='图像url')
    appointment_time = db.Column(db.DateTime, info='约定时间')
    likes = db.Column(db.Integer, info='点赞数')
    comments = db.Column(db.Integer, info='评论数')
    timestamp = db.Column(db.DateTime, info='时间戳')
