import base64
import json
import os

from flask import Flask, request, Response, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# 导入数据库配置
from database_config import get_db_connection

app = Flask(__name__)


# 上传图像到服务器，并返回url到数据库
# 设置图片存储路径
UPLOAD_FOLDER = '/root/var/www/myapp/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')
    image_urls = []

    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image_url = f"http://8.130.89.73:5000/images/{filename}"
        image_urls.append(image_url)

    return jsonify({'urls': image_urls}), 200


@app.route('/api/save-urls', methods=['POST'])
def save_urls():
    data = request.get_json()
    if not data or 'urls' not in data:
        return jsonify({'error': 'No URLs provided'}), 400

    urls = data['urls']
    urls_json = json.dumps(urls)

    connection = None  # 初始化 connection 为 None

    # 插入数据库
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO images (urls) VALUES (%s)", (urls_json,))
        connection.commit()
        return jsonify({'message': 'URLs successfully saved'}), 200
    except Exception as e:
        print(e)
        if connection:
            connection.rollback()
        return jsonify({'error': 'Error saving URLs to database'}), 500
    finally:
        if connection:
            connection.close()


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)


# 从服务器中加载数据
@app.route('/api/posts', methods=['GET'])
def get_posts():
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
                # 访问元组数据需要使用索引
                post_id = row[0]
                title = row[1]
                content = row[2]
                image = row[3]

                # 对每个图像进行 Base64 编码
                if image:
                    encoded_image = base64.b64encode(image).decode('utf-8')
                else:
                    encoded_image = None

                # 检查是否已经有这个id的动态
                if post_id in posts:
                    # 如果已经有了，添加图片到图片列表
                    if encoded_image:
                        posts[post_id]['images'].append(encoded_image)
                else:
                    # 如果还没有，创建一个新的动态条目
                    posts[post_id] = {
                        'id': post_id,
                        'title': title,
                        'content': content,
                        'images': [encoded_image] if encoded_image else []
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
    app.run(host='0.0.0.0', port=5000, debug=True)
