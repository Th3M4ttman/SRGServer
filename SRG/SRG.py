
import tempfile
from PIL import Image, ImageDraw, ImageFont
import pyinputplus as pyip
from os import system, name
import os
import time
import numpy as np
from pathlib import Path


def clear(): 

    if name == 'nt': 

        _ = system('cls') 

    else: 

        _ = system('clear')
        
def srg_to_byte(srg, printbyte=False,printbit=False,printbitvalue=False):
	b=1
	byte=0
	for x in range(7,-1,-1):
		if srg[x]==True:
			byte+=b
		if printbit: print(srg[x])
		if printbitvalue: print(b)	
		if b==1:
			b=2
		else:
			b=b*2
	if printbyte: print(byte)
	return int(byte)
        
def input_srg(printbyte=False,printbit=False,printbitvalue=False):
	
	srg=["Are you sexually attracted to NBs?\n","Are you sexually attracted to females?\n","Are you sexually attracted to males?\n","Are you romantically attracted to NBs?\n","Are you romantically attracted to females?\n","Are you romantically attracted to males?\n","Do you identify as female?\n","Do you identify as Male?\n"]


	i=7
	for x in range(0,8):
		bit=pyip.inputMenu(['Yes', 'No'], lettered=False, numbered=True,  prompt=srg[i], default="No", blank=True)
		if bit=="Yes":
			srg[i]=True
		else:
			srg[i]=False
		print(srg[i])
		time.sleep(0.1)
		clear()
		i-=1
		
	byte=srg_to_byte(srg, printbyte,printbit,printbitvalue)
	
	trans=pyip.inputMenu(['Yes', 'No'], lettered=False, numbered=True,  prompt="Do you wish to identify as trans\n", default="No", blank=True)
	questioning=pyip.inputMenu(['Yes', 'No'], lettered=False, numbered=True,  prompt="Are you certain of your sexual/romantic orientation\n", default="Yes", blank=True)
	
	if trans=="Yes":
		trans="*"
	else:
		trans=""
		
	if questioning=="No":
		questioning="?"
	else:
		questioning=""
	combined=str(byte)+questioning+trans
		
	output=[combined,byte,questioning,trans]

	
	return output

def srgint_to_bools(srg,debug=False):
	
	b=128
	i=0
	debugbyte=["SNB","SF","SM","RNB","RF","RM","F","M"]
	byte=[False, False, False, False, False,False, False, False]
	workingsrg=srg
	
	for y in range(0,8):
		if workingsrg >= b:
			byte[i]=True
			if debug: print(workingsrg)
			workingsrg-=b
		elif workingsrg==1:
			if debug: print(workingsrg)
			byte[7]=True
			workingsrg-=b
		i+=1
		b=int(b/2)
		if b==0:
			break
			
	if debug:
		print(debugbyte)
		print(byte)
	return byte
			

def gender_colour(x,array,width,height,p=False, lc=[0, 191, 255, 255], rc=[255, 105, 180, 255],O=False):
    '''applys gender colour to background'''
        
    if O:
        if p: print("NB")
        array[:,:int(width/2)] = lc 
        array[:,int(width/2):] = rc
        
    elif x[7] and x[6]:
        if p: print("NB")
        array[:,:int(width/2)] = lc #blue
        array[:,int(width/2):] = rc #pink
        
    elif x[7]:
        if p: print("Male")
        array[:,:] = [0, 191, 255, 255]
    
    elif x[6]:
        if p: print("Female")
        array[:,:] = [255, 105, 180, 255]

    else:
        if p: print("Agender")
        array[:,:] = [50, 50, 50, 255]

		
