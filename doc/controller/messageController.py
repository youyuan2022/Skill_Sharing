#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.message import Message
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class MessageController(Message):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        message_id = GenerateID.create_random_id()
        
        try:
            model = Message(
                message_id=message_id,
                sender_id=kwargs.get('sender_id'),
                conversation_id=kwargs.get('conversation_id'),
                receiver_id=kwargs.get('receiver_id'),
                message_text=kwargs.get('message_text'),
                image=kwargs.get('image'),
                timestamp=kwargs.get('timestamp'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message_id': model.message_id,
                
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
            if kwargs.get('message_id'):
                filter_list.append(cls.message_id == kwargs['message_id'])
            else:
                if kwargs.get('sender_id'):
                    filter_list.append(cls.sender_id == kwargs.get('sender_id'))
                if kwargs.get('conversation_id'):
                    filter_list.append(cls.conversation_id == kwargs.get('conversation_id'))
                if kwargs.get('receiver_id'):
                    filter_list.append(cls.receiver_id == kwargs.get('receiver_id'))
                if kwargs.get('message_text'):
                    filter_list.append(cls.message_text == kwargs.get('message_text'))
                if kwargs.get('image'):
                    filter_list.append(cls.image == kwargs.get('image'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            message_info = db.session.query(cls).filter(*filter_list)
            
            count = message_info.count()
            pages = math.ceil(count / size)
            message_info = message_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(message_info)
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
            if kwargs.get('message_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('message_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.message_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('sender_id'):
                    filter_list.append(cls.sender_id == kwargs.get('sender_id'))
                if kwargs.get('conversation_id'):
                    filter_list.append(cls.conversation_id == kwargs.get('conversation_id'))
                if kwargs.get('receiver_id'):
                    filter_list.append(cls.receiver_id == kwargs.get('receiver_id'))
                if kwargs.get('message_text'):
                    filter_list.append(cls.message_text == kwargs.get('message_text'))
                if kwargs.get('image'):
                    filter_list.append(cls.image == kwargs.get('image'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message_id': []
            }
            for query_model in res.all():
                results['message_id'].append(query_model.message_id)

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
            filter_list.append(cls.message_id == kwargs.get('message_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'message_id': res.first().message_id,
                
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
        param_list = kwargs.get('MessageList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            message_id = GenerateID.create_random_id()
            
            model = Message(
                message_id=message_id,
                sender_id=param_dict.get('sender_id'),
                conversation_id=param_dict.get('conversation_id'),
                receiver_id=param_dict.get('receiver_id'),
                message_text=param_dict.get('message_text'),
                image=param_dict.get('image'),
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
                added_record['message_id'] = model.message_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
