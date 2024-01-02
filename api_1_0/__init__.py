#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .apiVersionResource import apiversion_blueprint
from .commentsResource import comments_blueprint
from .likesResource import likes_blueprint
from .messageResource import message_blueprint
from .conversationsResource import conversations_blueprint
from .usersResource import users_blueprint
from .swapPostResource import swappost_blueprint
from .skillRequireResource import skillrequire_blueprint
from .userAppointmentResource import userappointment_blueprint
from .userFollowResource import userfollow_blueprint
from .skillMasterResource import skillmaster_blueprint
from .dailyPostResource import dailypost_blueprint
from .userInfoResource import userinfo_blueprint


def init_router(app):
    from api_1_0.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_1_0")

    # comments blueprint register
    from api_1_0.commentsResource import comments_blueprint
    app.register_blueprint(comments_blueprint, url_prefix="/api_1_0")
    
    # likes blueprint register
    from api_1_0.likesResource import likes_blueprint
    app.register_blueprint(likes_blueprint, url_prefix="/api_1_0")
    
    # message blueprint register
    from api_1_0.messageResource import message_blueprint
    app.register_blueprint(message_blueprint, url_prefix="/api_1_0")
    
    # conversations blueprint register
    from api_1_0.conversationsResource import conversations_blueprint
    app.register_blueprint(conversations_blueprint, url_prefix="/api_1_0")
    
    # users blueprint register
    from api_1_0.usersResource import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix="/api_1_0")
    
    # swapPost blueprint register
    from api_1_0.swapPostResource import swappost_blueprint
    app.register_blueprint(swappost_blueprint, url_prefix="/api_1_0")
    
    # skillRequire blueprint register
    from api_1_0.skillRequireResource import skillrequire_blueprint
    app.register_blueprint(skillrequire_blueprint, url_prefix="/api_1_0")
    
    # userAppointment blueprint register
    from api_1_0.userAppointmentResource import userappointment_blueprint
    app.register_blueprint(userappointment_blueprint, url_prefix="/api_1_0")
    
    # userFollow blueprint register
    from api_1_0.userFollowResource import userfollow_blueprint
    app.register_blueprint(userfollow_blueprint, url_prefix="/api_1_0")
    
    # skillMaster blueprint register
    from api_1_0.skillMasterResource import skillmaster_blueprint
    app.register_blueprint(skillmaster_blueprint, url_prefix="/api_1_0")
    
    # dailyPost blueprint register
    from api_1_0.dailyPostResource import dailypost_blueprint
    app.register_blueprint(dailypost_blueprint, url_prefix="/api_1_0")
    
    # userInfo blueprint register
    from api_1_0.userInfoResource import userinfo_blueprint
    app.register_blueprint(userinfo_blueprint, url_prefix="/api_1_0")
    
