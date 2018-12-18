from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def home():
    return render_template('mainpage.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('courses.html'), 404


if __name__ == '__main__':
    app.run(port="5000", debug=True)
