# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory
from werkzeug import secure_filename

#设置上传文件允许的文件扩展名
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif',])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd() #设置上传文件夹地址
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #设置上传文件夹限制文件大小


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>图片上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) #检查获取文件名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            return html + '<br><img src=' + file_url + '>'
    return html

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True,
    )