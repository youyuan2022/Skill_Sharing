# coding: utf-8
from . import db, BaseModel


class UserFollow(BaseModel):
    __tablename__ = 'user_follow'

    follow_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True)
    follower_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), nullable=False, info='关注者')
    followee_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), info='被关注者')
    follow_date = db.Column(db.DateTime)
