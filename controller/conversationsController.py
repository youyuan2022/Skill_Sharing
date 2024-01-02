#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.conversations import Conversations
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class ConversationsController(Conversations):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        conversation_id = GenerateID.create_random_id()
        
        try:
            model = Conversations(
                conversation_id=conversation_id,
                user1_id=kwargs.get('user1_id'),
                user2_id=kwargs.get('user2_id'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'conversation_id': model.conversation_id,
                
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
            if kwargs.get('conversation_id'):
                filter_list.append(cls.conversation_id == kwargs['conversation_id'])
            else:
                if kwargs.get('user1_id'):
                    filter_list.append(cls.user1_id == kwargs.get('user1_id'))
                if kwargs.get('user2_id'):
                    filter_list.append(cls.user2_id == kwargs.get('user2_id'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            conversations_info = db.session.query(cls).filter(*filter_list)
            
            count = conversations_info.count()
            pages = math.ceil(count / size)
            conversations_info = conversations_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(conversations_info)
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
            if kwargs.get('conversation_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('conversation_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.conversation_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('user1_id'):
                    filter_list.append(cls.user1_id == kwargs.get('user1_id'))
                if kwargs.get('user2_id'):
                    filter_list.append(cls.user2_id == kwargs.get('user2_id'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'conversation_id': []
            }
            for query_model in res.all():
                results['conversation_id'].append(query_model.conversation_id)

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
            filter_list.append(cls.conversation_id == kwargs.get('conversation_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'conversation_id': res.first().conversation_id,
                
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
        param_list = kwargs.get('ConversationsList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            conversation_id = GenerateID.create_random_id()
            
            model = Conversations(
                conversation_id=conversation_id,
                user1_id=param_dict.get('user1_id'),
                user2_id=param_dict.get('user2_id'),
                
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
                added_record['conversation_id'] = model.conversation_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
