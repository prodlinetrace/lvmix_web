from flask.ext.wtf import Form
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import Required, NumberRange
from flask.ext.pagedown.fields import PageDownField


class ProductForm(Form):
    type = IntegerField('Product Type', validators=[Required(), NumberRange(min=0, max=10000000000)])
    serial = IntegerField('Serial Number', validators=[Required(), NumberRange(min=0, max=10000000)])
    year = IntegerField('Year Number', validators=[Required(), NumberRange(min=0, max=99)])
    week = IntegerField('Week Number', validators=[Required(), NumberRange(min=0, max=99)])
    date = DateTimeField('Date Added', validators=[Required()])
    submit = SubmitField('Submit')

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
    body = PageDownField('Comment', validators=[Required()])
    submit = SubmitField('Submit')


class FindProductForm(Form):
    type = IntegerField('Product Type', validators=[Required()])
    serial = IntegerField('Serial Number', validators=[Required()])
    submit = SubmitField('Submit')
