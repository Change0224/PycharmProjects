#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 2.py
# @Author: huifer
# @Date  : 2018/8/20
from PIL import Image
import os


def rea(pdf_name):
    file_list = os.listdir('.')
    pic_name = []
    im_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)

    pic_name.sort()
    new_pic = []

    for x in pic_name:
        if "jpg" in x:
            new_pic.append(x)

    for x in pic_name:
        if "png" in x:
            new_pic.append(x)

    print("hec", new_pic)

    im1 = Image.open(new_pic[0])
    new_pic.pop(0)
    for i in new_pic:
        img = Image.open(i)
        # im_list.append(Image.open(i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    print("输出文件名称：", pdf_name)


if __name__ == '__main__':
    tttt = """

  _____ _____ _____   _______ ____    _____  _____  ______ 
 |  __ \_   _/ ____| |__   __/ __ \  |  __ \|  __ \|  ____|
 | |__) || || |         | | | |  | | | |__) | |  | | |__   
 |  ___/ | || |         | | | |  | | |  ___/| |  | |  __|  
 | |    _| || |____     | | | |__| | | |    | |__| | |     
 |_|   |_____\_____|    |_|  \____/  |_|    |_____/|_|     


"""
    print(tttt)
    print("制作者QQ:1187982580")
    pdf_name = input("请输入合成PDF文件名称：")
    if ".pdf" in pdf_name:
        rea(pdf_name=pdf_name)
    else:
        rea(pdf_name="{}.pdf".format(pdf_name))
    input("按任意键结束")
