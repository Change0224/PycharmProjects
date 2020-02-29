import os

import requests
from PIL import Image


def prase_img():

    os.makedirs('./image/', exist_ok=True)
    file_list = []
    for page in range(1,46):
        url = 'https://book.yunzhan365.com/gmze/ieqj/files/mobile/{}.jpg'.format(page)
        req = requests.get(url)
        with open('./image/page{}.jpg'.format(page), 'wb') as f:
            f.write(req.content)
            f.close()
            file_list.append('./image/page{}.jpg'.format(page))
    return file_list

def mk_book(file_list):
    print(file_list)
    im_list = []
    im1 = Image.open(file_list[0])
    file_list.pop(0)
    for i in file_list:
        img = Image.open(i)
        # im_list.append(Image.open(i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save("book.pdf", "PDF", resolution=100.0, save_all=True, append_images=im_list)
    print("输出文件名称：", "book.pdf")

if __name__ == '__main__':
    file_list = prase_img()
    mk_book(file_list)