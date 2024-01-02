#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

swappost_blueprint = Blueprint('swapPost', __name__)

from . import urls
