import textwrap
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import requests
fontFile = "./helveticaneuelt-arabic-55-roman.ttf"
imageFile = "/home/jameel/Coding/StationStartupsScreen/StationScreenTest-35.jpg"
textSize = 170
infoSize = 150
descriptionFont = ImageFont.truetype(fontFile, textSize)
infoFont = ImageFont.truetype(fontFile, infoSize)
image = Image.open(imageFile)
myRequest = requests.get("https://admin.jameel.xyz/stationstartups").json()[15]
requestText = myRequest['descriptionar']
requestLogo = Image.open(requests.get(myRequest['logo'], stream=True).raw)
requestPhone = myRequest['phone']
requestEmail = myRequest['email']
descriptionText = requestText
print(len(descriptionText))
descriptionWidth = 60
descriptionWrapped = textwrap.wrap(descriptionText, width=descriptionWidth)
descriptionWrapped = ' '.join(descriptionWrapped)
descriptionWrapped = descriptionWrapped.replace("         ", " ")
descriptionWrapped = textwrap.wrap(descriptionWrapped, width=descriptionWidth)
descriptionWrapped = '\n'.join(descriptionWrapped)
draw = ImageDraw.Draw(image)
print(descriptionWrapped)
if len(descriptionText) < 300:
    draw.multiline_text((3200, 2300), descriptionWrapped, font=descriptionFont, direction="rtl", align="right", language="ar")
elif len(descriptionText) > 300 and len(descriptionText) < 400:
    draw.multiline_text((3000, 2300), descriptionWrapped, font=descriptionFont, direction="rtl", align="right", language="ar")
elif len(descriptionText) > 400:
    draw.multiline_text((3000, 2300), descriptionWrapped, font=descriptionFont, direction="rtl", align="right", language="ar")
    

draw.text((650, 3200), requestPhone, font=infoFont)

draw.text((650, 3540), requestEmail, font=infoFont)

basewidth = 1500
wpercent = (basewidth/float(requestLogo.size[0]))
hsize = int((float(requestLogo.size[1])*float(wpercent)))
requestLogo = requestLogo.resize((basewidth,hsize), Image.ANTIALIAS)
image.paste(requestLogo, (6000, 730), mask=requestLogo)

image.convert('RGBA').save("output.png")