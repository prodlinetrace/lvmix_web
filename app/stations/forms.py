from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, IPAddress
from flask.ext.babel import gettext


class StationForm(Form):
    id = IntegerField(gettext('Id'), validators=[Required()])
    ip = StringField(gettext('IP Address'), validators=[Required(), IPAddress()])
    name = StringField(gettext('Name'), validators=[Optional(), Length(1, 64)])
    rack = IntegerField(gettext('Rack'), validators=[Optional()])
    slot = IntegerField(gettext('Slot'), validators=[Optional()])
    port = IntegerField(gettext('Port'), validators=[Optional()])
    submit = SubmitField(gettext('Submit'))

    def from_model(self, station):
        self.id.data = station.id
        self.ip.data = station.ip
        self.name.data = station.name
        self.rack.data = station.rack
        self.slot.data = station.slot
        self.port.data = station.port

    def to_model(self, station):
        station.id = self.id.data
        station.ip = self.ip.data
        station.name = self.name.data
        station.rack = self.rack.data
        station.port = self.port.data
        station.slot = self.slot.data
