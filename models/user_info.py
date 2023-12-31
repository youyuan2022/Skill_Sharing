# coding: utf-8
from . import db, BaseModel
from sqlalchemy.inspection import inspect


class UserInfo(BaseModel):
    __tablename__ = 'user_info'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False)
    profile_picture = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='头像')
    signature = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='个性签名')
    gender = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    phone = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'))
    date_of_birth = db.Column(db.DateTime)
    address = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))

    def to_dict(self):
        """将模型转换为字典"""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
