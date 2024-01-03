#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.conversationsController import ConversationsController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class ConversationsResource(Resource):

    # get
    @classmethod
    def get(cls, conversation_id=None):
        if conversation_id:
            kwargs = {
                'conversation_id': conversation_id
            }

            res = ConversationsController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('conversation_id', location='args', required=False, help='conversation_id参数类型不正确或缺失')
        parser.add_argument('user1_id', location='args', required=False, help='user1_id参数类型不正确或缺失')
        parser.add_argument('user2_id', location='args', required=False, help='user2_id参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = ConversationsController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, conversation_id=None):
        if conversation_id:
            kwargs = {
                'conversation_id': conversation_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = ConversationsController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, conversation_id):
        if not conversation_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('user1_id', location='form', required=False, help='user1_id参数类型不正确或缺失')
        parser.add_argument('user2_id', location='form', required=False, help='user2_id参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['conversation_id'] = conversation_id

        res = ConversationsController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        ConversationsList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('ConversationsList', type=str, location='form', required=False, help='ConversationsList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('ConversationsList'):
            kwargs['ConversationsList'] = json.loads(kwargs['ConversationsList'])
            for data in kwargs['ConversationsList']:
                for key in []:
                    data.pop(key, None)
            res = ConversationsController.add_list(**kwargs)

        else:
            parser.add_argument('user1_id', location='form', required=False, help='user1_id参数类型不正确或缺失')
            parser.add_argument('user2_id', location='form', required=False, help='user2_id参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = ConversationsController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
