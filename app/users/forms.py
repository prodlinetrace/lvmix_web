from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import Optional, Length, Required, EqualTo
from flask.ext.pagedown.fields import PageDownField
from flask.ext.babel import gettext


class ProfileForm(Form):
    name = StringField(gettext('Name'), validators=[Optional(), Length(1, 64)])
    location = StringField(gettext('Location'), validators=[Optional(), Length(1, 64)])
    bio = TextAreaField(gettext('Bio'))
    password = PasswordField(gettext('Password'), validators=[Required(), EqualTo(gettext('confirm'), message=gettext('Passwords must match'))])
    confirm = PasswordField(gettext('Repeat Password'))
    submit = SubmitField(gettext('Submit'))


class UserForm(Form):
    login = StringField(gettext('Login'), validators=[Required(), Length(1, 64)])
    name = StringField(gettext('Name'), validators=[Required(), Length(1, 64)])
    password = PasswordField(gettext('Password'), validators=[Required(), EqualTo(gettext('confirm'), message=gettext('Passwords must match'))])
    confirm = PasswordField(gettext('Repeat Password'))
    admin = BooleanField(gettext('Administrator'), default=False)
    submit = SubmitField(gettext('Submit'))


class EditUserForm(Form):
    login = StringField(gettext('Login'), validators=[Required(), Length(1, 64)])
    name = StringField(gettext('Name'), validators=[Required(), Length(1, 64)])
    location = StringField(gettext('Location'), validators=[Optional(), Length(1, 64)])
    bio = TextAreaField(gettext('Bio'), validators=[Optional()])
    password = PasswordField(gettext('Password'), validators=[Required(), EqualTo(gettext('confirm'), message=gettext('Passwords must match'))])
    confirm = PasswordField(gettext('Repeat Password'))
    admin = BooleanField(gettext('Administrator'), default=False)
    submit = SubmitField(gettext('Submit'))

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

