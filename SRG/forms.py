from wtforms import Form, fields, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.fields.html5 import DecimalRangeField, DecimalField
from flask_wtf import FlaskForm
import wtforms
from Flags import Flagdir
flagchoices=Flagdir.getflags(True)
flagchoices.insert(0,"None")
print(flagchoices)
class SRGForm(FlaskForm):

        ch=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255]
        
        
        Gender = fields.SelectField('Gender', choices=['Agender', 'Male' , 'Female', 'NB' ])
        Go = fields.StringField('Other')
        Rm = fields.BooleanField('Are you romantically attracted to Males')
        Rf = fields.BooleanField('Are you romantically attracted to Females')
        Rn = fields.BooleanField('Are you romantically attracted to NBs')
        Sm = fields.BooleanField('Are you sexually attracted to Males')
        Sf = fields.BooleanField('Are you sexually attracted to Females')
        Sn = fields.BooleanField('Are you sexually attracted to NBs')
        GP = DecimalRangeField('Genital preference', default=50)
        ShowGP = fields.BooleanField('Show genital preference')

        T = fields.BooleanField('Do you wish to identify as Trans')
        Q = fields.BooleanField('Are you certain of your orientation')
        SPP = StringField("Pronoun 1")
        TPP = StringField("Pronoun 2")
        S = DecimalRangeField('Resolution', default=100, places=0)
        R = DecimalRangeField('BorderRGB', default=255, places=0)
        G = DecimalRangeField('BorderRGB', default=255, places=0)
        B = DecimalRangeField('BorderRGB', default=255, places=0)
        
        O = fields.BooleanField('Override Gender Colour')

        BgRa = DecimalRangeField("Custom gender colour left half", default=0, places=0)
        BgGa = DecimalRangeField("Custom gender colour left half", default=75, places=0)
        BgBa = DecimalRangeField("Custom gender colour left half", default=100, places=0)

        BgRb = DecimalRangeField("Custom gender colour right half", default=100, places=0)
        BgGb = DecimalRangeField("Custom gender colour right half", default=41, places=0)
        BgBb = DecimalRangeField("Custom gender colour right half", default=71, places=0)

        Pride1 = fields.SelectField('Pride Flag Top Left', choices=flagchoices, default="None")
        Pride2 = fields.SelectField('Pride Flag Top Right', choices=flagchoices, default="None")
        Pride3 = fields.SelectField('Pride Flag Bottom Left', choices=flagchoices, default="None")
        Pride4 = fields.SelectField('Pride Flag Bottom Right', choices=flagchoices, default="None")

        
        Submit = SubmitField("Create SRG")

        FromNum = StringField("SRG")
        submitFromNum = SubmitField("Create SRG from number")

class SRGCrestForm(FlaskForm):
        ch=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255]
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
        SPP = StringField("Pronoun 1")
        TPP = StringField("Pronoun 2")
        S = DecimalRangeField('Resolution', default=50)
        GP = DecimalRangeField('Genital preference', default=50)
        ShowGP = fields.BooleanField('Show genital preference')

        O = fields.BooleanField('Override Gender Colour')

        BgRa = fields.SelectField('Custom gender colour left half', choices=ch, default=0)
        BgGa = fields.SelectField('Custom gender colour left half', choices=ch, default=75)
        BgBa = fields.SelectField('Custom gender colour left half', choices=ch, default=100)

        BgRb = fields.SelectField('Custom gender colour right half', choices=ch, default=100)
        BgGb = fields.SelectField('Custom gender colour right half', choices=ch, default=41)
        BgBb = fields.SelectField('Custom gender colour right half', choices=ch, default=71)

        # Trim

        TR = fields.SelectField('Trim colour', choices=ch, default=218)
        TG = fields.SelectField('Trim colour', choices=ch, default=165)
        TB = fields.SelectField('Trim colour', choices=ch, default=32)

        # wings

        WR = fields.SelectField('Wing colour', choices=ch, default=0)
        WG = fields.SelectField('Wing colour', choices=ch, default=0)
        WB = fields.SelectField('Wing colour', choices=ch, default=0)

        # adornment

        AR = fields.SelectField('Adornment colour', choices=ch, default=255)
        AG = fields.SelectField('Adornment colour', choices=ch, default=255)
        AB = fields.SelectField('Adornment colour', choices=ch, default=255)

        # glow

        GR = fields.SelectField('Glow colour', choices=ch, default=218)
        GG = fields.SelectField('Glow colour', choices=ch, default=165)
        GB = fields.SelectField('Glow colour', choices=ch, default=32)
        GA = fields.SelectField('Glow colour', choices=ch, default=75)
        Roman = fields.BooleanField('Do you wish to convert your SRG into roman numerals')

        Submit = SubmitField("Create SRG")

        FromNum = StringField("SRG")
        submitFromNum = SubmitField("Create SRG from number")

