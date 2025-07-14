
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from . import SRG
from .forms import SRGForm, SRGCrestForm
from .Flags import Flagdir

# Initialize Flask application
application = Flask(__name__)
application.config['SECRET_KEY'] = 'poop'  # Secret key for session management

# Route for the home page
@application.route('/')
def index():
    return render_template('index.html')

# Route for creating SRG objects
@application.route('/create', methods=['GET','POST'])
def create(debug=False):
    form = SRGForm()  # Initialize form
    if form.is_submitted():  # Check if form is submitted
        result = request.form  # Get form data
        # Initialize variables
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
        gt=""
        
        # Gender selection logic
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

        # Iterate through form fields
        for x in result:
            if debug: print(x)
            # Debug print for background color fields
            if x=="BgRa":
                if debug:
                    print("BgRa")
                    print(result.get("BgRa"))
            elif x=="BgGa":
                if debug:
                    print("BgGa")
                    print(result.get("BgRa"))
            elif x=="BgBa":
                if debug:
                    print("BgBa")
                    print(result.get("BgRa"))
            elif x=="BgRb":
                if debug:
                    print("BgRb")
                    print(result.get("BgRa"))
            elif x=="BgGb":
                if debug:
                    print("BgGb")
                    print(result.get("BgRa"))
            elif x=="BgBb":
                if debug:
                    print("BgBb")
                    print(result.get("BgRa"))
            # Byte value logic for various options
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
            # Color value logic
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
            # SPP and TPP values
            elif x == "SPP":
                SPP=result.get("SPP")
            elif x == "TPP":
                TPP=result.get("TPP")
            
        # Get other options from form
        o=result.get("O")
        S= round(float(result.get("S")))
        if debug: print(o)
        # Custom color logic
        if o=="y":
            o=True
            lr= round(float(result.get("BgRa")))
            lg= round(float(result.get("BgGa")))
            lb= round(float(result.get("BgBa")))
            rr= round(float(result.get("BgRb")))
            rg= round(float(result.get("BgGb")))
            rb= round(float(result.get("BgBb")))
            l=[lr,lg,lb, 255]
            r=[rr,rg,rb, 255]
            if debug: print(l)
            if debug: print(r)
            if debug: print("Custom Colour")
        else:
            o=False
            l=[255, 105, 180, 255]
            r=[0, 191, 255, 255]
            if debug: print("Default Colour")
        # Build bytetext string
        bytetext=str(byte)
        if T:
            bytetext+="*"
        if Q:
            bytetext+="?"
        if not o or result.get("Go") != "":
            gt=gender
        # GP (group points) logic
        ShowGP = result.get("ShowGP")
        if ShowGP == "y":
            gp = round(float(result.get("GP")))
            if gp==0:
                gp=1
            elif gp==100:
                gp=99
        else:
            gp = False
        # Pride flag logic
        pride1=result.get("Pride1")
        if pride1 in Flagdir.FlagNameList:
            index = Flagdir.FlagNameList.index(pride1)
            pride1 = Flagdir.FlagsList[index]
            pride1=pride1[2]
        else:
            pride1 = None
        pride2 = result.get("Pride2")
        if pride2 in Flagdir.FlagNameList:
            index = Flagdir.FlagNameList.index(pride2)
            pride2 = Flagdir.FlagsList[index]
            pride2 = pride2[2]
        else:
            pride2 = None
        pride3 = result.get("Pride3")
        if pride3 in Flagdir.FlagNameList:
            index = Flagdir.FlagNameList.index(pride3)
            pride3 = Flagdir.FlagsList[index]
            pride3 = pride3[2]
        else:
            pride3 = None
        pride4 = result.get("Pride4")
        if pride4 in Flagdir.FlagNameList:
            index = Flagdir.FlagNameList.index(pride4)
            pride4 = Flagdir.FlagsList[index]
            pride4 = pride4[2]
        else:
            pride4 = None

        print("Creating " + str(byte))
        try:
            # Call SRG.create to generate SRG URL
            tempsrgurl = SRG.create([byte,Q,T],SPP,TPP,int(R),int(G),int(B),int(S),"Test",gc=[l,r],o=o,gt=gt,gp=gp,pride1=pride1,pride2=pride2,pride3=pride3,pride4=pride4)
            print("created", tempsrgurl)
            tempsrgurl = list(tempsrgurl)
            del tempsrgurl[4]  # Remove 5th element
            srgurl=""
            for character in tempsrgurl:
                srgurl+=character
            # Render result template
            return render_template('SRG.html', result=result, bytetext=bytetext, byte=byte, T=T, Q=Q, srgurl=srgurl)
        except Exception as e:
            print("Error creating SRG:", e)
            # Render error template
            return render_template('SRG.html', result=None, bytetext="Upload Failed", byte="Upload Failed")
    # Render form template if not submitted
    return render_template('create.html', form=form)

