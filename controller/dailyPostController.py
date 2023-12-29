#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json
import os

from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app import db
from models.daily_post import DailyPost
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings

from datetime import datetime


class DailyPostController(DailyPost):

    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        daily_post_id = GenerateID.create_random_id()
        current_time = datetime.now()

        try:
            # 创建 DailyPost 模型实例
            model = DailyPost(
                daily_post_id=daily_post_id,
                user_id=kwargs.get('user_id'),
                post_title=kwargs.get('post_title'),
                post_text=kwargs.get('post_text'),
                images=kwargs.get('images', []),  # 直接使用列表存储图片 URL
                # images=images_str,  # 使用JSON字符串保存图片URLs
                topic=kwargs.get('topic'),
                timestamp=current_time,
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                'daily_post_id': daily_post_id,
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    @staticmethod
    def upload_images(files):
        # 上传目录
        UPLOAD_FOLDER = r'/var/images'

        image_urls = []
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    file.save(file_path)
                    image_url = f"http://8.130.89.73/images/{filename}"
                    image_urls.append(image_url)
                except Exception as e:
                    loggings.exception("Failed to save file", e)

        return image_urls

    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = []
            order_by = cls.timestamp.desc()  # 默认按照时间戳降序排序
            if kwargs.get('daily_post_id'):
                filter_list.append(cls.daily_post_id == kwargs['daily_post_id'])
            else:
                if kwargs.get('user_id') is not None:
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('post_title'):
                    filter_list.append(cls.post_title == kwargs.get('post_title'))
                if kwargs.get('post_text'):
                    filter_list.append(cls.post_text == kwargs.get('post_text'))
                if kwargs.get('images'):
                    filter_list.append(cls.images == kwargs.get('images'))
                if kwargs.get('topic'):
                    filter_list.append(cls.topic == kwargs.get('topic'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                if kwargs.get('likes'):
                    filter_list.append(cls.likes == kwargs.get('likes'))
                if kwargs.get('comments'):
                    filter_list.append(cls.comments == kwargs.get('comments'))

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))

            # 如果没有提供daily_post_id，则默认返回最新的帖子
            if 'daily_post_id' not in kwargs:
                size = 3  # 如果您想获取最新的3个帖子，忽略传递的Size参数
                order_by = cls.timestamp.desc()  # 确保按照时间戳降序排序

            daily_post_info = db.session.query(cls).filter(*filter_list).order_by(order_by)

            count = daily_post_info.count()
            pages = math.ceil(count / size)
            daily_post_info = daily_post_info.limit(size).offset((page - 1) * size).all()

            results = commons.query_to_dict(daily_post_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages,
                    'data': results}

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
            if kwargs.get('daily_post_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('daily_post_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.daily_post_id == primary_key)
                filter_list.append(or_(*primary_key_list))

            else:
                if kwargs.get('user_id') is not None:
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('post_title'):
                    filter_list.append(cls.post_title == kwargs.get('post_title'))
                if kwargs.get('post_text'):
                    filter_list.append(cls.post_text == kwargs.get('post_text'))
                if kwargs.get('images'):
                    filter_list.append(cls.images == kwargs.get('images'))
                if kwargs.get('topic'):
                    filter_list.append(cls.topic == kwargs.get('topic'))
                if kwargs.get('timestamp'):
                    filter_list.append(cls.timestamp == kwargs.get('timestamp'))
                if kwargs.get('likes'):
                    filter_list.append(cls.likes == kwargs.get('likes'))
                if kwargs.get('comments'):
                    filter_list.append(cls.comments == kwargs.get('comments'))

            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'daily_post_id': []
            }
            for query_model in res.all():
                results['daily_post_id'].append(query_model.daily_post_id)

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
            filter_list.append(cls.daily_post_id == kwargs.get('daily_post_id'))

            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'daily_post_id': res.first().daily_post_id,

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
        param_list = kwargs.get('DailyPostList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            daily_post_id = GenerateID.create_random_id()

            model = DailyPost(
                daily_post_id=daily_post_id,
                user_id=param_dict.get('user_id'),
                post_title=param_dict.get('post_title'),
                post_text=param_dict.get('post_text'),
                images=param_dict.get('images'),
                topic=param_dict.get('topic'),
                timestamp=param_dict.get('timestamp'),
                likes=param_dict.get('likes'),
                comments=param_dict.get('comments'),

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
                added_record['daily_post_id'] = model.daily_post_id

                results['added_records'].append(added_record)

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
