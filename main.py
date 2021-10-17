import textwrap
import requests
import json
import html2text
import re
from Naked.toolshed.shell import execute_js, muterun_js

success = execute_js('index.js')

if success:
    print("done!")
else:
    print("nope")    

def readJSONfile():
    with open('data.json') as f:
        data = json.load(f)
        return data


def extractFacebookID(url):
        x = re.search("^(?:https?:\/\/)?(?:www\.|m\.|touch\.)?(?:facebook\.com|fb(?:\.me|\.com))\/(?!$)(?:(?:\w)*#!\/)?(?:pages\/)?(?:photo\.php\?fbid=)?(?:[\w\-]*\/)*?(?:\/)?(?:profile\.php\?id=)?([^\/?\s]*)(?:\/|&|\?)?.*$", url)
        if x: 
            return x.group(1)
        else:
            return None
    
def extractInstagramID(url):
    x = re.search("(?:(?:http|https):\/\/)?(?:www\.)?(?:instagram\.com|instagr\.am)\/([A-Za-z0-9-_\.]+)")
    if x:
        return x.group(1)
    else:
        return None

def getStartupData(index):
    global startup
    startup = readJSONfile()[index]
    print(startup)
    global request_text
    request_text = html2text.html2text((startup.get('description')))
    global startup_logo
    startup_logo = Image.open(requests.get(startup['logo'], stream=True).raw)
    global logoWidth
    logoWidth = startup.get('logoWidth')
    global startupLocation
    startupLocation = startup.get('location')
    global startupPhone
    startupPhone = startup.get('phone')
    global startupEmail
    startupEmail = startup.get('email')
    global startupFacebook
    startupFacebook = startup.get('facebook')
    global startupInstagram
    startupInstagram = startup.get('instagram')


startupQuantity = len(readJSONfile())

for i in range(0, startupQuantity):
    from PIL import ImageFont
    from PIL import Image
    from PIL import ImageDraw

    descriptionFontFile = "./fonts/helveticaneuelt-arabic-55-roman.ttf"
    infoFontFile = "./fonts/TradeGothicLTStd.otf"
    imageFile = "./StationScreenTest-35.jpg"

    textSize = 160
    infoSize = 140

    descriptionFont = ImageFont.truetype(descriptionFontFile, textSize)
    infoFont = ImageFont.truetype(infoFontFile, infoSize)
    image = Image.open(imageFile)
    draw = ImageDraw.Draw(image)
    getStartupData(i)
    descriptionText = request_text
    descriptionWidth = 60
    descriptionWrapped = textwrap.wrap(descriptionText, width=descriptionWidth)
    descriptionWrapped = ' '.join(descriptionWrapped)
    descriptionWrapped = descriptionWrapped.replace("         ", " ")
    descriptionWrapped = textwrap.wrap(descriptionWrapped, width=descriptionWidth)
    descriptionWrapped = '\n'.join(descriptionWrapped)

    textCoords = draw.multiline_textbbox((3200, 2300), descriptionWrapped, font=descriptionFont, direction="rtl", align="right", language="ar")

    finalX = 3200 + (7501 - textCoords[-2]) 

    draw.multiline_text((finalX, 2300), descriptionWrapped, font=descriptionFont, direction="rtl", align="right", language="ar")
    if startupLocation == 'Baghdad':
        draw.rectangle((7000, 730, 7500, 950))
        draw.text((7100, 650), "بغداد", font=descriptionFont, fill="white")
    elif startupLocation == 'Mosul':
        draw.rectangle((7000, 730, 7500, 950))
        draw.text((7060, 650), "موصل", font=descriptionFont, fill="white")

    def resizeImage(image, baseWidth):
        wpercent = (baseWidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        return image.resize((baseWidth,hsize), Image.ANTIALIAS)

    phoneIcon = Image.open("./assets/phone.png")
    emailIcon = Image.open("./assets/email.png")
    facebookIcon = Image.open("./assets/facebook.png")
    instagramIcon = Image.open("./assets/instagram.png")

    phoneIcon = resizeImage(phoneIcon, 175)
    emailIcon = resizeImage(emailIcon, 175)
    facebookIcon = resizeImage(facebookIcon, 175)
    instagramIcon = resizeImage(instagramIcon, 175)

    infoCoordsStart = 2810
    global infoCoordsList
    infoCoordsList = [
        {"id": "phone", "number": 3180},
    ]
    global findInInfoCoordsList
    def findInInfoCoordsList(id):
        thing = [item for item in infoCoordsList if item['id'] == id][0]
        return thing['number']

    def has_transparency(img):
        if img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True
        elif img.mode == "RGBA":
            extrema = img.getextrema()
            if extrema[3][0] < 255:
                return True

        return False

    if startupPhone:
        image.paste(phoneIcon, (400, infoCoordsList[-1]['number']), mask=phoneIcon)
        draw.text((650, findInInfoCoordsList('phone')+30), startupPhone, font=infoFont)

    if startupEmail:
        image.paste(emailIcon, (400, infoCoordsList[-1]['number']+370), mask=emailIcon)
        infoCoordsList.append({"id": "email", "number": infoCoordsList[-1]['number']+370})
        draw.text((650, findInInfoCoordsList('email')+30), startupEmail, font=infoFont)
    if startupFacebook:
        try: 
            if len(extractFacebookID(startupFacebook)) < 24:
                image.paste(facebookIcon, (400, infoCoordsList[-1]['number']+370), mask=facebookIcon)
                infoCoordsList.append({"id": "facebook", "number": infoCoordsList[-1]['number']+370})
                startupFacebook = extractFacebookID(startupFacebook)
                draw.text((650, findInInfoCoordsList('facebook')+30), startupFacebook, font=infoFont)
        except:
            pass

    if startupInstagram:
        try:
            if len(extractInstagramID(startupInstagram)) < 24:
                image.paste(instagramIcon, (400, infoCoordsList[-1]['number']+370), mask=instagramIcon)
                infoCoordsList.append({"id": "instagram", "number": infoCoordsList[-1]['number']+370})
                startupInstagram = startupInstagram.replace("https://www.instagram.com/", "")
                startupInstagram = startupInstagram.replace("/", "")
                draw.text((650, findInInfoCoordsList("instagram")+30), startupInstagram, font=infoFont)
        except:
            pass
    # draw.ellipse((7450, 2200, 7550, 2300), fill = 'blue', outline ='blue')
    if logoWidth:
        print("startup width exists!")
        startup_logo = resizeImage(startup_logo, int(1500*(logoWidth/100)))
    else:
        startup_logo = resizeImage(startup_logo, 1500)

    startup_logoWidth, startup_logoHeight = startup_logo.size


    logoBox = (5950, 700, 7450, 2200) #x1 y1 x2 y2

    logoBoxHeight = logoBox[3] - logoBox[1]
    logoPasteHeight = (730 + int((logoBoxHeight-startup_logoHeight) / 2))

    if logoWidth:
        sampleCoord = 5850+(1500-int(1500*(logoWidth/100)))
        print(sampleCoord)
    else:
        sampleCoord = 6000

    if has_transparency(startup_logo):
        image.paste(startup_logo, (sampleCoord, logoPasteHeight), mask=startup_logo)
    else:
        image.paste(startup_logo, (sampleCoord, logoPasteHeight))
    # print(f"./pics/{startup['name']}_output.png")
    image = image.resize((int(image.size[0]/4), int(image.size[1]/4)))
    image.convert('RGBA').save(f"./pics/{startup['name']}_output.png", optimize=True,quality=20)
    del Image
    del ImageDraw
    del ImageFont