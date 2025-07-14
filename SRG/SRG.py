import tempfile
from PIL import Image, ImageDraw, ImageFont
import pyinputplus as pyip
from os import system, name
import os
import time
import numpy as np
from pathlib import Path
import sys
from .Flags import Flagdir as Flags
from io import BytesIO

# Clears the terminal screen
def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')

# Converts SRG boolean list to a byte value
def srg_to_byte(srg, printbyte=False, printbit=False, printbitvalue=False):
    b = 1
    byte = 0
    for x in range(7, -1, -1):
        if srg[x] == True:
            byte += b
        if printbit: print(srg[x])
        if printbitvalue: print(b)    
        if b == 1:
            b = 2
        else:
            b = b * 2
    if printbyte: print(byte)
    return int(byte)

# Prompts user for SRG input and returns encoded values
def input_srg(printbyte=False, printbit=False, printbitvalue=False):
    srg = [
        "Are you sexually attracted to NBs?\n",
        "Are you sexually attracted to females?\n",
        "Are you sexually attracted to males?\n",
        "Are you romantically attracted to NBs?\n",
        "Are you romantically attracted to females?\n",
        "Are you romantically attracted to males?\n",
        "Do you identify as female?\n",
        "Do you identify as Male?\n"
    ]
    i = 7
    for x in range(0, 8):
        bit = pyip.inputMenu(['Yes', 'No'], lettered=False, numbered=True, prompt=srg[i], default="No", blank=True)
        if bit == "Yes":
            srg[i] = True
        else:
            srg[i] = False
        print(srg[i])
        time.sleep(0.1)
        clear()
        i -= 1
    byte = srg_to_byte(srg, printbyte, printbit, printbitvalue)
    trans = pyip.inputMenu(['Yes', 'No'], lettered=False, numbered=True, prompt="Do you wish to identify as trans\n", default="No", blank=True)
    questioning = pyip.inputMenu(['Yes', 'No'], lettered=False, numbered=True, prompt="Are you certain of your sexual/romantic orientation\n", default="Yes", blank=True)
    if trans == "Yes":
        trans = "*"
    else:
        trans = ""
    if questioning == "No":
        questioning = "?"
    else:
        questioning = ""
    combined = str(byte) + questioning + trans
    output = [combined, byte, questioning, trans]
    return output

# Converts SRG integer to boolean list
def srgint_to_bools(srg, debug=False):
    b = 128
    i = 0
    debugbyte = ["SNB", "SF", "SM", "RNB", "RF", "RM", "F", "M"]
    byte = [False, False, False, False, False, False, False, False]
    workingsrg = srg
    for y in range(0, 8):
        if workingsrg >= b:
            byte[i] = True
            if debug: print(workingsrg)
            workingsrg -= b
        elif workingsrg == 1:
            if debug: print(workingsrg)
            byte[7] = True
            workingsrg -= b
        i += 1
        b = int(b / 2)
        if b == 0:
            break
    if debug:
        print(debugbyte)
        print(byte)
    return byte

# Applies gender color to image background array
def gender_colour(x, array, width, height, p=False, lc=[0, 191, 255, 255], rc=[255, 105, 180, 255], O=False):
    '''applys gender colour to background'''
    if O:
        if p: print("OverRiddenColour")
        array[:, :int(width / 2)] = lc 
        array[:, int(width / 2):] = rc
        print(lc)
        print(rc)
    elif x[7] and x[6]:
        if p: print("NB")
        array[:, :int(width / 2)] = lc # blue
        array[:, int(width / 2):] = rc # pink
    elif x[7]:
        if p: print("Male")
        array[:, :] = [0, 191, 255, 255]
    elif x[6]:
        if p: print("Female")
        array[:, :] = [255, 105, 180, 255]
    else:
        if p: print("Agender")
        array[:, :] = [50, 50, 50, 255]
        
        
