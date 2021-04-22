import textwrap
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import requests
descriptionFontFile = "./fonts/helveticaneuelt-arabic-55-roman.ttf"
infoFontFile = "./fonts/trade-gothic-lt-std-bold-condensed-no-20.otf"
imageFile = "./StationScreenTest-35.jpg"
textSize = 160
infoSize = 150
descriptionFont = ImageFont.truetype(descriptionFontFile, textSize)
infoFont = ImageFont.truetype(infoFontFile, infoSize)
image = Image.open(imageFile)
draw = ImageDraw.Draw(image)

def getStartupData(index):
    myRequest = requests.get("https://admin.jameel.xyz/stationstartups").json()[index]
    global requestText
    requestText = myRequest['descriptionar']
    global requestLogo
    requestLogo = Image.open(requests.get(myRequest['logo'], stream=True).raw)
    global requestPhone
    requestPhone = myRequest['phone']
    global requestEmail
    requestEmail = myRequest['email']

getStartupData(3)

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

draw.text((650, 3300), requestPhone, font=infoFont)
draw.text((650, 3640), requestEmail, font=infoFont)


basewidth = 1500
wpercent = (basewidth/float(requestLogo.size[0]))
hsize = int((float(requestLogo.size[1])*float(wpercent)))
requestLogo = requestLogo.resize((basewidth,hsize), Image.ANTIALIAS)
image.paste(requestLogo, (6000, 730), mask=requestLogo)

image.convert('RGBA').save("output.png")