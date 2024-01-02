# coding: utf-8
from . import db, BaseModel


class Message(BaseModel):
    __tablename__ = 'message'

    message_id = db.Column(db.String(64, 'utf8mb4_0900_ai_ci'), primary_key=True)
    sender_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), info='发送者id')
    conversation_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), info='对话表id')
    receiver_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), info='接收者id')
    message_text = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='文字内容')
    image = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='图片')
    timestamp = db.Column(db.DateTime)
