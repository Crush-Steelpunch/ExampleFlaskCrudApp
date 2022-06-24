from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, BooleanField

class ManipItem(FlaskForm):
    form_item_name = StringField("Name")
    form_item_value = DecimalField("Value")
    form_item_boolean = BooleanField("Boolean")
    form_item_submit_add = SubmitField("Add Item")
    form_item_submit_edit = SubmitField("Update Item")
    form_item_submit_delete = SubmitField("Delete Item")

class ManipItemAttributes(FlaskForm):
    form_itemAttr_name = StringField("Name")
    form_itemAttr_value = DecimalField("Value")
    form_itemAttr_boolean = BooleanField("Boolean")
    form_itemAttr_submit = SubmitField("Add Item Attribute")
    form_itemAttr_submit_update = SubmitField("Update Item Attribute")