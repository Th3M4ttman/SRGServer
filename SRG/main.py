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
            lr=str(result.get("BgRa"))
            print(lr)
            if lr==0:
                print(0)
            else:
                lr=float(lr)*2.25
                lr=round(lr)
            
            lg=str(result.get("BgGa"))
            print(lg)
            if lg==0:
                print(0)
            else:
                lg=float(lg)*2.25
                lg=round(lg)
            
            lb=str(result.get("BgBa"))
            print(lb)
            lb=int(lb)
            if lb==0:
                print(0)
            else:
                lb=float(lb)*2.25
                lb=round(lb)
            
            rr=str(result.get("BgRb"))
            print(rr)
            rr=int(rr)
            if rr==0:
                print(0)
            else:
                rr=float(rr)*2.25
                rr=round(rr)
            
            rg=str(result.get("BgGb"))
            print(rg)
            rg=int(rg)
            if rg==0:
                print(0)
            else:
                rg=float(rg)*2.25
                rg=round(rg)
            
            rb=str(result.get("BgBb"))
            print(rb)
            rb=int(rb)
            if rb==0:
                print(0)
            else:
                rb=float(rb)*2.25
                rb=round(rb)
            
            l=[lr,lg,lb, 255]
            r=[rr,rg,rb, 255]
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

