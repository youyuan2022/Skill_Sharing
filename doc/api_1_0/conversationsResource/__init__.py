#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

conversations_blueprint = Blueprint('conversations', __name__)

from . import urls
