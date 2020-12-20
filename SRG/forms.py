from wtforms import Form, fields, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.fields.html5 import DecimalRangeField
from flask_wtf import FlaskForm
class SRGForm(FlaskForm):
        Gender = fields.SelectField('Gender', choices=['Agender', 'Male' , 'Female', 'NB' ])
        Go = fields.StringField('Other')
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
        S = DecimalRangeField('Resolution', default=50)
        R = DecimalRangeField('Border Red', default=100)
        G = DecimalRangeField('Border Green', default=100)
        B = DecimalRangeField('Border Blue', default=100)

        BgRa = DecimalRangeField('Custom gender colour left half RGB', default=0)
        BgGa = DecimalRangeField('Custom gender colour left half Green', default=75)
        BgBa = DecimalRangeField('Custom gender colour left half Blue', default=100)

        BgRb = DecimalRangeField('Custom gender colour right half RGB', default=100)
        BgGb = DecimalRangeField('Custom gender colour right half Green', default=41)
        BgBb = DecimalRangeField('Custom gender colour right half Blue', default=71)
        
        Submit = SubmitField("Create SRG")

        FromNum = StringField("SRG")
        submitFromNum = SubmitField("Create SRG from number")
