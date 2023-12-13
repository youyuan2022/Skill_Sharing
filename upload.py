import base64
from flask import Flask, request, Response, jsonify
from sqlalchemy.dialects import mysql
from werkzeug.utils import secure_filename

# 导入数据库配置
from database_config import get_db_connection

app = Flask(__name__)


# 查看数据库中的图像
@app.route('/get-image/<int:image_id>')
def get_image(image_id):
    # 使用 database_config 模块获取数据库连接
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 执行SQL查询
            sql = "SELECT image FROM images WHERE id = %s"
            cursor.execute(sql, (image_id,))
            result = cursor.fetchone()
            if result:
                # 返回图像数据，假设图像是 JPEG 格式
                return Response(result[0], mimetype='image/jpeg')
            else:
                return 'Image not found', 404
    finally:
        connection.close()


# 上传图像到数据库
@app.route('/api/upload', methods=['POST'])
def save_text_and_image():
    title = request.form.get('title', '')  # 获取标题
    bodyText = request.form.get('bodyText', '')  # 获取正文文本
    user = request.form.get('user', '')  # 获取用户信息
    file = request.files.get('file')  # 获取上传的文件

    # 验证标题、正文文本和文件是否存在
    if not title or not bodyText:
        return 'No text provided', 400
    if not file or file.filename == '':
        return 'No file provided', 400

    filename = secure_filename(file.filename)
    image_content = file.read()

    # 使用 database_config 模块获取数据库连接
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 插入标题和正文文本
            cursor.execute('INSERT INTO texts (title, content) VALUES (%s, %s)', (title, bodyText))
            # 插入图像
            cursor.execute("INSERT INTO images (image) VALUES (%s)", (image_content,))
            # 提交事务
            connection.commit()
    except Exception as e:
        connection.rollback()
        return f'An error occurred: {str(e)}', 500
    finally:
        connection.close()

    return 'Text and Image successfully uploaded', 200


# 从服务器中加载数据
@app.route('/api/posts', methods=['GET'])
def get_posts():
    # 使用 database_config 模块获取数据库连接
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 查询texts和images表
            sql = """
            SELECT t.id, t.title, t.content, i.image
            FROM texts t
            LEFT JOIN images i ON t.id = i.id
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

            posts = {}
            for row in rows:
                # 获取图像的 URL
                image_url = row['imageUrl'] if row['imageUrl'] else None

                # 检查是否已经有这个id的动态
                if row['id'] in posts:
                    # 如果已经有了，添加图片 URL 到图片列表
                    if image_url:
                        posts[row['id']]['images'].append(image_url)
                else:
                    # 如果还没有，创建一个新的动态条目
                    posts[row['id']] = {
                        'id': row['id'],
                        'title': row['title'],
                        'content': row['content'],
                        'images': [image_url] if image_url else []
                    }

                # 获取所有动态的列表
            posts_list = list(posts.values())

            return jsonify(posts_list)
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
