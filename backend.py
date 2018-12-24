from flask import Flask, render_template, jsonify, session, url_for, redirect
from db import *
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


@app.route('/home')
@app.route('/')
def home():
    return render_template('mainpage.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(404)


@app.route('/loginSt/<username>/<password>')
def loginSt(username, password):
    a = conn()
    pass_cor = a.get_user_password(username)
    if pass_cor == password:
        session['username'] = username
        res = {'state': 1, 'message': 'Success'}
    else:
        res = {'state': 0, 'message': 'Fail'}
    a.close()
    return jsonify(res)

@app.route('/check')
def isSession():
    if 'username' not in session:
        return jsonify({'message': 'plz login first!'})
    else:
        return jsonify({'message': 'okay'})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return jsonify({'message': 'logout success'})


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

@app.route('/class')
def all_classes():
    a = conn()
    res = a.get_all_classes(11510102)
    a.close()
    return jsonify(res)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/courses.html')
def courses_page():
    return render_template('courses.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5000", debug=True)
