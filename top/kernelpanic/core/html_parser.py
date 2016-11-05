#coding=utf-8

from bs4 import BeautifulSoup
import urlparse
import re

class HtmlParser(object):

    def __init__(self):
        self.score_limit=8.6
        self.person_limit=1024

    def parse_root_url(self,root_url,root_cont):
        if root_url is None:
            return
        tag_urls=[]
        tag_names=[]
        soup=BeautifulSoup(root_cont,"html.parser")
        tags=soup.select("#content > div > div.article > div > div > table > tbody > tr > td > a")
        for tag in tags:
            url=urlparse.urljoin(root_url,tag['href'])
            tag_urls.append(url)
            tag_names.append(tag.get_text())
        return tag_urls,tag_names

    def parse_author_info(self,str):
        if str[0]=='[':
            pos=str.index(']')
            country=str[1:pos]
            author=str[pos+1:]
        elif str[0]=='(':
            pos=str.index(')')
            country=str[1:pos]
            author=str[pos+1:]
        else:
            country="中国".decode('utf-8')
            author=str
        return country,author.strip()

    def parse_price(self,str):
        return re.match(".*?(\d+).*?",str).group(1)

    def parse_date(self,str):
        result=re.match("(\d+)-(\d+).*?",str)
        if result:
            date="%s-%02d-00".decode('utf-8') %(result.group(1),int(result.group(2).encode('utf-8')))
        else:
            date="0000-00-00".decode('utf-8')
        return date

    def parse_tag_url(self,tag_name,tag_page_cont):
        detail_urls=set()
        soup=BeautifulSoup(tag_page_cont,"html.parser")
        titles = soup.select("#subject_list > ul > li > div.info > h2 > a")
        scores = soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.rating_nums")
        persons = soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.pl")
        flag=False
        for title,score,person in zip(titles,scores,persons):
            flag=True
            try:
                score = score.get_text()
                person=person.get_text().split()[0]
                person=person[1:len(person)-4]
                if float(score) < self.score_limit or int(person) < self.person_limit:
                    continue
                url=title['href']+'#'+tag_name
                detail_urls.add(url)
            except Exception:
                pass
        return detail_urls,flag

    def parse_detail_url(self,detail_url,detail_cont):
        soup=BeautifulSoup(detail_cont,"html.parser")
        try:
            title = soup.select("#wrapper > h1 > span")[0].get_text()
            author = soup.select("#info > span > a")[0].get_text()
            country, author = self.parse_author_info(author)
            isbn=soup.find(class_="pl",text="ISBN:").next_sibling.strip()
            page_num=soup.find(class_="pl",text="页数:").next_sibling.strip()
            price = soup.find(class_='pl', text="定价:").next_sibling.strip()
            price=self.parse_price(price)
            tag=detail_url.split('#')[1]
            score=soup.select("#interest_sectl > div > div.rating_self.clearfix > strong")[0].get_text().strip()
            reader_num=soup.select("#interest_sectl > div > div.rating_self.clearfix > div > div.rating_sum > span > a > span")[0].get_text()
            publisher = soup.find(class_='pl', text="出版社:").next_sibling.strip()
            publish_date = soup.find(class_='pl', text="出版年:").next_sibling.strip()
            publish_date =self.parse_date(publish_date)
            image = soup.select("#mainpic > a > img")[0]['src']
            book_info=""
            author_info=""
            if len(soup.select("div[class='intro']"))==2:
                intro = soup.select("div[class='intro']")[0].find_all('p')
                for i in intro:
                    book_info += i.text + '\n'
                intro = soup.select("div[class='intro']")[1].find_all('p')
                for i in intro:
                    author_info += i.text + '\n'
            elif len(soup.select("div[class='intro']"))==3:
                intro = soup.select("div[class='intro']")[1].find_all('p')
                for i in intro:
                    book_info+=i.text+'\n'
                intro=soup.select("div[class='intro']")[2].find_all('p')
                for i in intro:
                    author_info+=i.text+'\n'
        except Exception:
            return False

        book={
            'title':title,
            'author':author,
            'country':country,
            'isbn':isbn,
            'page_num':page_num,
            'price':price,
            'tag':tag,
            'score':score,
            'reader_num':reader_num,
            'publisher':publisher,
            'publish_date':publish_date,
            'image':image,
            'book_info':book_info,
            'author_info':author_info
        }
        return book
