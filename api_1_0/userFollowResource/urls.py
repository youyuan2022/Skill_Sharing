#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import userfollow_blueprint
from api_1_0.userFollowResource.userFollowResource import UserFollowResource
from api_1_0.userFollowResource.userFollowOtherResource import UserFollowOtherResource

api = Api(userfollow_blueprint)

api.add_resource(UserFollowResource, '/userFollow/<follow_id>', '/userFollow', endpoint='UserFollow')

