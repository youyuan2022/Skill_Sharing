#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

skillrequire_blueprint = Blueprint('skillRequire', __name__)

from . import urls
