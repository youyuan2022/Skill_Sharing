#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import userappointment_blueprint
from api_1_0.userAppointmentResource.userAppointmentResource import UserAppointmentResource
from api_1_0.userAppointmentResource.userAppointmentOtherResource import UserAppointmentOtherResource

api = Api(userappointment_blueprint)

api.add_resource(UserAppointmentResource, '/userAppointment/<appointment_id>', '/userAppointment', endpoint='UserAppointment')