def add_text(im,text,W,H,bordercolor=(0,0,0),so=[False,False,False],ro=[False,False,False],p1="They", p2="Them"):
	
	
	bigFont = ImageFont.truetype("Font.ttf", int(W/4))
	smallFont = ImageFont.truetype("Font.ttf", int(W/10))

	draw = ImageDraw.Draw(im)
	#w, h = draw.textsize(text)
	#draw.text(((W-w)/2,(H-h)/2), text, fill="black", align='center', font=bigFont)
	
	bounding_box = [0, 0, W, H]
	x1, y1, x2, y2 = bounding_box  # For easy reading
	
	# Calculate the width and height of the text to be drawn, given font size
	# Calculate the mid points and offset by the upper left corner of the bounding box
	w, h = draw.textsize(text, font=bigFont)
	x = (x2 - x1 - w)/2 + x1
	y = (y2 - y1 - h)/2 + y1


	# Write the text to the image, where (x,y) is the top left corner of the text
	draw.text((x, y), text, align='center', font=bigFont, fill='white', stroke_width=5, stroke_fill='black')
	
	w, h = draw.textsize(p1, font=smallFont)
	x = (W - w)/2 
	y = H/15

	draw.text((x, y), p1, align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
	
	w, h = draw.textsize(p2, font=smallFont)
	x = (W - w)/2 
	y = H-(H/7)

	
	draw.text((x, y), p2, align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
	
	#draw Frame
	
	draw.rectangle([x1, y1, x2, y2], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor))
	
	draw.rectangle([x1, y1, x2, y2], width=int(W/100), outline=bordercolor)
	
	#draw top left corner
	
	draw.rectangle([0, 0, int(W/5), int(H/5)], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor),fill=tuple(int(ti/1.5) for ti in bordercolor))
	
	draw.rectangle([0, 0, int(W/5), int(H/5)], width=int(W/100), outline=bordercolor)
	
	#draw top right corner
	
	draw.rectangle([int(W-(W/5)), 0, W, int(H/5)], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor),fill=tuple(int(ti/1.5) for ti in bordercolor))
	
	draw.rectangle([int(W-(W/5)), 0, W, int(H/5)], width=int(W/100), outline=bordercolor)
	
	#draw bottom left corner
	
	draw.rectangle([0, int(H-(H/5)),int(W/5),H], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor),fill=tuple(int(ti/1.5) for ti in bordercolor))
	
	draw.rectangle([0, int(H-(H/5)),int(W/5),H], width=int(W/100), outline=bordercolor)
		
	#draw bottom right corner
	
	draw.rectangle([int(W-(W/5)), int(H-(H/5)),W,H], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor),fill=tuple(int(ti/1.5) for ti in bordercolor))
	
	draw.rectangle([int(W-(W/5)), int(H-(H/5)),W,H], width=int(W/100), outline=bordercolor)
	
	draw.text((int(W/30), int((H/8)*2)), "R", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

	draw.text((int(W-(W/9)), int((H/8)*2)), "S", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black', )
	
	if ro[2]: draw.text((int(W/30), int((H/8)*3)), "M", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

	if so[2]: draw.text((int(W-(W/9)), int((H/8)*3)), "M", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black', )

	if ro[1]: draw.text((int(W/30), int((H/8)*4)), "F", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

	if so[1]: draw.text((int(W-(W/9)), int((H/8)*4)), "F", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black', )
	
	if ro[0]: draw.text((int(W/30), int((H/8)*5)), "NB", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

	if so[0]: draw.text((int(W-(W/6)), int((H/8)*5)), "NB", align='right', font=smallFont, fill='white', stroke_width=5, stroke_fill='black', )
			
			
def create(srg=[None,False,False],ps="They",pt="Them",cr=255,cg=255,cb=255,res=500,F=None,debug=False,gc=[[None,None,None],[None,None,None]],o=False):
        
    if srg[0] == None:
        if debug: print("None")
        x=input_srg()
        if debug: print(x[0])
        b=int(x[1])
        bs=x[0]
        bools=srgint_to_bools(b)
    else:
        if debug: print("srg arg: "+str(srg[0]))
        b=int(srg[0])
        bools=srgint_to_bools(b)
        bs=str(srg[0])
        if srg[1]:
            bs=bs+"?"
        if srg[2]:
            bs=bs+"*"
            
    so=[bools[0],bools[1],bools[2]]
    if debug: print(so)
    ro=[bools[3],bools[4],bools[5]]
    if debug: print(ro)
    if debug: print(bools)
    
    width = res
    height = width
    
    arr = np.zeros([height, width, 4], dtype=np.uint8)
    if o:
        gender_colour(bools,arr,width,height,True,gc[0],gc[1])

    else:
        gender_colour(bools,arr,width,height,True)
            
    if debug: print("Array created")
    temp=tempfile.NamedTemporaryFile(suffix=".png",delete=False)
    time.sleep(.2)
    name = str(temp.name)
    p=Path(temp.name)
    if debug: print("Tempfile created")
    
    img = Image.fromarray(arr)
    add_text(img,bs,width,height,(cr,cg,cb),so,ro,ps,pt)
    img.save(p)
    
    from imgurpython import ImgurClient
    client = ImgurClient("1ad9fa3c6cc700a", "a17ace1750e1e2c4610fed9ca65c2ee0778510af")
    request=client.upload_from_path(p, anon=True)
    print("Uploaded to "+request["link"])
    temp.close()
    os.remove(temp.name)
    return request["link"]
        

def main(imported=False):
    
    if imported: return
    
    y=pyip.inputInt("Byte: ")
    print("y for yes anything else for no")
    z=input("Trans: ")
    w=input("Questioning: ")
    if z in ["y","Y"]:
       z = True
    else:
        z = False
    if w in ["y","Y"]:
        w = True
    else:
        w = False

    override=input("Override Gender Color: ")

    R=[255, 105, 180, 255]
    L=[0, 191, 255, 255]

    if override != "":
            override=True
            gra=pyip.inputInt("Gender Left Red: ", blank=True)
            gga=pyip.inputInt("Gender Left Green: ", blank=True)
            gba=pyip.inputInt("Gender Left Blue: ", blank=True)
            
            if gra!="":
                L[0]=gra
            else:
                L[0]=0
            if gga!="":
                L[1]=gga
            else:
                L[1]=0
            if gba!="":
                L[2]=gba
            else:
                L[2]=0
                
            grb=pyip.inputInt("Gender Right Red: ", blank=True)
            ggb=pyip.inputInt("Gender Right Green: ", blank=True)
            gbb=pyip.inputInt("Gender Right Blue: ", blank=True)
        
            if gra!="":
                R[0]=grb
            else:
                R[0]=0
            if gga!="":
                R[1]=ggb
            else:
                R[1]=0
            if gba!="":
                R[2]=gbb
            else:
                R[2]=0
    
    r=pyip.inputInt("Border Red: ", blank=True)
    g=pyip.inputInt("Border Green: ", blank=True)
    b=pyip.inputInt("Border Blue: ", blank=True)
    print([r,g,b])


    if r=="":
        r=255
    elif r==0:
        r=0
    else:
        r=r%256
    print(r)
    
    if g=="":
        g=255
    elif g==0:
        g=0
    else:
        g=g%256
    print(g)
    
    if b=="":
        b=255
    elif b==0:
        b=0
    else:
        b=b%256
    print(b)
    
    size=pyip.inputInt("Resolution: ")
    
    second=input("Pronoun 1: ")
    third=input("Pronoun 2: ")
    
    x=create([int(y),w,z],second, third,r,g,b,size,gc=[L,R],o=True)

    input("press enter to continue")
    
i=True
if __name__ == "__main__":
   i=False
   
main(i)

