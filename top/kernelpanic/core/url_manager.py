#coding=utf-8

class UrlManager(object):

    def __init__(self):
        self.detail_urls=set()
        self.old_detail_urls=set()

    def add_detail_url(self,url):
        if url is None:
            return
        if url not in self.detail_urls and url not in self.old_detail_urls:
            self.detail_urls.add(url)

    def add_detail_urls(self,urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.add_detail_url(url)

    def has_detail_url(self):
        return len(self.detail_urls)!=0

    def get_detail_url(self):
        url=self.detail_urls.pop()
        self.old_detail_urls.add(url)
        return url
