#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.swap_post import SwapPost
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class SwapPostController(SwapPost):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        swap_post_id = GenerateID.create_random_id()
        
        try:
            model = SwapPost(
                swap_post_id=swap_post_id,
                user_id=kwargs.get('user_id'),
                swap_method=kwargs.get('swap_method'),
                post_text=kwargs.get('post_text'),
                images=kwargs.get('images'),
                appointment_time=kwargs.get('appointment_time'),
                likes=kwargs.get('likes'),
                comments=kwargs.get('comments'),
                timestamp=kwargs.get('timestamp'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'swap_post_id': model.swap_post_id,
                
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
            if kwargs.get('swap_post_id'):
                filter_list.append(cls.swap_post_id == kwargs['swap_post_id'])
            else:
                if kwargs.get('user_id'):
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('swap_method'):
                    filter_list.append(cls.swap_method == kwargs.get('swap_method'))
                if kwargs.get('post_text'):
                    filter_list.append(cls.post_text == kwargs.get('post_text'))
                if kwargs.get('images'):
                    filter_list.append(cls.images == kwargs.get('images'))
                if kwargs.get('appointment_time'):
                    filter_list.append(cls.appointment_time == kwargs.get('appointment_time'))
                if kwargs.get('likes') is not None:
                    filter_list.append(cls.likes == kwargs.get('likes'))
                if kwargs.get('comments') is not None:
                    filter_list.append(cls.comments == kwargs.get('comments'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            swap_post_info = db.session.query(cls).filter(*filter_list)
            
            count = swap_post_info.count()
            pages = math.ceil(count / size)
            swap_post_info = swap_post_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(swap_post_info)
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
            if kwargs.get('swap_post_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('swap_post_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.swap_post_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('user_id'):
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('swap_method'):
                    filter_list.append(cls.swap_method == kwargs.get('swap_method'))
                if kwargs.get('post_text'):
                    filter_list.append(cls.post_text == kwargs.get('post_text'))
                if kwargs.get('images'):
                    filter_list.append(cls.images == kwargs.get('images'))
                if kwargs.get('appointment_time'):
                    filter_list.append(cls.appointment_time == kwargs.get('appointment_time'))
                if kwargs.get('likes') is not None:
                    filter_list.append(cls.likes == kwargs.get('likes'))
                if kwargs.get('comments') is not None:
                    filter_list.append(cls.comments == kwargs.get('comments'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'swap_post_id': []
            }
            for query_model in res.all():
                results['swap_post_id'].append(query_model.swap_post_id)

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
            filter_list.append(cls.swap_post_id == kwargs.get('swap_post_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'swap_post_id': res.first().swap_post_id,
                
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
        param_list = kwargs.get('SwapPostList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            swap_post_id = GenerateID.create_random_id()
            
            model = SwapPost(
                swap_post_id=swap_post_id,
                user_id=param_dict.get('user_id'),
                swap_method=param_dict.get('swap_method'),
                post_text=param_dict.get('post_text'),
                images=param_dict.get('images'),
                appointment_time=param_dict.get('appointment_time'),
                likes=param_dict.get('likes'),
                comments=param_dict.get('comments'),
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
                added_record['swap_post_id'] = model.swap_post_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
