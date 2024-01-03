#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import userinfo_blueprint
from api_1_0.userInfoResource.userInfoResource import UserInfoResource
from api_1_0.userInfoResource.userInfoOtherResource import UserInfoOtherResource

api = Api(userinfo_blueprint)

api.add_resource(UserInfoResource, '/userInfo/<user_id>', '/userInfo', endpoint='UserInfo')

