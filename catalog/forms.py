from wtforms import Form, SelectField, StringField, TextAreaField, DecimalField, validators
from flask import flash


class ItemForm(Form):
    name = StringField('Name', [validators.Length(max=80), validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(max=250), validators.DataRequired()])
    category_id = SelectField('Category', coerce=int)
    price = DecimalField('Price')


def flash_form_errors(form):
    for field_name in form.errors:
        label = form[field_name].label
        print form[field_name].label
        for error in list(form.errors[field_name]):
            flash('<strong>%s</strong>: %s!' % (label, error), 'danger')
