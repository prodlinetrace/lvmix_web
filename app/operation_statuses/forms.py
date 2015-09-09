from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import Optional, Length, Required, InputRequired
from flask.ext.babel import gettext, lazy_gettext
from ..models import Unit

#unit_list = Unit.query.order_by(Unit.id.desc())
#print unit_list
#TODO: replace this ugly hardcode by db entries
unit_choices = [('0', 'None'), ('1', 'N'), ('2', 'Nm'), ('3', 'deg'), ('4', 'mm')]

class Operation_StatusForm(Form):

    id = IntegerField(lazy_gettext('Id'), validators=[InputRequired()])
    name = StringField(lazy_gettext('Name'), validators=[Required(), Length(1, 50)])
    unit_id = SelectField(lazy_gettext('Unit'), choices=unit_choices)
    description = StringField(lazy_gettext('Description'), validators=[Optional(), Length(1, 255)])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, status):
        self.id.data = status.id
        self.name.data = status.name
        self.unit_id.data = status.unit_id
        self.description.data = status.description

    def to_model(self, status):
        status.id = self.id.data
        status.name = self.name.data
        status.unit_id = self.unit_id.data
        status.description = self.description.data
