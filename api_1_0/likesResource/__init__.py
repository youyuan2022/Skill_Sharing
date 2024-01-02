#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

likes_blueprint = Blueprint('likes', __name__)

from . import urls
