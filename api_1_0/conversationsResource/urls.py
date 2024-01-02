#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import conversations_blueprint
from api_1_0.conversationsResource.conversationsResource import ConversationsResource
from api_1_0.conversationsResource.conversationsOtherResource import ConversationsOtherResource

api = Api(conversations_blueprint)

api.add_resource(ConversationsResource, '/conversations/<conversation_id>', '/conversations', endpoint='Conversations')

