#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import dailypost_blueprint
from api_1_0.dailyPostResource.dailyPostResource import DailyPostResource
from api_1_0.dailyPostResource.dailyPostOtherResource import DailyPostOtherResource

api = Api(dailypost_blueprint)

api.add_resource(DailyPostResource, '/dailyPost/<daily_post_id>', '/dailyPost', endpoint='DailyPost')

