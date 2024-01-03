#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.user_appointment import UserAppointment
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class UserAppointmentController(UserAppointment):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        appointment_id = GenerateID.create_random_id()
        
        try:
            model = UserAppointment(
                appointment_id=appointment_id,
                sender_id=kwargs.get('sender_id'),
                receiver_id=kwargs.get('receiver_id'),
                method=kwargs.get('method'),
                appointment_time=kwargs.get('appointment_time'),
                agree=kwargs.get('agree'),
                timestamp=kwargs.get('timestamp'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'appointment_id': model.appointment_id,
                
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
            if kwargs.get('appointment_id'):
                filter_list.append(cls.appointment_id == kwargs['appointment_id'])
            else:
                if kwargs.get('sender_id'):
                    filter_list.append(cls.sender_id == kwargs.get('sender_id'))
                if kwargs.get('receiver_id'):
                    filter_list.append(cls.receiver_id == kwargs.get('receiver_id'))
                if kwargs.get('method'):
                    filter_list.append(cls.method == kwargs.get('method'))
                if kwargs.get('appointment_time'):
                    filter_list.append(cls.appointment_time == kwargs.get('appointment_time'))
                if kwargs.get('agree') is not None:
                    filter_list.append(cls.agree == kwargs.get('agree'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            user_appointment_info = db.session.query(cls).filter(*filter_list)
            
            count = user_appointment_info.count()
            pages = math.ceil(count / size)
            user_appointment_info = user_appointment_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(user_appointment_info)
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
            if kwargs.get('appointment_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('appointment_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.appointment_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('sender_id'):
                    filter_list.append(cls.sender_id == kwargs.get('sender_id'))
                if kwargs.get('receiver_id'):
                    filter_list.append(cls.receiver_id == kwargs.get('receiver_id'))
                if kwargs.get('method'):
                    filter_list.append(cls.method == kwargs.get('method'))
                if kwargs.get('appointment_time'):
                    filter_list.append(cls.appointment_time == kwargs.get('appointment_time'))
                if kwargs.get('agree') is not None:
                    filter_list.append(cls.agree == kwargs.get('agree'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'appointment_id': []
            }
            for query_model in res.all():
                results['appointment_id'].append(query_model.appointment_id)

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
            filter_list.append(cls.appointment_id == kwargs.get('appointment_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'appointment_id': res.first().appointment_id,
                
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
        param_list = kwargs.get('UserAppointmentList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            appointment_id = GenerateID.create_random_id()
            
            model = UserAppointment(
                appointment_id=appointment_id,
                sender_id=param_dict.get('sender_id'),
                receiver_id=param_dict.get('receiver_id'),
                method=param_dict.get('method'),
                appointment_time=param_dict.get('appointment_time'),
                agree=param_dict.get('agree'),
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
                added_record['appointment_id'] = model.appointment_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
