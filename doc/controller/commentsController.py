#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.comments import Comments
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class CommentsController(Comments):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        comment_id = GenerateID.create_random_id()
        
        try:
            model = Comments(
                comment_id=comment_id,
                user_id=kwargs.get('user_id'),
                comment_text=kwargs.get('comment_text'),
                commented_type=kwargs.get('commented_type'),
                commented_id=kwargs.get('commented_id'),
                parent_comment_id=kwargs.get('parent_comment_id'),
                likes=kwargs.get('likes'),
                replies=kwargs.get('replies'),
                timestamp=kwargs.get('timestamp'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'comment_id': model.comment_id,
                
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('comment_id'):
                filter_list.append(cls.comment_id == kwargs['comment_id'])
            else:
                if kwargs.get('user_id'):
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('comment_text'):
                    filter_list.append(cls.comment_text == kwargs.get('comment_text'))
                if kwargs.get('commented_type') is not None:
                    filter_list.append(cls.commented_type == kwargs.get('commented_type'))
                if kwargs.get('commented_id') is not None:
                    filter_list.append(cls.commented_id == kwargs.get('commented_id'))
                if kwargs.get('parent_comment_id') is not None:
                    filter_list.append(cls.parent_comment_id == kwargs.get('parent_comment_id'))
                if kwargs.get('likes'):
                    filter_list.append(cls.likes == kwargs.get('likes'))
                if kwargs.get('replies'):
                    filter_list.append(cls.replies == kwargs.get('replies'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            comments_info = db.session.query(cls).filter(*filter_list)
            
            count = comments_info.count()
            pages = math.ceil(count / size)
            comments_info = comments_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(comments_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}
            
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('comment_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('comment_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.comment_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('user_id'):
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('comment_text'):
                    filter_list.append(cls.comment_text == kwargs.get('comment_text'))
                if kwargs.get('commented_type') is not None:
                    filter_list.append(cls.commented_type == kwargs.get('commented_type'))
                if kwargs.get('commented_id') is not None:
                    filter_list.append(cls.commented_id == kwargs.get('commented_id'))
                if kwargs.get('parent_comment_id') is not None:
                    filter_list.append(cls.parent_comment_id == kwargs.get('parent_comment_id'))
                if kwargs.get('likes'):
                    filter_list.append(cls.likes == kwargs.get('likes'))
                if kwargs.get('replies'):
                    filter_list.append(cls.replies == kwargs.get('replies'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'comment_id': []
            }
            for query_model in res.all():
                results['comment_id'].append(query_model.comment_id)

            res.delete()
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            
            
            filter_list = []
            filter_list.append(cls.comment_id == kwargs.get('comment_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'comment_id': res.first().comment_id,
                
                }
                
                res.update(kwargs)
                db.session.commit()
            else:
                results = {
                    'error': 'data dose not exist'
                }
            
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = kwargs.get('CommentsList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            comment_id = GenerateID.create_random_id()
            
            model = Comments(
                comment_id=comment_id,
                user_id=param_dict.get('user_id'),
                comment_text=param_dict.get('comment_text'),
                commented_type=param_dict.get('commented_type'),
                commented_id=param_dict.get('commented_id'),
                parent_comment_id=param_dict.get('parent_comment_id'),
                likes=param_dict.get('likes'),
                replies=param_dict.get('replies'),
                timestamp=param_dict.get('timestamp'),
                
            )
            model_list.append(model)
        
        try:
            db.session.add_all(model_list)
            db.session.commit()
            results = {
                'added_records': [],
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for model in model_list:
                added_record = {}
                added_record['comment_id'] = model.comment_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
