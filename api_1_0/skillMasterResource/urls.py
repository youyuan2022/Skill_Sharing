#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import skillmaster_blueprint
from api_1_0.skillMasterResource.skillMasterResource import SkillMasterResource
from api_1_0.skillMasterResource.skillMasterOtherResource import SkillMasterOtherResource

api = Api(skillmaster_blueprint)

api.add_resource(SkillMasterResource, '/skillMaster/<skill_id>', '/skillMaster', endpoint='SkillMaster')

