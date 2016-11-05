#coding=utf-8

from top.kernelpanic.core.html_parser import HtmlParser
from top.kernelpanic.core.html_downloader import HtmlDownloader
from top.kernelpanic.core.url_manager import UrlManager
from top.kernelpanic.util.db_helper import DBHelper

class CrawlDouBan(object):

    def __init__(self):
        self.dbhelper=DBHelper("douban")
        self.urlmanager=UrlManager()
        self.downloader=HtmlDownloader()
        self.parser=HtmlParser()

    def crawl_dou_ban(self,root_url):
        root_cont=self.downloader.download(root_url)
        tag_urls,tag_names=self.parser.parse_root_url(root_url,root_cont)

        tag_count=0
        book_count=0
        for tag_url,tag_name in zip(tag_urls,tag_names):
            tag_count+=1
            print "Count:%d Crawling tag %s from url %s" %(tag_count,tag_name,tag_url)
            if self.dbhelper.create_table(tag_name) is False:
                print "Table %s already exists!" %(tag_name)
                continue
            for i in range(0,1000,20):
                payload={'start':i,'type':'T'}
                tag_cont=self.downloader.download(tag_url,payload)
                detail_urs,flag=self.parser.parse_tag_url(tag_name,tag_cont)
                if flag is False:
                    break
                self.urlmanager.add_detail_urls(detail_urs)
            while(self.urlmanager.has_detail_url()):
                detail_url=self.urlmanager.get_detail_url()
                detail_cont=self.downloader.download(detail_url)
                book=self.parser.parse_detail_url(detail_url,detail_cont)
                if book is False:
                    continue
                book_count+=1
                print "Count:%d Crawling book %s from url %s" % (book_count, book['title'], detail_url)
                img_name=self.downloader.downloadImageFile(book['image'])
                book['image']=img_name
                if self.dbhelper.save_book(book) is False:
                    print "Book %s saved error!" %(book['title'])

        self.dbhelper.close()

if __name__=="__main__":
    root_url="https://book.douban.com/tag/"
    spider=CrawlDouBan()
    spider.crawl_dou_ban(root_url)
