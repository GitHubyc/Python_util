# -*- coding: utf-8 -*-

from PIL import Image
import pytesseract

#上面都是导包，只需要下面这一行就能实现图片文字识别

# text=pytesseract.image_to_string(Image.open('123.png'),lang='chi_sim') #设置为中文文字的识别

#text=pytesseract.image_to_string(Image.open('123.png'),lang='eng')  #设置为英文或阿拉伯字母的识别

img = Image.open('abc.jpg')
text = pytesseract.image_to_string(img, lang='eng')
print(text)
