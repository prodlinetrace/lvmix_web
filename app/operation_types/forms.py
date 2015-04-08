from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required
from flask.ext.babel import gettext, lazy_gettext


class Operation_TypeForm(Form):
    id = IntegerField(lazy_gettext('Id'), validators=[Required()])
    name = StringField(lazy_gettext('Name'), validators=[Optional(), Length(1, 50)])
    description = StringField(lazy_gettext('Description'), validators=[Required(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, station):
        self.id.data = station.id
        self.name.data = station.name
        self.description.data = station.description

    def to_model(self, station):
        station.id = self.id.data
        station.name = self.name.data
        station.description = self.description.data
