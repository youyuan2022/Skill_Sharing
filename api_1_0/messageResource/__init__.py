#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

message_blueprint = Blueprint('message', __name__)

from . import urls
