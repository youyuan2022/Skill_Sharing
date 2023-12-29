#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .apiVersionResource import apiversion_blueprint
from .dailyPostResource import dailypost_blueprint
from .userInfoResource import userinfo_blueprint


def init_router(app):
    from api_1_0.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_1_0")

    # dailyPost blueprint register
    from api_1_0.dailyPostResource import dailypost_blueprint
    app.register_blueprint(dailypost_blueprint, url_prefix="/api_1_0")
    
    # userInfo blueprint register
    from api_1_0.userInfoResource import userinfo_blueprint
    app.register_blueprint(userinfo_blueprint, url_prefix="/api_1_0")
    
