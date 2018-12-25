from flask import Flask, render_template, jsonify, session, url_for, redirect
from flask_cors import CORS, cross_origin
from db import *
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app)


@app.route('/home')
@app.route('/')
@cross_origin()
def home():
    return render_template('mainpage.html')


@app.errorhandler(404)
@cross_origin()
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(404)


@app.route('/loginSt/<username>/<password>', methods=['GET', 'POST'])
@cross_origin()
def loginSt(username, password):
    logout()
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
@cross_origin()
def isSession():
    if 'username' not in session:
        return jsonify({'message': 'plz login first!'})
    else:
        return jsonify({'message': 'okay'})


@app.route('/logout')
@cross_origin()
def logout():
    session.pop('username', None)
    return jsonify({'message': 'logout success'})


@app.route('/change_password/<username>/<password_old>/<password_new>')
@cross_origin()
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


@app.route('/all_class')
@cross_origin()
def all_classes():
    if 'username' in session:
        UID = session['username']
        a = conn()
        res = a.get_all_classes(UID)
        a.close()
        return jsonify(res)
    else:
        return redirect(url_for('login_page'))


@app.route('/schedule')
@cross_origin()
def schedule():
    if 'username' in session:
        UID = session['username']
        a = conn()
        res = a.get_schedule(UID)
        a.close()
        return jsonify(res)
    else:
        return redirect(url_for('login_page'))


@app.route('/pick/<CID>')
@cross_origin()
def pick_class(CID):
    if 'username' in session:
        UID = session['username']
        a = conn()
        msg = a.select_course(UID, CID)
        a.close()
        return msg
    else:
        return redirect(url_for('login_page'))


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/myself')
def myself_page():
    return render_template('myself.html')


@app.route('/changePassword')
def change_page():
    return render_template('changePassword.html')


@app.route('/withdraw/<CID>')
def withdraw(CID):
    if 'username' in session:
        UID = session['username']
        a = conn()
        a.withdraw_course(UID, CID)
        a.close()
        return jsonify({"message": "success"})
    else:
        return redirect(url_for('login_page'))


@app.route('/login')
@cross_origin()
def login_page():
    return render_template('login.html')


@app.route('/courses')
@cross_origin()
def courses_page():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('courses.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
