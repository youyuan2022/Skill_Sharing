#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

dailypost_blueprint = Blueprint('dailyPost', __name__)

from . import urls
