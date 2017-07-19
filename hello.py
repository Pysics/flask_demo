from flask import Flask, request, render_template

# shell脚本运行交互提示
from flask_script import Manager

# 引入bootstrap
from flask_bootstrap import Bootstrap

# 格式化时间
from flask_moment import Moment
from datetime import date

app = Flask(__name__)
# manager = Manager(app)

bootstrap = Bootstrap(app)

moment = Moment(app)

@app.route('/')
def index():
    # user_agent = request.headers.get('User-Agent')
    return render_template('index.html', current_time=date(2994, 8, 29))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
