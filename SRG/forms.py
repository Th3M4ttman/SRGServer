from wtforms import Form, fields, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.fields.html5 import DecimalRangeField
from flask_wtf import FlaskForm
class SRGForm(FlaskForm):
        Gm = fields.BooleanField('Do you identify as Male')
        Gf = fields.BooleanField('Do you identify as Female')
        Rm = fields.BooleanField('Are you romantically attracted to Males')
        Rf = fields.BooleanField('Are you romantically attracted to Females')
        Rn = fields.BooleanField('Are you romantically attracted to NBs')
        Sm = fields.BooleanField('Are you sexually attracted to Males')
        Sf = fields.BooleanField('Are you sexually attracted to Females')
        Sn = fields.BooleanField('Are you sexually attracted to NBs')

        T = fields.BooleanField('Do you wish to identify as Trans')
        Q = fields.BooleanField('Are you certain of your orientation')
        SPP = StringField("Second Person Pronoun")
        TPP = StringField("Third Person Pronoun")
        S = DecimalRangeField('Age', default=500)
        R = DecimalRangeField('Age', default=255)
        G = DecimalRangeField('Age', default=255)
        B = DecimalRangeField('Age', default=255)
        
        Submit = SubmitField("Create SRG")

        FromNum = StringField("SRG")
        submitFromNum = SubmitField("Create SRG from number")
