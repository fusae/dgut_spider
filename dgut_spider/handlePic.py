from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import os
import io
import requests

#path = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/yzm.gif'
def handle(content):
    img = Image.open(io.BytesIO(content))
    img = img.convert('RGBA')
    pix = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                pix[x, y] = (0, 0, 0, 255)
            else:
                pix[x, y] = (255, 255, 255, 255)

    img.save('temp.jpg')

    im = Image.open("temp.jpg")
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save('temp2.jpg')
    text = pytesseract.image_to_string(Image.open('temp2.jpg'))

    os.remove('temp.jpg')
    os.remove('temp2.jpg')

    return text



if __name__ == '__main__':
    r = requests.get('http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx')
    yzm = handle(r.content)
    print(yzm)
