import os
from flask import Flask, request, render_template, url_for, session, redirect, flash

# shell脚本运行交互提示
from flask_script import Manager

# 引入bootstrap
from flask_bootstrap import Bootstrap

# 格式化时间
from flask_moment import Moment
from datetime import date

# 表单
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask_mail import Mail, Message

app = Flask(__name__)
# manager = Manager(app)

app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)

moment = Moment(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# mail
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'xx@163.com'
app.config['MAIL_PASSWORD'] = 'xx'

mail = Mail(app)

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'xx@163.com'

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


class NameForm(FlaskForm):
    name = StringField('Your Name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
            send_email('hellowd93@outlook.com', 'New User',
                           'mail/new_user', user=user)
        # 将name存储于session，以便在重定向后依然能拿到数据
        session['name'] = form.name.data
        return redirect(url_for('index'))
        # name = form.name.data
        # form.name.data = ''
    # user_agent = request.headers.get('User-Agent')
    return render_template('index.html', form=form, name=session.get('name'), current_time=date(2994, 8, 29))


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
