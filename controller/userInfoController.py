#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import datetime
import math
import json
import string

from sqlalchemy import or_

from app import db
from models.user_info import UserInfo
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from utils.generate_id import GenerateID


class UserInfoController(UserInfo):

    # add
    @classmethod
    def add(cls, **kwargs):

        user_id = GenerateID.create_random_id()
        
        try:
            model = UserInfo(
                user_id=user_id,
                user_name=kwargs.get('user_name'),
                profile_picture=kwargs.get('profile_picture'),
                signature=kwargs.get('signature'),
                gender=kwargs.get('gender'),
                phone=kwargs.get('phone'),
                date_of_birth=kwargs.get('date_of_birth'),
                address=kwargs.get('address'),
                
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

    # 用户授权手机号之后的处理
    @classmethod
    def create_or_update_user_from_wechat(cls, phone_number):
        try:
            user = cls.query.filter_by(phone=phone_number).first()
            if not user:
                # 如果用户不存在，创建新用户
                user_id = GenerateID.create_random_id()

                # 这里直接生成唯一用户名
                suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
                user_name = f"user_{phone_number[-4:]}_{suffix}"

                user = UserInfo(
                    user_id=user_id,
                    phone=phone_number,
                    user_name=user_name,
                    # 其他字段根据需要添加
                )
                db.session.add(user)
            else:
                # 如果用户已存在，可以更新信息
                # user.some_field = some_value
                pass
            db.session.commit()
            return {'code': RET.OK, 'message': 'User created/updated successfully', 'data': {'user_id': user.user_id}}
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': str(e), 'data': {}}

    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = []
            if kwargs.get('user_id'):
                filter_list.append(cls.user_id == kwargs['user_id'])
            else:
                if kwargs.get('user_name'):
                    filter_list.append(cls.user_name == kwargs.get('user_name'))
                if kwargs.get('profile_picture'):
                    filter_list.append(cls.profile_picture == kwargs.get('profile_picture'))
                if kwargs.get('signature'):
                    filter_list.append(cls.signature == kwargs.get('signature'))
                if kwargs.get('gender'):
                    filter_list.append(cls.gender == kwargs.get('gender'))
                if kwargs.get('phone'):
                    filter_list.append(cls.phone == kwargs.get('phone'))
                if kwargs.get('date_of_birth'):
                    filter_list.append(cls.date_of_birth == kwargs.get('date_of_birth'))
                if kwargs.get('address'):
                    filter_list.append(cls.address == kwargs.get('address'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            user_info_info = db.session.query(cls).filter(*filter_list)
            
            count = user_info_info.count()
            pages = math.ceil(count / size)
            user_info_info = user_info_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(user_info_info)
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
                if kwargs.get('user_name'):
                    filter_list.append(cls.user_name == kwargs.get('user_name'))
                if kwargs.get('profile_picture'):
                    filter_list.append(cls.profile_picture == kwargs.get('profile_picture'))
                if kwargs.get('signature'):
                    filter_list.append(cls.signature == kwargs.get('signature'))
                if kwargs.get('gender'):
                    filter_list.append(cls.gender == kwargs.get('gender'))
                if kwargs.get('phone'):
                    filter_list.append(cls.phone == kwargs.get('phone'))
                if kwargs.get('date_of_birth'):
                    filter_list.append(cls.date_of_birth == kwargs.get('date_of_birth'))
                if kwargs.get('address'):
                    filter_list.append(cls.address == kwargs.get('address'))
                
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
        param_list = kwargs.get('UserInfoList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            user_id = GenerateID.create_random_id()
            
            model = UserInfo(
                user_id=user_id,
                user_name=param_dict.get('user_name'),
                profile_picture=param_dict.get('profile_picture'),
                signature=param_dict.get('signature'),
                gender=param_dict.get('gender'),
                phone=param_dict.get('phone'),
                date_of_birth=param_dict.get('date_of_birth'),
                address=param_dict.get('address'),
                
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
