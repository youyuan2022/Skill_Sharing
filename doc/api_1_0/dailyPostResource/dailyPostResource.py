#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify, request

from controller.dailyPostController import DailyPostController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class DailyPostResource(Resource):

    # get
    @classmethod
    def get(cls, daily_post_id=None):
        if daily_post_id:
            kwargs = {
                'daily_post_id': daily_post_id
            }

            res = DailyPostController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('daily_post_id', location='args', required=False, help='daily_post_id参数类型不正确或缺失')
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('post_title', location='args', required=False, help='post_title参数类型不正确或缺失')
        parser.add_argument('post_text', location='args', required=False, help='post_text参数类型不正确或缺失')
        parser.add_argument('images', location='args', required=False, help='images参数类型不正确或缺失')
        parser.add_argument('topic', location='args', required=False, help='topic参数类型不正确或缺失')
        parser.add_argument('timestamp', location='args', required=False, help='timestamp参数类型不正确或缺失')
        parser.add_argument('likes', location='args', required=False, help='likes参数类型不正确或缺失')
        parser.add_argument('comments', location='args', required=False, help='comments参数类型不正确或缺失')

        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = DailyPostController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'],
                           totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])

            # delete

    @classmethod
    def delete(cls, daily_post_id=None):
        if daily_post_id:
            kwargs = {
                'daily_post_id': daily_post_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = DailyPostController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, daily_post_id):
        if not daily_post_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('post_title', location='form', required=False, help='post_title参数类型不正确或缺失')
        parser.add_argument('post_text', location='form', required=False, help='post_text参数类型不正确或缺失')
        parser.add_argument('images', location='form', required=False, help='images参数类型不正确或缺失')
        parser.add_argument('topic', location='form', required=False, help='topic参数类型不正确或缺失')
        parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
        parser.add_argument('likes', location='form', required=False, help='likes参数类型不正确或缺失')
        parser.add_argument('comments', location='form', required=False, help='comments参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['daily_post_id'] = daily_post_id

        res = DailyPostController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        print("1")
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='form', required=False)
        parser.add_argument('post_title', location='form', required=True)
        parser.add_argument('post_text', location='form', required=True)
        parser.add_argument('topic', location='form', required=False)
        parser.add_argument('timestamp', location='form', required=False)
        # parser.add_argument('likes', location='form', required=False)
        # parser.add_argument('comments', location='form', required=False)

        # 在这里你不需要解析 images，因为它们来自于文件上传
        # parser.add_argument('images', location='form', required=False)

        args = parser.parse_args()

        # 处理图片上传
        if 'images' in request.files:
            files = request.files.getlist('images')
            image_urls = DailyPostController.upload_images(files)
            args['images'] = image_urls

        # 调用控制器方法添加帖子
        res = DailyPostController.add(**args)

        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])