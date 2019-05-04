from flask import request
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField("提交")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("请输入一个不同的名字")

class PostForm(FlaskForm):
    post = PageDownField("现在在想什么呢？", validators=[DataRequired()])
    submit = SubmitField('发布')


class MessageForm(FlaskForm):
    message = TextAreaField("请编辑一条私信", validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('发送啦~')


class CommentForm(FlaskForm):
    body = TextAreaField("评论", validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField("发送~")


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)