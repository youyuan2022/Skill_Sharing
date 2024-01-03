#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

userappointment_blueprint = Blueprint('userAppointment', __name__)

from . import urls
