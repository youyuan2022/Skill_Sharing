#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.likes import Likes
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class LikesController(Likes):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        like_id = GenerateID.create_random_id()
        
        try:
            model = Likes(
                like_id=like_id,
                user_id=kwargs.get('user_id'),
                liked_type=kwargs.get('liked_type'),
                liked_id=kwargs.get('liked_id'),
                timestamp=kwargs.get('timestamp'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'like_id': model.like_id,
                
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
            if kwargs.get('like_id'):
                filter_list.append(cls.like_id == kwargs['like_id'])
            else:
                if kwargs.get('user_id'):
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('liked_type') is not None:
                    filter_list.append(cls.liked_type == kwargs.get('liked_type'))
                if kwargs.get('liked_id'):
                    filter_list.append(cls.liked_id == kwargs.get('liked_id'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            likes_info = db.session.query(cls).filter(*filter_list)
            
            count = likes_info.count()
            pages = math.ceil(count / size)
            likes_info = likes_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(likes_info)
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
            if kwargs.get('like_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('like_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.like_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('user_id'):
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('liked_type') is not None:
                    filter_list.append(cls.liked_type == kwargs.get('liked_type'))
                if kwargs.get('liked_id'):
                    filter_list.append(cls.liked_id == kwargs.get('liked_id'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'like_id': []
            }
            for query_model in res.all():
                results['like_id'].append(query_model.like_id)

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
            filter_list.append(cls.like_id == kwargs.get('like_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'like_id': res.first().like_id,
                
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
        param_list = kwargs.get('LikesList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            like_id = GenerateID.create_random_id()
            
            model = Likes(
                like_id=like_id,
                user_id=param_dict.get('user_id'),
                liked_type=param_dict.get('liked_type'),
                liked_id=param_dict.get('liked_id'),
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
                added_record['like_id'] = model.like_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
