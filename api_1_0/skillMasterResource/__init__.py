#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

skillmaster_blueprint = Blueprint('skillMaster', __name__)

from . import urls
