#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.commentsController import CommentsController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class CommentsResource(Resource):

    # get
    @classmethod
    def get(cls, comment_id=None):
        if comment_id:
            kwargs = {
                'comment_id': comment_id
            }

            res = CommentsController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('comment_id', location='args', required=False, help='comment_id参数类型不正确或缺失')
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('comment_text', location='args', required=False, help='comment_text参数类型不正确或缺失')
        parser.add_argument('commented_type', location='args', required=False, help='commented_type参数类型不正确或缺失')
        parser.add_argument('commented_id', location='args', required=False, help='commented_id参数类型不正确或缺失')
        parser.add_argument('parent_comment_id', location='args', required=False, help='parent_comment_id参数类型不正确或缺失')
        parser.add_argument('likes', location='args', required=False, help='likes参数类型不正确或缺失')
        parser.add_argument('replies', location='args', required=False, help='replies参数类型不正确或缺失')
        parser.add_argument('timestamp', location='args', required=False, help='timestamp参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = CommentsController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    # delete
    @classmethod
    def delete(cls, comment_id=None):
        if comment_id:
            kwargs = {
                'comment_id': comment_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = CommentsController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, comment_id):
        if not comment_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('comment_text', location='form', required=False, help='comment_text参数类型不正确或缺失')
        parser.add_argument('commented_type', location='form', required=False, help='commented_type参数类型不正确或缺失')
        parser.add_argument('commented_id', location='form', required=False, help='commented_id参数类型不正确或缺失')
        parser.add_argument('parent_comment_id', location='form', required=False, help='parent_comment_id参数类型不正确或缺失')
        parser.add_argument('likes', location='form', required=False, help='likes参数类型不正确或缺失')
        parser.add_argument('replies', location='form', required=False, help='replies参数类型不正确或缺失')
        parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['comment_id'] = comment_id

        res = CommentsController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    def post(cls):
        '''
        CommentsList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('CommentsList', type=str, location='form', required=False, help='CommentsList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('CommentsList'):
            kwargs['CommentsList'] = json.loads(kwargs['CommentsList'])
            for data in kwargs['CommentsList']:
                for key in []:
                    data.pop(key, None)
            res = CommentsController.add_list(**kwargs)

        else:
            parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
            parser.add_argument('comment_text', location='form', required=False, help='comment_text参数类型不正确或缺失')
            parser.add_argument('commented_type', location='form', required=True, help='commented_type参数类型不正确或缺失')
            parser.add_argument('commented_id', location='form', required=True, help='commented_id参数类型不正确或缺失')
            parser.add_argument('parent_comment_id', location='form', required=False, help='parent_comment_id参数类型不正确或缺失')
            parser.add_argument('likes', location='form', required=False, help='likes参数类型不正确或缺失')
            parser.add_argument('replies', location='form', required=False, help='replies参数类型不正确或缺失')
            parser.add_argument('timestamp', location='form', required=False, help='timestamp参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = CommentsController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
