from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from flask.ext.babel import gettext


class LoginForm(Form):
    username = StringField(gettext('Username'), validators=[Required(), Length(1, 64)])
    password = PasswordField(gettext('Password'), validators=[Required()])
    remember_me = BooleanField(gettext('Keep me logged in'))
    submit = SubmitField(gettext('Log In'))
