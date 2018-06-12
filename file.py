# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory, render_template
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
            '''
            ecure_filename仅返回ASCII字符
            非ASCII（比如汉字）会被过滤掉
            空格会被替换为下划线
            '''
            filename = secure_filename(file.filename) #检查获取文件名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #保存文件至后台
            file_url = url_for('uploaded_file', filename=filename) #获取上传文件的url
            # return html + '<br><img src=' + file_url + '>' #展示图片：图片地址为/upload/<filename>，实际地址为os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template('file.html', file_url=file_url)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True,
    )