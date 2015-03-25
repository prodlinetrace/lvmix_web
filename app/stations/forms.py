from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional, Length, Required, IPAddress


class StationForm(Form):
    id = IntegerField('id', validators=[Required()])
    ip = StringField('IP Address', validators=[Required(), IPAddress()])
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    rack = IntegerField('Rack', validators=[Optional()])
    slot = IntegerField('Slot', validators=[Optional()])
    port = IntegerField('Port', validators=[Optional()])
    submit = SubmitField('Submit')

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
