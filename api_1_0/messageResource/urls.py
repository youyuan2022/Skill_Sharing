#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import message_blueprint
from api_1_0.messageResource.messageResource import MessageResource
from api_1_0.messageResource.messageOtherResource import MessageOtherResource

api = Api(message_blueprint)

api.add_resource(MessageResource, '/message/<message_id>', '/message', endpoint='Message')

