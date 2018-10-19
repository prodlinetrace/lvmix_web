from flask_wtf import Form
from wtforms import SubmitField, SelectField, StringField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import Required, NumberRange, InputRequired, Length
from flask_pagedown.fields import PageDownField
from flask_babel import gettext, lazy_gettext
from wtforms.fields.simple import BooleanField


class ProductForm(Form):
    type = StringField(lazy_gettext('Product Type'), validators=[InputRequired(), Length(min=10, max=10)])
    serial = StringField(lazy_gettext('Serial Number'), validators=[Required(), Length(min=1, max=6)])
    year = StringField(lazy_gettext('Year Number'), validators=[Required(), Length(min=1, max=2)])
    week = StringField(lazy_gettext('Week Number'), validators=[Required(), Length(min=1, max=2)])
    date = DateTimeField(lazy_gettext('Date Added'), validators=[Required()])
    variant_id = SelectField(lazy_gettext('Variant'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))

    def from_model(self, product):
        self.type.data = product.type
        self.serial.data = product.serial
        self.year.data = product.year
        self.week.data = product.week
        self.date.data = product.date_added
        self.variant_id.data = product.variant_id

    def to_model(self, product):
        product.type = self.type.data
        product.serial = self.serial.data
        product.year = self.year.data
        product.week = self.week.data
        product.date_added = self.date.data
        product.variant_id = self.variant_id.data

    def __init__(self, variant_choices):
        Form.__init__(self)
        self.variant_id.choices = variant_choices


class CommentForm(Form):
    body = PageDownField(lazy_gettext('Comment'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))


class FindProductForm(Form):
    type = SelectField(lazy_gettext('Product Type'), validators=[Required()])
    serial = StringField(lazy_gettext('Serial Number'), validators=[Required()])
    submit = SubmitField(lazy_gettext('Submit'))

    def __init__(self, type_choices):
        Form.__init__(self)
        self.type.choices = type_choices


class FindProductsRangeForm(Form):
    start = StringField(lazy_gettext('From'))
    end = StringField(lazy_gettext('To'))
    status_failed = BooleanField(lazy_gettext('Status Failed'))
    operation_failed = BooleanField(lazy_gettext('Operation Failed'))
    variant_id = SelectField(lazy_gettext('Variant'))
    submit = SubmitField(lazy_gettext('Find'))

    def __init__(self, variant_choices):
        Form.__init__(self)
        self.variant_id.choices = variant_choices
