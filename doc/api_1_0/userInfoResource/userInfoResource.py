#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from controller.userInfoController import UserInfoController
from utils import commons
from utils.response_code import RET, error_map_EN
import json

import http.client
import json
from flask import jsonify, request
from urllib.parse import urlencode

# 微信小程序的ID和密钥
APP_ID = 'wxe057749b1f26d808'
APP_SECRET = '501ce19bc2bfa6d6b7889ab28222660c'


class UserInfoResource(Resource):

    # get
    @classmethod
    def get(cls, user_id=None):
        if user_id:
            kwargs = {
                'user_id': user_id
            }

            res = UserInfoController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('user_name', location='args', required=False, help='user_name参数类型不正确或缺失')
        parser.add_argument('profile_picture', location='args', required=False,
                            help='profile_picture参数类型不正确或缺失')
        parser.add_argument('signature', location='args', required=False, help='signature参数类型不正确或缺失')
        parser.add_argument('gender', location='args', required=False, help='gender参数类型不正确或缺失')
        parser.add_argument('phone', location='args', required=False, help='phone参数类型不正确或缺失')
        parser.add_argument('date_of_birth', location='args', required=False, help='date_of_birth参数类型不正确或缺失')
        parser.add_argument('address', location='args', required=False, help='address参数类型不正确或缺失')

        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = UserInfoController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'],
                           totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])

            # delete

    @classmethod
    def delete(cls, user_id=None):
        if user_id:
            kwargs = {
                'user_id': user_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = UserInfoController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, user_id):
        if not user_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='form', required=False, help='user_name参数类型不正确或缺失')
        # parser.add_argument('profile_picture', location='form', required=False,
        #                     help='profile_picture参数类型不正确或缺失')
        parser.add_argument('signature', location='form', required=False, help='signature参数类型不正确或缺失')
        parser.add_argument('gender', location='form', required=False, help='gender参数类型不正确或缺失')
        parser.add_argument('phone', location='form', required=False, help='phone参数类型不正确或缺失')
        parser.add_argument('date_of_birth', location='form', required=False, help='date_of_birth参数类型不正确或缺失')
        parser.add_argument('address', location='form', required=False, help='address参数类型不正确或缺失')

        args = parser.parse_args()

        # 处理图片上传
        if 'profile_picture' in request.files:
            file = request.files.get('profile_picture')
            avatar_url = UserInfoController.upload_avatar(file)
            args['profile_picture'] = avatar_url

        kwargs = commons.put_remove_none(**args)
        kwargs['user_id'] = user_id

        res = UserInfoController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # POST 方法
    @classmethod
    def post(cls):
        content_type = request.headers.get('Content-Type')

        if content_type == 'application/json':
            json_data = request.get_json(silent=True)
            if json_data and 'code' in json_data:
                code = json_data['code']

                # 使用 http.client 获取 access_token
                conn = http.client.HTTPSConnection("api.weixin.qq.com")
                params = urlencode({'grant_type': 'client_credential', 'appid': APP_ID, 'secret': APP_SECRET})
                conn.request("GET", "/cgi-bin/token?" + params)
                token_response = conn.getresponse()

                if token_response.status == 200:
                    token_data = json.loads(token_response.read())
                    access_token = token_data.get('access_token')

                    # 使用 access_token 和 code 获取用户手机号
                    conn.request("POST", "/wxa/business/getuserphonenumber?access_token=" + access_token,
                                 body=json.dumps({"code": code}), headers={"Content-Type": "application/json"})
                    phone_response = conn.getresponse()

                    if phone_response.status == 200:
                        phone_info = json.loads(phone_response.read())
                        phone_number = phone_info.get('phone_info', {}).get('purePhoneNumber')

                        # 调用 UserInfoController 的方法处理用户数据
                        res = UserInfoController.create_or_update_user_from_wechat(phone_number)
                        return jsonify(res)
                    else:
                        return jsonify({'error': 'Failed to get phone number from WeChat'}), phone_response.status
                else:
                    return jsonify({'error': 'Failed to get access token from WeChat'}), token_response.status

        else:
            # 处理表单数据的请求
            parser = reqparse.RequestParser()
            parser.add_argument('user_name', location='form', required=True, help='user_name参数类型不正确或缺失')
            parser.add_argument('profile_picture', location='form', required=False,
                                help='profile_picture参数类型不正确或缺失')
            parser.add_argument('signature', location='form', required=False, help='signature参数类型不正确或缺失')
            parser.add_argument('gender', location='form', required=False, help='gender参数类型不正确或缺失')
            parser.add_argument('phone', location='form', required=False, help='phone参数类型不正确或缺失')
            parser.add_argument('date_of_birth', location='form', required=False,
                                help='date_of_birth参数类型不正确或缺失')
            parser.add_argument('address', location='form', required=False, help='address参数类型不正确或缺失')

            # 解析表单数据
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            # 调用控制器方法处理表单数据
            res = UserInfoController.add(**kwargs)
            return jsonify(res)

        return jsonify({'message': 'Invalid request'}), 400

