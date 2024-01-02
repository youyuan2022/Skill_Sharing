#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import comments_blueprint
from api_1_0.commentsResource.commentsResource import CommentsResource
from api_1_0.commentsResource.commentsOtherResource import CommentsOtherResource

api = Api(comments_blueprint)

api.add_resource(CommentsResource, '/comments/<comment_id>', '/comments', endpoint='Comments')

