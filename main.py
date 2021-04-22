import textwrap
import requests

def getStartupData(index):
    global myRequest
    myRequest = requests.get("https://admin.jameel.xyz/stationstartups").json()[index]
    global requestText
    requestText = myRequest['descriptionar']
    global requestLogo
    requestLogo = Image.open(requests.get(myRequest['logo'], stream=True).raw)
    global requestPhone
    requestPhone = myRequest['phone']
    global requestEmail
    requestEmail = myRequest['email']
    global requestFacebook
    requestFacebook = myRequest['facebook']
    global requestInstagram
    requestInstagram = myRequest['instagram']


startupQuantity = len(requests.get("https://admin.jameel.xyz/stationstartups").json())
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
    print(myRequest['name'])
    descriptionText = requestText
    descriptionWidth = 60
    descriptionWrapped = textwrap.wrap(descriptionText, width=descriptionWidth)
    descriptionWrapped = ' '.join(descriptionWrapped)
    descriptionWrapped = descriptionWrapped.replace("         ", " ")
    descriptionWrapped = textwrap.wrap(descriptionWrapped, width=descriptionWidth)
    descriptionWrapped = '\n'.join(descriptionWrapped)

    textCoords = draw.multiline_textbbox((3200, 2300), descriptionWrapped, font=descriptionFont, direction="rtl", align="right", language="ar")

    finalX = 3200 + (7501 - textCoords[-2]) 

    draw.multiline_text((finalX, 2300), descriptionWrapped, font=descriptionFont, direction="rtl", align="right", language="ar")

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

    if requestPhone:
        image.paste(phoneIcon, (400, 3180), mask=phoneIcon)

    if requestEmail:
        image.paste(emailIcon, (400, 3550), mask=emailIcon)

    if requestFacebook:
        image.paste(facebookIcon, (400, 3900), mask=facebookIcon)

    if requestInstagram:
        image.paste(instagramIcon, (400, 4270), mask=instagramIcon)

    if requestPhone:
        draw.text((650, 3230), requestPhone, font=infoFont)
    if requestEmail:
        draw.text((650, 3570), requestEmail, font=infoFont)
    if requestFacebook:
        requestFacebook = requestFacebook.replace("https://www.facebook.com/", "")
        requestFacebook = requestFacebook.replace("/", "")
        draw.text((650, 3920), requestFacebook, font=infoFont)
    if requestInstagram:
        requestInstagram = requestInstagram.replace("https://www.instagram.com/", "")
        requestInstagram = requestInstagram.replace("/", "")
        draw.text((650, 4300), requestInstagram, font=infoFont)


    requestLogo = resizeImage(requestLogo, 1500)
    if myRequest['logo'][-3:] == 'png':
        image.paste(requestLogo, (6000, 730), mask=requestLogo)
    else:
        image.paste(requestLogo, (6000, 730))

    image.convert('RGBA').save(f"./pics/{myRequest['name']}_output.png")

    del Image
    del ImageDraw
    del ImageFont