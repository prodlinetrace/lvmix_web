from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import Optional, Length, Required, EqualTo
from flask.ext.pagedown.fields import PageDownField


class ProfileForm(Form):
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    location = StringField('Location', validators=[Optional(), Length(1, 64)])
    bio = TextAreaField('Bio')
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')


class UserForm(Form):
    login = StringField('Login', validators=[Required(), Length(1, 64)])
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    admin = BooleanField('Administrator', default=False)
    submit = SubmitField('Submit')


class EditUserForm(Form):
    login = StringField('Login', validators=[Required(), Length(1, 64)])
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    location = StringField('Location', validators=[Optional(), Length(1, 64)])
    bio = TextAreaField('Bio', validators=[Optional()])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    admin = BooleanField('Administrator', default=False)
    submit = SubmitField('Submit')

    def from_model(self, user):
        self.login.data = user.login
        self.name.data = user.name
        self.location.data = user.location
        self.bio.data = user.bio
        if self.admin:
            self.admin.data = user.is_admin

    def to_model(self, user):
        user.login = self.login.data
        user.name = self.name.data
        user.password = self.password.data
        user.location = self.location.data
        user.bio = self.bio.data
        if self.admin:
            user.is_admin = self.admin.data

