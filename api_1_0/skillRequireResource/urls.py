#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import skillrequire_blueprint
from api_1_0.skillRequireResource.skillRequireResource import SkillRequireResource
from api_1_0.skillRequireResource.skillRequireOtherResource import SkillRequireOtherResource

api = Api(skillrequire_blueprint)

api.add_resource(SkillRequireResource, '/skillRequire/<skill_id>', '/skillRequire', endpoint='SkillRequire')

