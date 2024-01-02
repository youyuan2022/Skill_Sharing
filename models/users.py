# coding: utf-8
from . import db, BaseModel


class Users(BaseModel):
    __tablename__ = 'users'

    user_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True)
    password = db.Column(db.String(72, 'utf8mb4_0900_ai_ci'))
    status = db.Column(db.Integer, info='用户状态:1--正常状态;2--禁用状态')
    wx_openid = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'))
    role = db.Column(db.Integer, info='角色---1管理/2用户/3已注销')
    registration_time = db.Column(db.DateTime, info='注册时间')
