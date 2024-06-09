# coding=utf-8

import requests
import json
import re
from urllib import parse
import os
import time
from PIL import Image


class BaiduImageSpider(object):
    def __init__(self):
        self.page_count = 20  # 一个关键词请求20页-每页30张图
        self.req_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=10675405532307977043'\
                  '&ipn=rj&ct=201326592&is=&fp=result&fr='\
                  '&word={}&queryWord={}'\
                  '&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync='\
                  '&pn={}&rn=30&gsm=23a&1716904792716='
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
        }

    # 下载图片
    def save_image(self, img_url, img_name):
        ret_data = requests.get(img_url, headers=self.header)
        is_err = 0
        with open(img_name, "wb") as img_f:
            img_f.write(ret_data.content)
            print("save ok %s" % img_name)
            # 进行webP转jpeg
            try:
                wp_img = Image.open(img_name)
                jpeg_img = wp_img.convert('RGB')
                jpeg_img.save(img_name, 'JPEG')
            except:
                print("PIL err %s" % img_name)
                is_err = 1
                # os.remove(filename_down)
            else:
                print("PIL OK")
        if 1 == is_err:
            os.remove(img_name)  # 针对转换错误的进行删除

    # 获取图片下载URL
    def get_img_url(self, page_url):
        img_url_list = []
        print(page_url)
        ret_html = requests.get(page_url, headers=self.header)
        try:
            json_info = json.loads(ret_html.text)
        except:
            print("json.loads err")
        else:
            print("json.loads ok")
        for index in range(30):
            #print(json_info['data'][index]['thumbURL'])
            img_url_list.append(json_info['data'][index]['thumbURL'])

        return img_url_list

    # 入口函数
    def run(self):
        keyword = input("请输入搜索关键词:")
        keyword_urlencode = parse.quote(keyword)  # URL编码
        pic_num = 0

        filename = ".\{}"
        filename = filename.format(keyword)
        # 如果目录不存在则创建
        if not os.path.exists(filename):
            os.makedirs(filename)
        filename += r'\{}.jpg'

        for page in range(self.page_count):
            page_n = (page + 1) * 30
            page_url = self.req_url.format(keyword_urlencode, keyword_urlencode, page_n)
            img_list = self.get_img_url(page_url)
            for link in img_list:
                pic_num += 1
                filename_down = filename.format(pic_num)
                self.save_image(link, filename_down)
                time.sleep(0.2)
        print("----下载完成,共计 %d 张----" % pic_num)


if __name__ == '__main__':
    img_spider = BaiduImageSpider()
    img_spider.page_count = 1
    img_spider.run()
