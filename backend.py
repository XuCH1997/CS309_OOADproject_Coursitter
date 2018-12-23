from flask import Flask, render_template, jsonify
from db import *

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def home():
    return render_template('mainpage.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('courses.html'), 404


@app.route('/loginSt/<username>/<password>')
def loginSt(username, password):
    a = conn()
    pass_cor = a.get_user_password(username)
    if pass_cor == password:
        res = {'state': 1, 'message': 'Success'}
    else:
        res = {'state': 0, 'message': 'Fail'}
    a.close()
    return jsonify(res)


@app.route('/change_password/<username>/<password_old>/<password_new>')
def change_password(username, password_old, password_new):
    a = conn()
    pass_cor = a.get_user_password(username)
    if pass_cor == password_old:
        a.change_user_password(username, password_new)
        res = {'state': 1, 'message': 'password changed'}
    else:
        res = {'state': 0, 'message': 'old password is not correct'}
    a.close()
    return jsonify(res)




if __name__ == '__main__':
    app.run(port="5000", debug=True)
