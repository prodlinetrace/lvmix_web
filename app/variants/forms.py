from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask_babel import gettext, lazy_gettext


class VariantForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 50)])
    description = StringField(lazy_gettext('Description'), validators=[Optional(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, variant):
        self.id.data = variant.id
        self.name.data = variant.name
        self.description.data = variant.description

    def to_model(self, variant):
        variant.id = self.id.data
        variant.name = self.name.data
        variant.description = self.description.data
