# coding=utf-8
from flask import Flask
from flask import url_for
from flask import request
import handle_script
import logging
import datetime
import os
from hashlib import md5

logging.basicConfig(filename='serveice.log', level=logging.DEBUG)
app = Flask(__name__)
def getTIme():
    return str(datetime.datetime.now())

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        logging.info(getTIme() + " 传入" + str(f) + "文件")
        if not os.path.exists("upload"):
            os.mkdir("upload")
        time = getTIme().replace(":", ".")
        filename = "upload\\" + os.path.splitext(str(f.filename))[0] + time + os.path.splitext(str(f.filename))[1]
        f.save(filename)
        try:
            a = handle_script.Script(filename)
            logging.info(getTIme() + " 分析完成")
            return 'ok'
        except:
            logging.error("")


@app.route('/hello')
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0')



    #
    # @app.route('/post/<int:post_id>')
    # def show_post(post_id):
    #     # show the post with the given id, the id is an integer
    #     return 'Post %d' % post_id

    # @app.route('/user <username>')
    # def show_user_profile(username):
    #     # show the user profile for that user
    #     return 'User %s' % username
    '''一些简单的测试'''
    #
    # @app.route('/')
    # def hello_world():
    #     return 'Hello World!'
    #
    #
    '''构建http方法'''
