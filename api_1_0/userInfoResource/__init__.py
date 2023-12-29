#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

userinfo_blueprint = Blueprint('userInfo', __name__)

from . import urls
