#coding=utf-8

import requests
import time
import random

class HtmlDownloader(object):

    def __init__(self):
        self.headers={'Host': 'book.douban.com',
                 'Connection': 'keep-alive',
                 'Cache-Control': 'max-age=0',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                 'Referer': 'https://book.douban.com/tag/?icn=index-nav',
                 'Accept-Encoding': 'gzip, deflate, sdch, br',
                 'Accept-Language': 'zh-CN,zh;q=0.8',
				 'Cookie': 'bid=OIVDBBHR3ls; gr_user_id=e773e35a-fd82-4db6-b57e-d6decd3660eb; ll="118146"; ct=y; viewed="25862578_2064977_6082808_3124386_26425831_1082154_1200840_3826293_6152040_26821903"; _vwo_uuid_v2=523C2A5A919008A29110628A18320EB8|a12a4833b35c435dee9a9634a408df27; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1475499617%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ap=1; __utmt_douban=1; __utma=30149280.93992039.1474182719.1475492762.1475499617.36; __utmb=30149280.2.10.1475499617; __utmc=30149280; __utmz=30149280.1475470167.30.13.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utma=81379588.709195023.1474182719.1475492762.1475499617.30; __utmb=81379588.2.10.1475499617; __utmc=81379588; __utmz=81379588.1475462897.23.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.3ac3=026b5ce3bc96b3bf.1474182719.29.1475500394.1475493817.; _pk_ses.100001.3ac3=*'
        }
        self.proxies={
            'https':"http://127.0.0.1:1080"
        }

    def download(self,url,params=None):
        if url is None:
            return
        time.sleep(random.uniform(0,10))
        if params is None:
            return requests.get(url,headers=self.headers).text
        else:
            return requests.get(url,params=params,headers=self.headers).text

    def downloadImageFile(self,img_url):
        if img_url is None:
            return
        local_filename=img_url.split("/")[-1]
        result=requests.get(img_url,stream=True)
        time.sleep(random.uniform(0,10))
        with open("E:\images\%s" %local_filename,"wb") as f:
            for chunk in result.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()
        return local_filename
