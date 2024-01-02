#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

userfollow_blueprint = Blueprint('userFollow', __name__)

from . import urls
