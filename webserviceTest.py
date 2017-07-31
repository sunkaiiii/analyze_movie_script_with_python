#coding=utf-8
from flask import Flask
from flask import url_for
from flask import request
import urllib.parse
import urllib.request
import handle_script

app = Flask(__name__)
'''一些简单的测试'''
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
@app.route('/hello')
def hello():
    a=handle_script.Script('疯狂的石头.txt')
    return a.script_name
# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return 'User %s' % username
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id
'''构建url'''
# @app.route('/')
# def index():pass
#
# @app.route('/login')
# def login():pass
#
# @app.route('/user/<username>')
# def profile(username):pass
#
# with app.test_request_context():
#     print url_for('index')
#     print url_for('login')
#     print url_for('login',next='/')
#     print url_for('profile',username='sunkai')

'''构建http方法'''
@app.route('/login',methods=['POST','GET'])
def login():
    error=None
    if request.method=='POST':
        print('POST')
    else:
        print('Not Post')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
