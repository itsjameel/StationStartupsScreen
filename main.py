import textwrap
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import requests
fontFile = "./helveticaneuelt-arabic-55-roman.ttf"
imageFile = "/home/jameel/Coding/StationStartupsScreen/StationScreenTest-35.jpg"
textSize = 150
font = ImageFont.truetype(fontFile, textSize)
image = Image.open(imageFile)
myRequest = requests.get("https://admin.jameel.xyz/stationstartups").json()[22]
requestText = myRequest['descriptionar']
requestLogo = Image.open(requests.get(myRequest['logo'], stream=True).raw)
requestPhone = myRequest['phone']
requestEmail = myRequest['email']
descriptionText = requestText
descriptionWidth = 70
descriptionWrapped = textwrap.wrap(descriptionText, width=descriptionWidth)
descriptionWrapped = ' '.join(descriptionWrapped)
descriptionWrapped = descriptionWrapped.replace("         ", " ")
descriptionWrapped = textwrap.wrap(descriptionWrapped, width=descriptionWidth)
descriptionWrapped = '\n'.join(descriptionWrapped)
draw = ImageDraw.Draw(image)

draw.multiline_text((2800, 2300), descriptionWrapped, font=font, direction="rtl", align="right")


draw.text((650, 3200), requestPhone, font=font)

draw.text((650, 3540), requestEmail, font=font)


basewidth = 1500
wpercent = (basewidth/float(requestLogo.size[0]))
hsize = int((float(requestLogo.size[1])*float(wpercent)))
requestLogo = requestLogo.resize((basewidth,hsize), Image.ANTIALIAS)
image.paste(requestLogo, (6000, 730), mask=requestLogo)

image.convert('RGBA').save("output.png")