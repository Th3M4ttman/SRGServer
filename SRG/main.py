from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import SRG.SRG
from SRG.forms import SRGForm

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
            print(x)
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
            elif x == "R":
                R=result.get("R")
            elif x == "G":
                G=result.get("G")
            elif x == "B":
                B=result.get("B")
            elif x == "SPP":
                SPP=result.get("SPP")
            elif x == "TPP":
                TPP=result.get("TPP")
            elif x == "S":
                S=result.get("S")

        bytetext=str(byte)
        if T:
            bytetext+="*"
        if Q:
            bytetext+="?"
        print("Creating " + str(byte))
        tempsrgurl = SRG.SRG.create([byte,Q,T],SPP,TPP,int(R),int(G),int(B),int(S),"Test",True)
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

