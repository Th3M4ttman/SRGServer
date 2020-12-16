from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import SRG.SRG
from SRG.forms import SRGForm
help(SRG)
application = Flask(__name__)
application.config['SECRET_KEY'] = 'poop'

@application.route('/', methods=['GET','POST'])
def create():
    form = SRGForm()
    if form.is_submitted():
        result = request.form
        byte=0
        T=False
        Q=False
        for x in result:
            if x == "Gm":
                byte+=1
            elif x == "Gf":
                byte+=2
            elif x == "Rm":
                byte+=4
            elif x == "Rf":
                byte+=8
            elif x == "Rn":
                byte+=16
            elif x == "Sm":
                byte+=32
            elif x == "Sf":
                byte+=64
            elif x == "Sn":
                byte+=128
            elif x == "T":
                T=True
            elif x == "Q":
                F=False

        bytetext=str(byte)
        if T:
            bytetext+="*"
        if Q:
            bytetext+="?"
        print("Creating " + str(byte))
        help(SRG)
        tempsrgurl = SRG.SRG.create([byte,Q,T],"","","Test")
        tempsrgurl = list(tempsrgurl)
        del tempsrgurl[4]
        srgurl=""
        for character in tempsrgurl:
            srgurl+=character
        
        return render_template('SRG.html', result=result, bytetext=bytetext, byte=byte, T=T, Q=Q, srgurl=srgurl)
 
    return render_template('create.html', form=form)

'''
@app.route('/search')
def search():
    return render_template('index.html')

@app.route('/data')
def data():
    return render_template('index.html')
'''
@application.route('/about')
def about():
    return render_template('about.html')

