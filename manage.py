 #!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
   入口程序
"""

from app import create_app
from flask_script import Manager, Server
from flask import request, jsonify, g
from utils.response_code import RET

# 创建flask的app对象
app = create_app("develop")

# 通过Flask-Script的Manager,Server接管Flask运行
manager = Manager(app)

# 开启Debug模式
manager.add_command("runserver", Server(use_debugger=True))


# 创建全站拦截器,每个请求之前做处理
@app.before_request
def user_validation():
    print(request.endpoint)  # 方便跟踪调试
    
    if not request.endpoint: # 如果请求点为空
        return jsonify(code=RET.URLNOTFOUND, message="url not found", error="url not found")
        
@app.before_request
def user_require_token():
    # 不需要token验证的请求点列表
    permission = ['apiversion.Apiversion', 'comments.Comments', 'likes.Likes', 'message.Message', 'conversations.Conversations', 'users.Users', 'swapPost.SwapPost', 'skillRequire.SkillRequire', 'userAppointment.UserAppointment', 'userFollow.UserFollow', 'skillMaster.SkillMaster', 'dailyPost.DailyPost', 'userInfo.UserInfo']

    # 如果不是请求上述列表中的接口，需要验证token
    if request.endpoint not in permission:
        # 在请求头上拿到token
        token = request.headers.get("Token")
        if not all([token]):
            return jsonify(code=RET.PARAMERR, message="缺少参数Token或请求非法")

        # 校验token格式正确与过期时间
        secret_key = app.config['SECRET_KEY']
        from utils.jwt_util import JwtToken
        
        verify_status, payload_data = JwtToken.parse_token(token, secret_key=secret_key)
        if not verify_status:
            # 单平台用户登录失效
            app.logger.error(payload_data.get("err"))
            return jsonify(code=RET.SESSIONERR, message='用户未登录或登录已过期', error=payload_data.get("err"))
            
        # 将token中封装的信息存入当前请求的全局变量g
        g.user = payload_data


# 创建全站拦截器，每个请求之后根据请求方法统一设置返回头
@app.after_request
def process_response(response):
    allow_cors = ['OPTIONS', 'PUT', 'DELETE', 'GET', 'POST']
    if request.method in allow_cors:
        response.headers["Access-Control-Allow-Origin"] = '*'
        if request.headers.get('Origin') and request.headers['Origin'] == 'http://api.youwebsite.com':
            response.headers["Access-Control-Allow-Origin"] = 'http://api.youwebsite.com'

        response.headers["Access-Control-Allow-Credentials"] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST,PUT,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,Token,Authorization'
        response.headers['Access-Control-Expose-Headers'] = 'VerifyCodeID,ext'
    return response


if __name__ == "__main__":
    manager.run()

