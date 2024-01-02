#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.user_follow import UserFollow
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class UserFollowController(UserFollow):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        follow_id = GenerateID.create_random_id()
        
        try:
            model = UserFollow(
                follow_id=follow_id,
                follower_id=kwargs.get('follower_id'),
                followee_id=kwargs.get('followee_id'),
                follow_date=kwargs.get('follow_date'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'follow_id': model.follow_id,
                
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
            if kwargs.get('follow_id'):
                filter_list.append(cls.follow_id == kwargs['follow_id'])
            else:
                if kwargs.get('follower_id'):
                    filter_list.append(cls.follower_id == kwargs.get('follower_id'))
                if kwargs.get('followee_id'):
                    filter_list.append(cls.followee_id == kwargs.get('followee_id'))
                if kwargs.get('follow_date'):
                    filter_list.append(cls.follow_date == kwargs.get('follow_date'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            user_follow_info = db.session.query(cls).filter(*filter_list)
            
            count = user_follow_info.count()
            pages = math.ceil(count / size)
            user_follow_info = user_follow_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(user_follow_info)
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
            if kwargs.get('follow_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('follow_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.follow_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('follower_id'):
                    filter_list.append(cls.follower_id == kwargs.get('follower_id'))
                if kwargs.get('followee_id'):
                    filter_list.append(cls.followee_id == kwargs.get('followee_id'))
                if kwargs.get('follow_date'):
                    filter_list.append(cls.follow_date == kwargs.get('follow_date'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'follow_id': []
            }
            for query_model in res.all():
                results['follow_id'].append(query_model.follow_id)

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
            filter_list.append(cls.follow_id == kwargs.get('follow_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'follow_id': res.first().follow_id,
                
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
        param_list = kwargs.get('UserFollowList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            follow_id = GenerateID.create_random_id()
            
            model = UserFollow(
                follow_id=follow_id,
                follower_id=param_dict.get('follower_id'),
                followee_id=param_dict.get('followee_id'),
                follow_date=param_dict.get('follow_date'),
                
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
                added_record['follow_id'] = model.follow_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
