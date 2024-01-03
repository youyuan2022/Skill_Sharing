#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.skill_master import SkillMaster
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class SkillMasterController(SkillMaster):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        skill_id = GenerateID.create_random_id()
        
        try:
            model = SkillMaster(
                skill_id=skill_id,
                skill_name=kwargs.get('skill_name'),
                parent_type=kwargs.get('parent_type'),
                parent_id=kwargs.get('parent_id'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'skill_id': model.skill_id,
                
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
            if kwargs.get('skill_id'):
                filter_list.append(cls.skill_id == kwargs['skill_id'])
            else:
                if kwargs.get('skill_name'):
                    filter_list.append(cls.skill_name == kwargs.get('skill_name'))
                if kwargs.get('parent_type') is not None:
                    filter_list.append(cls.parent_type == kwargs.get('parent_type'))
                if kwargs.get('parent_id'):
                    filter_list.append(cls.parent_id == kwargs.get('parent_id'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            skill_master_info = db.session.query(cls).filter(*filter_list)
            
            count = skill_master_info.count()
            pages = math.ceil(count / size)
            skill_master_info = skill_master_info.limit(size).offset((page - 1) * size).all()
   
            results = commons.query_to_dict(skill_master_info)
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
            if kwargs.get('skill_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('skill_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.skill_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('skill_name'):
                    filter_list.append(cls.skill_name == kwargs.get('skill_name'))
                if kwargs.get('parent_type') is not None:
                    filter_list.append(cls.parent_type == kwargs.get('parent_type'))
                if kwargs.get('parent_id'):
                    filter_list.append(cls.parent_id == kwargs.get('parent_id'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'skill_id': []
            }
            for query_model in res.all():
                results['skill_id'].append(query_model.skill_id)

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
            filter_list.append(cls.skill_id == kwargs.get('skill_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'skill_id': res.first().skill_id,
                
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
        param_list = kwargs.get('SkillMasterList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            skill_id = GenerateID.create_random_id()
            
            model = SkillMaster(
                skill_id=skill_id,
                skill_name=param_dict.get('skill_name'),
                parent_type=param_dict.get('parent_type'),
                parent_id=param_dict.get('parent_id'),
                
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
                added_record['skill_id'] = model.skill_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