def create_save_upload(img: Image.Image, use_disk: bool = False) -> str:
    """
    Saves and uploads a PIL Image to Imgur. Returns the image URL.
    
    Args:
        img (PIL.Image): The image to save and upload.
        use_disk (bool): If True, saves to a temporary disk file. Otherwise uses memory.
        
    Returns:
        str: Imgur URL of uploaded image.
    """
    
    client_id = "1ad9fa3c6cc700a"
    headers = {'Authorization': f'Client-ID {client_id}'}

    if use_disk:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
            img.save(temp.name, format='PNG')
            path = Path(temp.name)
        
        with open(path, 'rb') as f:
            files = {'image': ('image.png', f.read())}
            response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files)
        
        os.remove(path)

    else:
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        files = {'image': ('image.png', buffer.getvalue())}
        response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files)

    response.raise_for_status()
    link = response.json()['data']['link']
    print("Uploaded to:", link)
    return link

# Adds text and decorations to the image
def add_text(im, text, W, H, bordercolor=(0,0,0), so=[False,False,False], ro=[False,False,False], p1="They", p2="Them", gt="", gp=False, pride1=None, pride2=None, pride3=None, pride4=None):
    bigFont = ImageFont.truetype("Font.ttf", int(W/4))
    smallFont = ImageFont.truetype("Font.ttf", int(W/10))
    draw = ImageDraw.Draw(im)
    bounding_box = [0, 0, W, H]
    x1, y1, x2, y2 = bounding_box

    # Replace draw.textsize with draw.textbbox for 'text'
    bbox = draw.textbbox((0, 0), text, font=bigFont)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), text, align='center', font=bigFont, fill='white', stroke_width=5, stroke_fill='black')

    # For 'gt'
    bbox = draw.textbbox((0, 0), gt, font=smallFont)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (W - w)/2
    y = H/15
    draw.text((x, y), gt, align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

    # For p1 + p2
    combined_text = p1 + " " + p2
    bbox = draw.textbbox((0, 0), combined_text, font=smallFont)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (W - w)/2
    y = H - (H/6)
    draw.text((x, y), combined_text, align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

    if gp != False:
        gpxstart = (W/5)
        gpxend = W-(W/5)
        gpystart = H-(H/20)
        gpyend = (H-(H/20))-(H/100)
        draw.rectangle([gpxstart,gpystart,gpxend,gpyend], width=int(W/100), outline=bordercolor)
        increment = (gpxend-gpxstart)/100
        markerwidth = W/30
        markerheight = W / 40
        markerxstart = (gpxstart+(increment*gp))-(markerwidth/2)
        markerxend = markerxstart+markerwidth
        markerystart = gpystart-(markerheight/2)
        markeryend = gpyend+(markerheight/2)
        draw.rectangle([markerxstart,markerystart,markerxend,markeryend], width=int(W/100), outline=(0,0,0,255))

    # Draw frame and corners
    draw.rectangle([x1, y1, x2, y2], width=int(W/50), outline=tuple(int(int(ti)/0.5) for ti in bordercolor))
    draw.rectangle([x1, y1, x2, y2], width=int(W/100), outline=bordercolor)
    draw.rectangle([0, 0, int(W/5), int(H/5)], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor), fill=tuple(int(ti/1.5) for ti in bordercolor))
    draw.rectangle([0, 0, int(W/5), int(H/5)], width=int(W/100), outline=bordercolor)

    # Pride images (if provided)
    def process_pride(pride_path, x_start, y_start):
        pride_img = Image.open(pride_path)
        size = (int(W/5.5), int(H/5))
        pride_img.thumbnail(size, Image.ANTIALIAS)
        loc = (int((int(int(W/5)) - pride_img.width) / 2) + x_start, int((int(int(H/5)) - pride_img.height) / 2) + y_start)
        im.paste(pride_img, loc)

    if pride1 is not None:
        process_pride(pride1, 0, 0)

    draw.rectangle([int(W-(W/5)), 0, W, int(H/5)], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor), fill=tuple(int(ti/1.5) for ti in bordercolor))
    draw.rectangle([int(W-(W/5)), 0, W, int(H/5)], width=int(W/100), outline=bordercolor)
    if pride2 is not None:
        boxlength = int(W/5)
        process_pride(pride2, W - boxlength, 0)

    draw.rectangle([0, int(H-(H/5)), int(W/5), H], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor), fill=tuple(int(ti/1.5) for ti in bordercolor))
    draw.rectangle([0, int(H-(H/5)), int(W/5), H], width=int(W/100), outline=bordercolor)
    if pride3 is not None:
        boxlength = int(W/5)
        boxheight = int(H/5)
        pridestartx = int((int(int(W/5)) - im.width) / 2)
        pridestarty = H - boxheight
        process_pride(pride3, 0, pridestarty)

    draw.rectangle([int(W-(W/5)), int(H-(H/5)), W, H], width=int(W/50), outline=tuple(int(int(ti)/1.5) for ti in bordercolor), fill=tuple(int(ti/1.5) for ti in bordercolor))
    draw.rectangle([int(W-(W/5)), int(H-(H/5)), W, H], width=int(W/100), outline=bordercolor)
    if pride4 is not None:
        boxlength = int(W/5)
        boxheight = int(H/5)
        pridestartx = W - boxlength
        pridestarty = H - boxheight
        process_pride(pride4, pridestartx, pridestarty)

    # Draw labels
    draw.text((int(W/30), int((H/8)*2)), "R", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
    draw.text((int(W-(W/9)), int((H/8)*2)), "S", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
    if ro[2]: draw.text((int(W/30), int((H/8)*3)), "M", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
    if so[2]: draw.text((int(W-(W/9)), int((H/8)*3)), "M", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
    if ro[1]: draw.text((int(W/30), int((H/8)*4)), "F", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
    if so[1]: draw.text((int(W-(W/9)), int((H/8)*4)), "F", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
    if ro[0]: draw.text((int(W/30), int((H/8)*5)), "NB", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
    if so[0]: draw.text((int(W-(W/6)), int((H/8)*5)), "NB", align='right', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
    
# Converts integer to Roman numeral string
def toNumeral(Number):
    runningtotal = Number
    output = ""
    while runningtotal > 0:
        if runningtotal >= 100:
            output += "C"
            runningtotal -= 100
        elif runningtotal >= 50:
            output += "L"
            runningtotal -= 50
        elif runningtotal >= 10:
            output += "X"
            runningtotal -= 10
        elif runningtotal == 9:
            output += "IX"
            runningtotal -= 9
        elif runningtotal == 8:
            output += "VIII"
            runningtotal -= 8
        elif runningtotal == 7:
            output += "VII"
            runningtotal -= 7
        elif runningtotal == 6:
            output += "VI"
            runningtotal -= 6
        elif runningtotal == 5:
            output += "V"
            runningtotal -= 5
        elif runningtotal == 4:
            output += "IV"
            runningtotal -= 4
        elif runningtotal == 3:
            output += "III"
            runningtotal -= 3
        elif runningtotal == 1:
            output += "II"
            runningtotal -= 2
        elif runningtotal == 1:
            output += "I"
            runningtotal -= 1
    return output

# Adds crest text and decorations to the image
def crest_text(im, text, W, H, so=[False, False, False], ro=[False, False, False], p1="They", p2="Them", gt="", gp=False, rn=True, Q=False, T=False, Trim=(255,255,255,255), Ad=(0,0,0,255)):
    print("crest text")
    if rn:
        text = int(text)
        text = toNumeral(text)
        if Q:
            text = str(text) + "?"
            print("Questioning")
        if T:
            text = str(text) + "*"
            print("Trans")
    else:
        text = int(text)
        if Q:
            text = str(text) + "?"
            print("Questioning")
        if T:
            text = str(text) + "*"
            print("Trans")
    text = str(text)
    print(text)
    print("Setting Fonts")
    bigFont = ImageFont.truetype("Numerals.ttf", int(W / 15))
    smallFont = ImageFont.truetype("Numerals.ttf", int(W / 25))
    draw = ImageDraw.Draw(im)
    print("Calculating bounding box")
    bounding_box = [0, 0, W, H]
    x1, y1, x2, y2 = bounding_box

    # Replace draw.textsize with draw.textbbox for 'text'
    bbox = draw.textbbox((0, 0), text, font=bigFont)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (x2 - x1 - w) / 2 + x1
    y = (y2 - y1 - h) / 2 + y1
    print("Drawing SRG")
    draw.text((x, y), text, align='center', font=bigFont, fill='white', stroke_width=5, stroke_fill='black')

    # For gt
    bbox = draw.textbbox((0, 0), gt, font=smallFont)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (W - w) / 2
    y = H / 3.5
    print("Drawing gendertext")
    draw.text((x, y), gt, align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

    # For p1 + p2 pronouns
    combined_text = p1 + " " + p2
    bbox = draw.textbbox((0, 0), combined_text, font=smallFont)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (W - w) / 2
    y = H - (H / 3)
    print("Drawing pronouns")
    draw.text((x, y), combined_text, align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

    print("Drawing R")
    draw.text((int(W / 3.2), int((H / 6.5) * 2)), "R", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

    print("Drawing S")
    draw.text((int(W - (W / 2.9)), int((H / 6.5) * 2)), "S", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')

    if ro[2]: 
        draw.text((int(W / 3.2), int((H / 7) * 3)), "M", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
        print("Drawing RN")

    if so[2]: 
        draw.text((int(W - (W / 2.8)), int((H / 7) * 3)), "M", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
        print("Drawing SN")

    if ro[1]: 
        draw.text((int(W / 3.2), int((H / 8) * 4)), "F", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
        print("Drawing RF")

    if so[1]: 
        draw.text((int(W - (W / 2.9)), int((H / 8) * 4)), "F", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
        print("Drawing SF")

    if ro[0]: 
        draw.text((int(W / 3.2), int((H / 8.8) * 5)), "NB", align='center', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
        print("Drawing RM")

    if so[0]: 
        draw.text((int(W - (W / 2.7)), int((H / 8.8) * 5)), "NB", align='right', font=smallFont, fill='white', stroke_width=5, stroke_fill='black')
        print("Drawing SM")

    if gp != False:
        barheight = H / 200
        gpxstart = (W / 2.5) - 10
        gpxend = W - (W / 2.5)
        gpystart = H - (H / 2.8)
        gpyend = gpystart + barheight
        draw.rectangle([gpxstart, gpystart, gpxend, gpyend], width=int(W / 100), fill=Ad)
        increment = (gpxend - gpxstart) / 100
        markerwidth = W / 100
        markerheight = H / 100
        markerxstart = (gpxstart + (increment * gp)) - (markerwidth / 2)
        markerxend = markerxstart + markerwidth
        markerystart = gpystart - (markerheight / 2)
        markeryend = gpyend + (markerheight / 2)
        draw.rectangle([markerxstart, markerystart, markerxend, markeryend], width=int(W / 100), fill=Trim)

# Creates crest image, colors it, adds text, uploads to Imgur
def crest(SRG=[255,True,True],p1="P1",p2="P2",gt="Gender",rn=True,o=False,bgl=(0,191,255,255),bgr=(255,105,180,255),trim=(218,165,32,255),wings=(0,0,0,255),ad=(255,255,255,255),glow=(218,165,32,75),gp=False,s=950):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    i = np.asarray(Image.open(os.path.join(script_dir, 'Crest500.png')))
    im = Image.fromarray(np.uint8(i))
    width = im.width
    height = im.height
    x = srgint_to_bools(SRG[0])
    ro = [x[0], x[1], x[2]]
    so = [x[3], x[4], x[5]]
    # Set colors based on gender
    if o:
        print("custom colour")
    elif x[7] and x[6]:
        print("NB colour")
        bgl = (0, 191, 255, 255)
        bgr = (255, 105, 180, 255)
    elif x[7]:
        print("Male colour")
        bgl = (0, 191, 255, 255)
        bgr = (0, 191, 255, 255)
    elif x[6]:
        print("Female colour")
        bgl = (255, 105, 180, 255)
        bgr = (255, 105, 180, 255)
    else:
        print("Agender colour")
        bgl = (50, 50, 50, 255)
        bgr = (50, 50, 50, 255)
    # Color pixels
    for x in range(0, width):
        for y in range(0, height):
            current_color = im.getpixel((x, y))
            if current_color[3] > 20:
                if current_color[0] >= 250 and current_color[1] >= 250 and current_color[2] >= 250:
                    new_color = glow
                elif current_color[0] >= 250 and current_color[1] == 0 and current_color[2] == 0:
                    if x > width/2.03:
                        new_color = bgr
                    else:
                        new_color = bgl
                elif current_color[1] >= 250 and current_color[0] == 0 and current_color[2] == 0:
                    new_color = trim
                elif current_color[2] >= 250 and current_color[0] == 0 and current_color[1] == 0:
                    new_color = ad
                else:
                    new_color = wings
            else:
                new_color = False
            if new_color != False:
                im.putpixel((x, y), new_color)
    print("Completed Colouring")
    crest_text(im, SRG[0], im.width, im.height, ro=ro, so=so, p1=p1, p2=p2, gt=gt, gp=gp, Q=SRG[1], T=SRG[2], rn=rn, Trim=trim, Ad=ad)
    print("Text Added")
    
    """
    temp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    name = str(temp.name)
    p = Path(temp.name)
    """
    wpercent = (s / float(im.size[0]))
    hsize = int((float(im.size[1]) * float(wpercent)))
    img = im.resize((s, hsize), Image.Resampling.LANCZOS)
    debugsize = [img.width, "x", img.height]
    print(debugsize)
    print("Saving")
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    print("Saved Uploading")
    import requests

    headers = {
        'Authorization': 'Client-ID 1ad9fa3c6cc700a'
    }

    data = {
        'type': 'file'
    }

    files = {
        'image': ('image.png', img_bytes.getvalue())
    }

    res = requests.post('https://api.imgur.com/3/upload', headers=headers, data=data, files=files)
    res.raise_for_status()
    link = res.json()['data']['link']
    print("Uploaded to", link)
    
    return link

# Creates SRG image, adds text, uploads to Imgur or Cloudinary
def create(srg=[None,False,False],ps="They",pt="Them",cr=255,cg=255,cb=255,res=500,F=None,debug=False,gc=[[None,None,None],[None,None,None]],o=False,gt="",gp=False,pride1=None,pride2=None,pride3=None,pride4=None):
    if srg[0] == None:
        if debug: print("None")
        x = input_srg()
        if debug: print(x[0])
        b = int(x[1])
        bs = x[0]
        bools = srgint_to_bools(b)
    else:
        if debug: print("srg arg: "+str(srg[0]))
        b = int(srg[0])
        bools = srgint_to_bools(b)
        bs = str(srg[0])
        if srg[1]:
            bs = bs + "?"
        if srg[2]:
            bs = bs + "*"
    so = [bools[0], bools[1], bools[2]]
    if debug: print(so)
    ro = [bools[3], bools[4], bools[5]]
    if debug: print(ro)
    if debug: print(bools)
    width = res
    height = width
    arr = np.zeros([height, width, 4], dtype=np.uint8)
    if o:
        gender_colour(bools, arr, width, height, True, gc[0], gc[1], True)
    else:
        gender_colour(bools, arr, width, height, True)
    if debug: print("Array created")
    
    """
    temp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    time.sleep(.2)
    name = str(temp.name)
    p = Path(temp.name)
    if debug: print("Tempfile created")
    """
    
    
    img_bytes = BytesIO()
    
    
    img = Image.fromarray(arr)
    add_text(img, bs, width, height, (cr, cg, cb), so, ro, ps, pt, gt, gp=gp, pride1=pride1, pride2=pride2, pride3=pride3, pride4=pride4)
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    
    try:
        IFail = False
        """
        from imgurpython import ImgurClient
        client = ImgurClient("1ad9fa3c6cc700a", "a17ace1750e1e2c4610fed9ca65c2ee0778510af")
        request = client.upload_from_path(p, anon=True)"""
        
        import requests
        headers = {
            'Authorization': 'Client-ID 1ad9fa3c6cc700a'
        }

        data = {
            'type': 'file'
        }

        files = {
            'image': ('image.png', img_bytes.getvalue())
        }
        
        res = requests.post('https://api.imgur.com/3/upload', headers=headers, data=data, files=files)
        res.raise_for_status()
        link = res.json()['data']['link']
        print("Uploaded to", link)
        return link
    
        
    except Exception as error:
        print("Failed Upload", error)
        return "Failed Upload"
    
# Main function for interactive CLI
def main(imported=False):
    if imported: return
    y = pyip.inputInt("Byte: ")
    print("y for yes anything else for no")
    z = input("Trans: ")
    w = input("Questioning: ")
    if z in ["y", "Y"]:
       z = True
    else:
        z = False
    if w in ["y", "Y"]:
        w = True
    else:
        w = False
    override = input("Override Gender Color: ")
    R = [255, 105, 180, 255]
    L = [0, 191, 255, 255]
    if override != "":
        override = True
        gra = pyip.inputInt("Gender Left Red: ", blank=True)
        gga = pyip.inputInt("Gender Left Green: ", blank=True)
        gba = pyip.inputInt("Gender Left Blue: ", blank=True)
        if gra != "":
            L[0] = gra
        else:
            L[0] = 0
        if gga != "":
            L[1] = gga
        else:
            L[1] = 0
        if gba != "":
            L[2] = gba
        else:
            L[2] = 0
        grb = pyip.inputInt("Gender Right Red: ", blank=True)
        ggb = pyip.inputInt("Gender Right Green: ", blank=True)
        gbb = pyip.inputInt("Gender Right Blue: ", blank=True)
        if gra != "":
            R[0] = grb
        else:
            R[0] = 0
        if gga != "":
            R[1] = ggb
        else:
            R[1] = 0
        if gba != "":
            R[2] = gbb
        else:
            R[2] = 0
    r = pyip.inputInt("Border Red: ", blank=True)
    g = pyip.inputInt("Border Green: ", blank=True)
    b = pyip.inputInt("Border Blue: ", blank=True)
    print([r, g, b])
    if r == "":
        r = 255
    elif r == 0:
        r = 0
    else:
        r = r % 256
    print(r)
    if g == "":
        g = 255
    elif g == 0:
        g = 0
    else:
        g = g % 256
    print(g)
    if b == "":
        b = 255
    elif b == 0:
        b = 0
    else:
        b = b % 256
    print(b)
    size = pyip.inputInt("Resolution: ")
    second = input("Pronoun 1: ")
    third = input("Pronoun 2: ")
    gt = input("Gender Text: ")
    print("Type c for crest anything else")
    ty = input("Type: ")
    gp = input("Genital Preference")
    try:
        gp = int(gp)
    except:
        gp = False
    if ty == "c":
        y = crest(SRG=[253,False,False],rn=False,p2="Him",p1="He",gt="Male",o=True,bgl=(180, 0, 0, 255), bgr=(36, 36, 36, 255), trim=(218,165,32,255), wings=(0, 0, 0, 255),
          ad=(255, 255, 255, 255), glow=(218,165,32,75),gp=gp)
    else:
        choices = []
        paths = []
        for flag in Flags.FlagList:
            choices.append(flag[1])
            paths.append(flag[2])
        print(Flags.getflags())
        flag = pyip.inputMenu(choices, "Pick a flag", numbered=True)
        index = choices.index(flag)
        flag = paths[index]
        flag2 = pyip.inputMenu(choices, "Pick a flag", numbered=True)
        index = choices.index(flag2)
        flag2 = paths[index]
        flag3 = pyip.inputMenu(choices, "Pick a flag", numbered=True)
        index = choices.index(flag3)
        flag3 = paths[index]
        flag4 = pyip.inputMenu(choices, "Pick a flag", numbered=True)
        index = choices.index(flag4)
        flag4 = paths[index]
        print(flag)
        print(flag2)
        print(flag3)
        print(flag4)
        x = create([int(y), w, z], second, third, r, g, b, size, gc=[L, R], o=True, gt=gt, gp=gp, pride1=flag, pride2=flag2, pride3=flag3, pride4=flag4)
    input("press enter to continue")

# Entry point
i = True
if __name__ == "__main__":
   i = False
main(i)
