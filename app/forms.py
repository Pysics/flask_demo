from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from .models import User


class LoginForm(Form):
  openid = StringField('openid', validators=[DataRequired()])
  remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
  nickname = StringField('nickname', validators=[DataRequired()])
  about_me = TextAreaField('about_me', validators=[Length(min=0, max=100)])

  def __init__(self, original_nickname, *args, **kwargs):
    # ISSUE 这句有什么用?
    Form.__init__(self, *args, **kwargs)

    self.original_nickname = original_nickname

  # 重写Form.validate
  def validate(self):
    if not Form.validate(self):
      return False
    # 未发生更改
    if self.nickname.data == self.original_nickname:
      return True
    # 发生更改查询是否重名
    user = User.query.filter_by(nickname=self.nickname.data).first()
    if user != None:
      self.nickname.errors.append('用户名已存在')
      return False
    return True
