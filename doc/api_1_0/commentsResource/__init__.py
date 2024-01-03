#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

comments_blueprint = Blueprint('comments', __name__)

from . import urls
