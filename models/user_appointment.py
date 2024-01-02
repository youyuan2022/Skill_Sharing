# coding: utf-8
from . import db, BaseModel


class UserAppointment(BaseModel):
    __tablename__ = 'user_appointment'

    appointment_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True)
    sender_id = db.Column(db.String(0, 'utf8mb4_0900_ai_ci'), nullable=False, info='发送者id')
    receiver_id = db.Column(db.String(0, 'utf8mb4_0900_ai_ci'), info='接收者id')
    method = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='交换方法（线上，线下）')
    appointment_time = db.Column(db.DateTime, info='约定时间')
    agree = db.Column(db.Integer, info='状态：0未定，1同意，2拒绝')
    timestamp = db.Column(db.DateTime)
