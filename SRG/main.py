from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import SRG.SRG
from SRG.forms import SRGForm

application = Flask(__name__)
application.config['SECRET_KEY'] = 'poop'

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/create', methods=['GET','POST'])
def create(debug=True):
    form = SRGForm()
    if form.is_submitted():
        result = request.form
        byte=0
        T=False
        Q=True
        SPP=""
        TPP=""
        R=255
        G=255
        B=255
        S=500
        gender=""
        if result.get("Gender") == 'Male':
            byte+=1
            gender="Male"
        elif result.get("Gender") == "Female":
            byte+=2
            gender="Female"
        elif result.get("Gender") == 'Agender':
            byte+=0
            gender="Agender"
        else:
            byte+=3
            gender=result.get("Go")

        for x in result:
            if debug: print(x)
            


            if x=="BgRa":
                print("BgRa")
                print(result.get("BgRa"))
            elif x=="BgGa":
                print("BgGa")
                print(result.get("BgRa"))
            elif x=="BgBa":
                print("BgBa")
                print(result.get("BgRa"))
                
            elif x=="BgRb":
                print("BgRb")
                print(result.get("BgRa"))
            elif x=="BgGb":
                print("BgGb")
                print(result.get("BgRa"))
            elif x=="BgBb":
                print("BgBb")
                print(result.get("BgRa"))
                

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
                Q=False
            elif x == "R":
                R=result.get("R")
                R=round(float(R))
                R=round(int(R)*2.55)
            elif x == "G":
                G=result.get("G")
                G=round(float(G))
                G=round(int(G)*2.55)
            elif x == "B":
                B=result.get("B")
                B=round(float(B))
                B=round(int(B)*2.55)
            elif x == "SPP":
                SPP=result.get("SPP")
            elif x == "TPP":
                TPP=result.get("TPP")
            elif x == "S":
                S=result.get("S")
                S=round(float(S))
                S=round(int(S)*10.80)
                if S<100:
                    S=100
            
        o=result.get("O")
        print(o)
        if o=="y":
            o=True
            l=[result.get("BgRa"), result.get("BgGa"), result.get("BgBa"), 255]
            r=[result.get("BgRb"), result.get("BgGb"), result.get("BgBb"), 255]
            print(l)
            print(r)
            print("Custom Colour")
        else:
            o=False
            l=[255, 105, 180, 255]
            r=[0, 191, 255, 255]
            print("Default Colour")
        bytetext=str(byte)
        if T:
            bytetext+="*"
        if Q:
            bytetext+="?"         
        print("Creating " + str(byte))
        tempsrgurl = SRG.SRG.create([byte,Q,T],SPP,TPP,int(R),int(G),int(B),int(S),"Test",gc=[l,r],o=o)
        tempsrgurl = list(tempsrgurl)
        del tempsrgurl[4]
        srgurl=""
        for character in tempsrgurl:
            srgurl+=character
        
        return render_template('SRG.html', result=result, bytetext=bytetext, byte=byte, T=T, Q=Q, srgurl=srgurl)
 
    return render_template('create.html', form=form)

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/pictut')
def pictut():
    return render_template('PicTutorial.html')

