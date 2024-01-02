# coding: utf-8
from . import db, BaseModel


class SkillRequire(BaseModel):
    __tablename__ = 'skill_require'

    skill_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True)
    skill_name = db.Column(db.String(64, 'utf8mb4_0900_ai_ci'))
    parent_type = db.Column(db.Integer, info='1.swap_post 2.user_appointment')
    parent_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'))
