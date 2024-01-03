#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import likes_blueprint
from api_1_0.likesResource.likesResource import LikesResource
from api_1_0.likesResource.likesOtherResource import LikesOtherResource

api = Api(likes_blueprint)

api.add_resource(LikesResource, '/likes/<like_id>', '/likes', endpoint='Likes')

