#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import swappost_blueprint
from api_1_0.swapPostResource.swapPostResource import SwapPostResource
from api_1_0.swapPostResource.swapPostOtherResource import SwapPostOtherResource

api = Api(swappost_blueprint)

api.add_resource(SwapPostResource, '/swapPost/<swap_post_id>', '/swapPost', endpoint='SwapPost')

