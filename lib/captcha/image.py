import os.path
import random
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from io import StringIO

# font = ImageFont.load_default()
font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "captcha.ttf"), 32)

def gen_randoms():
    return ''.join(random.sample("abcdefghjkmnpqrstuvwzyzACDEFGHJKMNPQRSTUVWZY345679", 6))

def gen_captcha(text, form = 'jpeg'):
    im = Image.new("RGB", (32*len(text), max(font.getsize(text)[1], 48)), 0xffffff)

    draw = ImageDraw.Draw(im)
    posx = 0
    for char in text:
        draw.text((posx, 0), char, font = font, fill = 0x333333)
        posx = posx + font.getsize(char)[0] - 8

    im = im.transform(im.size, Image.PERSPECTIVE, [
        1-float(random.randint(1,2))/100,
        0, 0, 0,
        1-float(random.randint(1,10))/100, float(random.randint(1,2))/500, 0.001, float(random.randint(1,2))/500
        ])
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)

    bufs = StringIO()
    im.save(bufs, form)
    data = bufs.getvalue()
    bufs.close()

    return data
