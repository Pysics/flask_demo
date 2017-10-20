from app import db
# 头像
from hashlib import md5

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nickname = db.Column(db.String(64), index = True, unique = True)
  email = db.Column(db.String(120), index = True, unique = True)
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime)

  def avatar(self, size):
    return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
            (md5(self.email.encode('utf-8')).hexdigest(), size)

  @property
  def is_authenticated(self):
    return True
  def is_active(self):
    return True
  def is_anonymous(self):
    return False
  def get_id(self):
    try:
      return unicode(self.id)
    except NameError:
      return str(self.id)

  @staticmethod
  # 作为一个静态方法，因为这种操作并不适用于任何特定的类的实例。
  def make_unique_nickname(nickname):
    if User.query.filter_by(nickname = nickname).first() == None:
      return nickname
    version = 2
    while True:
      new_nickname = nickname + str(version)
      if User.query.filter_by(nickname = new_nickname).first() == None:
        break
      version += 1
    return new_nickname

  def __repr__(self):
    return '<User %r>' % (self.nickname)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime)
  # 为何是user.id而不是User.id
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Post %r>' % (self.body)
