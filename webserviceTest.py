#coding=utf-8
from flask import Flask
from flask import url_for
from flask import request
import handle_script

app = Flask(__name__)

'''一些简单的测试'''
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
'''构建http方法'''
@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method=='POST':
        print(request.get_data())
        print(request.headers)
        print(request.files)
        f=request.files['file']
        f.save('testsave.txt')
        a = handle_script.Script('testsave.txt')
        return ';123'

@app.route('/hello')
def hello():
    a=handle_script.Script('疯狂的石头.txt')
    return a.script_name


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