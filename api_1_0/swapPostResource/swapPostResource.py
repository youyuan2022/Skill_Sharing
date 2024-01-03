#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.swapPostController import SwapPostController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class SwapPostResource(Resource):

    # get
    @classmethod
    def get(cls, swap_post_id=None):
        if swap_post_id:
            kwargs = {
                'swap_post_id': swap_post_id
            }

            res = SwapPostController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('swap_post_id', location='args', required=False, help='swap_post_id参数类型不正确或缺失')
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('swap_method', location='args', required=False, help='swap_method参数类型不正确或缺失')
        parser.add_argument('post_text', location='args', required=False, help='post_text参数类型不正确或缺失')
        parser.add_argument('images', location='args', required=False, help='images参数类型不正确或缺失')
        parser.add_argument('appointment_time', location='args', required=False, help='appointment_time参数类型不正确或缺失')
        parser.add_argument('likes', location='args', required=False, help='likes参数类型不正确或缺失')
        parser.add_argument('comments', location='args', required=False, help='comments参数类型不正确或缺失')
        parser.add_argument('timestamp', location='args', required=False, help='timestamp参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = SwapPostController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, swap_post_id=None):
        if swap_post_id:
            kwargs = {
                'swap_post_id': swap_post_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = SwapPostController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, swap_post_id):
        if not swap_post_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('swap_method', location='form', required=False, help='swap_method参数类型不正确或缺失')
        parser.add_argument('post_text', location='form', required=False, help='post_text参数类型不正确或缺失')
        parser.add_argument('images', location='form', required=False, help='images参数类型不正确或缺失')
        parser.add_argument('appointment_time', location='form', required=False, help='appointment_time参数类型不正确或缺失')
        parser.add_argument('likes', location='form', required=False, help='likes参数类型不正确或缺失')
        parser.add_argument('comments', location='form', required=False, help='comments参数类型不正确或缺失')
        parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['swap_post_id'] = swap_post_id

        res = SwapPostController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        SwapPostList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('SwapPostList', type=str, location='form', required=False, help='SwapPostList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('SwapPostList'):
            kwargs['SwapPostList'] = json.loads(kwargs['SwapPostList'])
            for data in kwargs['SwapPostList']:
                for key in []:
                    data.pop(key, None)
            res = SwapPostController.add_list(**kwargs)

        else:
            parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
            parser.add_argument('swap_method', location='form', required=False, help='swap_method参数类型不正确或缺失')
            parser.add_argument('post_text', location='form', required=False, help='post_text参数类型不正确或缺失')
            parser.add_argument('images', location='form', required=False, help='images参数类型不正确或缺失')
            parser.add_argument('appointment_time', location='form', required=False, help='appointment_time参数类型不正确或缺失')
            parser.add_argument('likes', location='form', required=False, help='likes参数类型不正确或缺失')
            parser.add_argument('comments', location='form', required=False, help='comments参数类型不正确或缺失')
            parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = SwapPostController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
