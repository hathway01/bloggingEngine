from flask_wtf import Form
from flask import request
from wtforms import StringField, TextAreaField,FileField, BooleanField,SubmitField,PasswordField,validators
from .models import db,User

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign Up")


    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken.Try signing in")
            return False
        else:
            return True


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign In")

    def validate(self):
        if not Form.validate(self):
            return False
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email,password=password).first()
        if user:
            return True
        else:
            self.email.errors.append("E-mail/Password is not correct")
            return False

class BlogForm(Form):
    title = StringField(" Title ",[validators.DataRequired()])
    content = TextAreaField("Blog Content",[validators.DataRequired()])
    submit = SubmitField("Publish")

    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True