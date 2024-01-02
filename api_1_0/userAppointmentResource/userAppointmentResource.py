#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.userAppointmentController import UserAppointmentController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class UserAppointmentResource(Resource):

    # get
    @classmethod
    def get(cls, appointment_id=None):
        if appointment_id:
            kwargs = {
                'appointment_id': appointment_id
            }

            res = UserAppointmentController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('appointment_id', location='args', required=False, help='appointment_id参数类型不正确或缺失')
        parser.add_argument('sender_id', location='args', required=False, help='sender_id参数类型不正确或缺失')
        parser.add_argument('receiver_id', location='args', required=False, help='receiver_id参数类型不正确或缺失')
        parser.add_argument('method', location='args', required=False, help='method参数类型不正确或缺失')
        parser.add_argument('appointment_time', location='args', required=False, help='appointment_time参数类型不正确或缺失')
        parser.add_argument('agree', location='args', required=False, help='agree参数类型不正确或缺失')
        parser.add_argument('timestamp', location='args', required=False, help='timestamp参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = UserAppointmentController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, appointment_id=None):
        if appointment_id:
            kwargs = {
                'appointment_id': appointment_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = UserAppointmentController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, appointment_id):
        if not appointment_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', location='form', required=False, help='sender_id参数类型不正确或缺失')
        parser.add_argument('receiver_id', location='form', required=False, help='receiver_id参数类型不正确或缺失')
        parser.add_argument('method', location='form', required=False, help='method参数类型不正确或缺失')
        parser.add_argument('appointment_time', location='form', required=False, help='appointment_time参数类型不正确或缺失')
        parser.add_argument('agree', location='form', required=False, help='agree参数类型不正确或缺失')
        parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['appointment_id'] = appointment_id

        res = UserAppointmentController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        UserAppointmentList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('UserAppointmentList', type=str, location='form', required=False, help='UserAppointmentList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('UserAppointmentList'):
            kwargs['UserAppointmentList'] = json.loads(kwargs['UserAppointmentList'])
            for data in kwargs['UserAppointmentList']:
                for key in []:
                    data.pop(key, None)
            res = UserAppointmentController.add_list(**kwargs)

        else:
            parser.add_argument('sender_id', location='form', required=True, help='sender_id参数类型不正确或缺失')
            parser.add_argument('receiver_id', location='form', required=False, help='receiver_id参数类型不正确或缺失')
            parser.add_argument('method', location='form', required=False, help='method参数类型不正确或缺失')
            parser.add_argument('appointment_time', location='form', required=False, help='appointment_time参数类型不正确或缺失')
            parser.add_argument('agree', location='form', required=False, help='agree参数类型不正确或缺失')
            parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = UserAppointmentController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
