# coding: utf-8
from . import db, BaseModel

from .users import Users




class Conversations(BaseModel):
    __tablename__ = 'conversations'

    conversation_id = db.Column(db.String(32, 'utf8mb4_0900_ai_ci'), primary_key=True, info='对话表')
    user1_id = db.Column(db.ForeignKey('users.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, info='用户1')
    user2_id = db.Column(db.ForeignKey('users.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, info='用户2')

    user1 = db.relationship('Users', primaryjoin='Conversations.user1_id == Users.user_id', backref='users_conversationss')
    user2 = db.relationship('Users', primaryjoin='Conversations.user2_id == Users.user_id', backref='users_conversationss_0')
