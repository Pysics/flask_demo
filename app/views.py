from app import app, db, lm, oid
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, EditForm
from .models import User, Post
from datetime import datetime


@app.before_request
def before_quest():
  g.user = current_user
  if g.user.is_authenticated:
    g.user.last_seen = datetime.utcnow()
    # 修改全局用户配置，并更新到数据库
    db.session.add(g.user)
    db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
  user = g.user
  posts = [
    {
      'author': {'nickname': 'John'},
      'body': 'Beautiful day in Portland!'
    },
    {
      'author': {'nickname': 'Susan'},
      'body': 'The Avengers movie was so cool!'
    }
  ]
  return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
  # 已登陆用户定位到首页不用登录
  if g.user is not None and g.user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
  return render_template('login.html', title='Sign In', form=form, providers = app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

@oid.after_login
def after_login(resp):
  if resp.email is None or resp.email == '':
    flash('不合法的邮件地址，请重试')
    return redirect(url_for('login'))
  user = User.query.filter_by(email=resp.email).first()
  if user is None:
    nickname = resp.nickname
    if nickname is None or nickname == '':
      nickname = resp.email.splite('@')[0]
    nickname = User.make_unique_nickname(nickname)
    user = User(nickname=nickname, email=resp.email)
    db.session.add(user)
    db.session.commit()
  remember_me = False
  if 'remember_me' in session:
    remember_me = session['remember_me']
    session.pop('remember_me', None)
  login_user(user, remember = remember_me)
  return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
  user = User.query.filter_by(nickname = nickname).first()
  if user == None:
    flash('没有 ' + nickname + ' 这个用户')
    return redirect(url_for('index'))
  posts = [
    {'author': user, 'body': '第一篇文章'},
    {'author': user, 'body': '第二篇文章'}
  ]
  return render_template('user.html', user=user, posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
  # ISSUE POST时,传递g的user给表单验证, 但是此时的user还是未更改前的吧
  form = EditForm(g.user.nickname)
  if form.validate_on_submit():
    # 更新个人信息
    g.user.nickname = form.nickname.data
    g.user.about_me = form.about_me.data
    db.session.add(g.user)
    db.session.commit()
    flash('更改生效')
    return redirect(url_for('index'))
  else:
    # 初始化? GET
    # 未通过验证
    form.nickname.data = g.user.nickname
    form.about_me.data = g.user.about_me
  return render_template('edit.html', form=form)

@app.errorhandler(404)
def internal_error(error):
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('500.html'), 500
