#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.skillMasterController import SkillMasterController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class SkillMasterResource(Resource):

    # get
    @classmethod
    def get(cls, skill_id=None):
        if skill_id:
            kwargs = {
                'skill_id': skill_id
            }

            res = SkillMasterController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('skill_id', location='args', required=False, help='skill_id参数类型不正确或缺失')
        parser.add_argument('skill_name', location='args', required=False, help='skill_name参数类型不正确或缺失')
        parser.add_argument('parent_type', location='args', required=False, help='parent_type参数类型不正确或缺失')
        parser.add_argument('parent_id', location='args', required=False, help='parent_id参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = SkillMasterController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, skill_id=None):
        if skill_id:
            kwargs = {
                'skill_id': skill_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = SkillMasterController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, skill_id):
        if not skill_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('skill_name', location='form', required=False, help='skill_name参数类型不正确或缺失')
        parser.add_argument('parent_type', location='form', required=False, help='parent_type参数类型不正确或缺失')
        parser.add_argument('parent_id', location='form', required=False, help='parent_id参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['skill_id'] = skill_id

        res = SkillMasterController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        SkillMasterList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('SkillMasterList', type=str, location='form', required=False, help='SkillMasterList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('SkillMasterList'):
            kwargs['SkillMasterList'] = json.loads(kwargs['SkillMasterList'])
            for data in kwargs['SkillMasterList']:
                for key in []:
                    data.pop(key, None)
            res = SkillMasterController.add_list(**kwargs)

        else:
            parser.add_argument('skill_name', location='form', required=False, help='skill_name参数类型不正确或缺失')
            parser.add_argument('parent_type', location='form', required=False, help='parent_type参数类型不正确或缺失')
            parser.add_argument('parent_id', location='form', required=False, help='parent_id参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = SkillMasterController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
