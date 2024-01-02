#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.likesController import LikesController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class LikesResource(Resource):

    # get
    @classmethod
    def get(cls, like_id=None):
        if like_id:
            kwargs = {
                'like_id': like_id
            }

            res = LikesController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('like_id', location='args', required=False, help='like_id参数类型不正确或缺失')
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('liked_type', location='args', required=False, help='liked_type参数类型不正确或缺失')
        parser.add_argument('liked_id', location='args', required=False, help='liked_id参数类型不正确或缺失')
        parser.add_argument('timestamp', location='args', required=False, help='timestamp参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = LikesController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, like_id=None):
        if like_id:
            kwargs = {
                'like_id': like_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = LikesController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, like_id):
        if not like_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('liked_type', location='form', required=False, help='liked_type参数类型不正确或缺失')
        parser.add_argument('liked_id', location='form', required=False, help='liked_id参数类型不正确或缺失')
        parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['like_id'] = like_id

        res = LikesController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        LikesList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('LikesList', type=str, location='form', required=False, help='LikesList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('LikesList'):
            kwargs['LikesList'] = json.loads(kwargs['LikesList'])
            for data in kwargs['LikesList']:
                for key in []:
                    data.pop(key, None)
            res = LikesController.add_list(**kwargs)

        else:
            parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
            parser.add_argument('liked_type', location='form', required=False, help='liked_type参数类型不正确或缺失')
            parser.add_argument('liked_id', location='form', required=False, help='liked_id参数类型不正确或缺失')
            parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = LikesController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
