#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.users import Users
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class UsersController(Users):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        user_id = GenerateID.create_random_id()
        
        try:
            model = Users(
                user_id=user_id,
                password=kwargs.get('password'),
                status=kwargs.get('status'),
                wx_openid=kwargs.get('wx_openid'),
                role=kwargs.get('role'),
                registration_time=kwargs.get('registration_time'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user_id': model.user_id,
                
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
            if kwargs.get('user_id'):
                filter_list.append(cls.user_id == kwargs['user_id'])
            else:
                if kwargs.get('password'):
                    filter_list.append(cls.password == kwargs.get('password'))
                if kwargs.get('status') is not None:
                    filter_list.append(cls.status == kwargs.get('status'))
                if kwargs.get('wx_openid'):
                    filter_list.append(cls.wx_openid == kwargs.get('wx_openid'))
                if kwargs.get('role') is not None:
                    filter_list.append(cls.role == kwargs.get('role'))
                if kwargs.get('registration_time'):
                    filter_list.append(cls.registration_time == kwargs.get('registration_time'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            users_info = db.session.query(cls).filter(*filter_list)
            
            count = users_info.count()
            pages = math.ceil(count / size)
            users_info = users_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(users_info)
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
            if kwargs.get('user_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('user_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.user_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('password'):
                    filter_list.append(cls.password == kwargs.get('password'))
                if kwargs.get('status') is not None:
                    filter_list.append(cls.status == kwargs.get('status'))
                if kwargs.get('wx_openid'):
                    filter_list.append(cls.wx_openid == kwargs.get('wx_openid'))
                if kwargs.get('role') is not None:
                    filter_list.append(cls.role == kwargs.get('role'))
                if kwargs.get('registration_time'):
                    filter_list.append(cls.registration_time == kwargs.get('registration_time'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user_id': []
            }
            for query_model in res.all():
                results['user_id'].append(query_model.user_id)

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
            filter_list.append(cls.user_id == kwargs.get('user_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'user_id': res.first().user_id,
                
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
        param_list = kwargs.get('UsersList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            user_id = GenerateID.create_random_id()
            
            model = Users(
                user_id=user_id,
                password=param_dict.get('password'),
                status=param_dict.get('status'),
                wx_openid=param_dict.get('wx_openid'),
                role=param_dict.get('role'),
                registration_time=param_dict.get('registration_time'),
                
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
                added_record['user_id'] = model.user_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
