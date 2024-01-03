#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.userFollowController import UserFollowController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class UserFollowResource(Resource):

    # get
    @classmethod
    def get(cls, follow_id=None):
        if follow_id:
            kwargs = {
                'follow_id': follow_id
            }

            res = UserFollowController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('follow_id', location='args', required=False, help='follow_id参数类型不正确或缺失')
        parser.add_argument('follower_id', location='args', required=False, help='follower_id参数类型不正确或缺失')
        parser.add_argument('followee_id', location='args', required=False, help='followee_id参数类型不正确或缺失')
        parser.add_argument('follow_date', location='args', required=False, help='follow_date参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = UserFollowController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, follow_id=None):
        if follow_id:
            kwargs = {
                'follow_id': follow_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = UserFollowController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, follow_id):
        if not follow_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('follower_id', location='form', required=False, help='follower_id参数类型不正确或缺失')
        parser.add_argument('followee_id', location='form', required=False, help='followee_id参数类型不正确或缺失')
        parser.add_argument('follow_date', location='form', required=False, help='follow_date参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['follow_id'] = follow_id

        res = UserFollowController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        UserFollowList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('UserFollowList', type=str, location='form', required=False, help='UserFollowList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('UserFollowList'):
            kwargs['UserFollowList'] = json.loads(kwargs['UserFollowList'])
            for data in kwargs['UserFollowList']:
                for key in []:
                    data.pop(key, None)
            res = UserFollowController.add_list(**kwargs)

        else:
            parser.add_argument('follower_id', location='form', required=True, help='follower_id参数类型不正确或缺失')
            parser.add_argument('followee_id', location='form', required=False, help='followee_id参数类型不正确或缺失')
            parser.add_argument('follow_date', location='form', required=False, help='follow_date参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = UserFollowController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
