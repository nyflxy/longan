# -*- coding: utf-8 -*-
#
# @author: HuShuLong
# Created on 2016-07-18
#

import pdb
from dhuicredit.app import get_options
options = get_options()

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def text_watermark(img_data , text , angle=23 , opacity=0.40):
    # 指定上传图片最大宽度580和高宽600，如超过进行resize
    if img_data.size[0] > 580:
        img_data = img_data.resize((580, img_data.size[1]/(img_data.size[0]/580)),Image.ANTIALIAS)

    if img_data.size[1] > 600:
        img_data = img_data.resize((img_data.size[0]/(img_data.size[1]/600),600),Image.ANTIALIAS)
    watermark = Image.new('RGBA', img_data.size) # 一层白色的膜
    size = 36
    FONT = options.root_path + "/static/font/msyh.ttf"
    n_font = ImageFont.truetype(FONT, size)                                       #得到字体
    n_width, n_height = n_font.getsize(text)
    text_box = min(watermark.size[0], watermark.size[1])
    while (n_width + n_height <  text_box):
        size += 2
        n_font = ImageFont.truetype(FONT, size=size)
        n_width, n_height = n_font.getsize(text)                                   #文字逐渐放大，但是要小于图片的宽高最小值

    text_width = (watermark.size[0] - n_width) / 2
    text_height = (watermark.size[1] - n_height) / 2
    draw = ImageDraw.Draw(watermark, 'RGBA')                                       #在水印层加画笔
    draw.text((text_width,text_height),
              unicode(text,'utf-8'), font=n_font, fill="#21ACDA")
    watermark = watermark.rotate(angle, Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    return Image.composite(watermark,img_data,watermark)
    print u"文字水印成功"
