# coding: utf-8
from . import db, BaseModel


class UserInfo(BaseModel):
    __tablename__ = 'user_info'

    user_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True)
    user_name = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, info='名称\\r\\n名称')
    profile_picture = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='头像')
    signature = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='个性签名')
    gender = db.Column(db.String(64, 'utf8mb4_0900_ai_ci'), info='性别')
    phone = db.Column(db.String(24, 'utf8mb4_0900_ai_ci'), info='电话')
    date_of_birth = db.Column(db.DateTime, info='出生日期')
    address = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='地址')
