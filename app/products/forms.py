from flask.ext.wtf import Form
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import Required, NumberRange, InputRequired
from flask.ext.pagedown.fields import PageDownField
from flask.ext.babel import gettext, lazy_gettext


class ProductForm(Form):
    type = IntegerField(lazy_gettext('Product Type'), validators=[InputRequired(), NumberRange(min=0, max=10000000000)])
    serial = IntegerField(lazy_gettext('Serial Number'), validators=[Required(), NumberRange(min=0, max=10000000)])
    year = IntegerField(lazy_gettext('Year Number'), validators=[Required(), NumberRange(min=0, max=99)])
    week = IntegerField(lazy_gettext('Week Number'), validators=[Required(), NumberRange(min=0, max=99)])
    date = DateTimeField(lazy_gettext('Date Added'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, product):
        self.type.data = product.type
        self.serial.data = product.serial
        self.year.data = product.year
        self.week.data = product.week
        self.date.data = product.date_added

    def to_model(self, product):
        product.type = self.type.data
        product.serial = self.serial.data
        product.year = self.year.data
        product.week = self.week.data
        product.date_added = self.date.data 


class CommentForm(Form):
    body = PageDownField(lazy_gettext('Comment'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))


class FindProductForm(Form):
    type = IntegerField(lazy_gettext('Product Type'), validators=[Required()])
    serial = IntegerField(lazy_gettext('Serial Number'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))