# Route for creating SRG crest objects
@application.route('/crest', methods=['GET','POST'])
def crest(debug=True):
    form = SRGCrestForm()  # Initialize crest form
    fs = False
    if form.is_submitted():  # Check if form is submitted
        fs = True
        result = request.form  # Get form data
        # Initialize variables
        byte=0
        T=False
        Q=True
        SPP=""
        TPP=""
        R=255
        G=255
        B=255
        S=round(float(result.get("S")))
        gender=""
        gt=""
        
        # Gender selection logic
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
        # Byte value logic for various options
        for x in result:
            if x == "Rm":
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

    if fs:
        # Get SPP and TPP values
        SPP=result.get("SPP")
        TPP=result.get("TPP")
        # Custom color logic
        o=result.get("O")
        print(o)
        if o == "y":
            o = True
            lr = round(float(result.get("BgRa")))
            lg = round(float(result.get("BgGa")))
            lb = round(float(result.get("BgBa")))
            rr = round(float(result.get("BgRb")))
            rg = round(float(result.get("BgGb")))
            rb = round(float(result.get("BgBb")))
            l = (lr, lg, lb, 255)
            r = (rr, rg, rb, 255)
            print(l)
            print(r)
            print("Custom Colour L:".join(str(v) for v in l)+" R:".join(str(v) for v in r))
        else:
            o=False
            l=(255, 105, 180, 255)
            r=(0, 191, 255, 255)
            print("Default Colour")
        # Build bytetext string
        bytetext=str(byte)
        if T:
            bytetext+="*"
        if Q:
            bytetext+="?"
        if result.get("Go") != "":
           gt=result.get("Go")
        # Get crest color options
        trim = (round(float(result.get("TR"))),round(float(result.get("TG"))),round(float(result.get("TB"))),255)
        ad = (round(float(result.get("AR"))),round(float(result.get("AG"))),round(float(result.get("AB"))),255)
        wings = (round(float(result.get("WR"))),round(float(result.get("WG"))),round(float(result.get("WB"))),255)
        glow = (round(float(result.get("GR"))),round(float(result.get("GG"))),round(float(result.get("GB"))),75)
        rn = result.get("Roman")
        # GP (group points) logic
        ShowGP=result.get("ShowGP")
        if ShowGP == "y":
            gp = round(float(result.get("GP")))
        else:
            gp=False
        # Roman option logic
        if rn == "y":
            rn=True
        else:
            rn=False

        print("Creating " + str(byte))
        print(trim)
        print(wings)
        print(ad)
        print(glow)

        # Call SRG.crest to generate crest URL
        tempsrgurl = SRG.crest(SRG=[byte,Q,T],p1=SPP,p2=TPP,gt=gt,rn=rn,o=o,bgl=l,bgr=r,trim=trim,wings=wings,ad=ad,glow=glow,gp=gp,s=S)
        tempsrgurl = list(tempsrgurl)
        del tempsrgurl[4]  # Remove 5th element
        srgurl=""
        for character in tempsrgurl:
            srgurl+=character
        # Render result template
        return render_template('SRG.html', result=result, bytetext=bytetext, byte=byte, T=T, Q=Q, srgurl=srgurl)
    else:
        # Render form template if not submitted
        return render_template('crest.html', form=form)

# Route for about page
@application.route('/about')
def about():
    return render_template('about.html')

# Route for picture tutorial page
@application.route('/pictut')
def pictut():
    return render_template('PicTutorial.html')
