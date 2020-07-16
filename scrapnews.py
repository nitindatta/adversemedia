from bs4 import BeautifulSoup
from readability import Document
import urllib
import requests
from urllib.parse import urlparse
from extractarticle import ExtractArticle
import re
import logging
from requests.exceptions import Timeout

IGNORE_LIST = r'wikipedia.org|books.google|linkedin|monster|jobstreet.com|wisdomjobs|naukari|sec.gov|sec.report|dl.bourse|fintel.io|ftp.cs.princeton.edu'
IGNORE_LINKS_LIST = r'Annual|Financial-Report'
# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

GOOGLE_CLASS='gG0TJc'
class ScrapNews:
    links=[]
    link=''
    errorcount=0
    ingnorelist=re.compile(IGNORE_LIST)
    ingnorelink=re.compile(IGNORE_LINKS_LIST)
    logger = logging.getLogger(__name__)
    def __init__(self):
        #logger = logging.getLogger(__name__)
        print (__name__)
        #print(logger)

    def scrapEntity(self,id,pageno,keyword):
        
        #query =  keyword +'+"' +entity +'"'
        #query = query.replace(' ', '+')
        print(str(pageno))
        query="{0}&sxsrf=ALeKk03SaWrEuh1vZDxLQXk1bJUIwMSzIA:1594109560695&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjaluTw2LrqAhXb8XMBHempA28Q_AUoAXoECBQQAw&biw=1280&bih=578&start={1}".format(keyword,str(pageno))
        URL = f"https://google.com/search?q={query}"
        #ingnorelist=('.wikipedia.org','.books.google.*')
        print("running query=" +URL)
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers,timeout=3)            
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content,features="lxml")    

            results = []
            #check for trusted new site and implement custom logic for parsing.
            # for rest use library to get text as required.
            
            for g in soup.find_all('div', class_='dbsr'):
                anchors = g.find_all('a')
                if anchors:            
                    link = anchors[0]['href']
                    parsed_uri = urlparse(link)
                    #optimize further to handle ignore url's
                    if not(link in self.links
                        or parsed_uri.path.lower().endswith('.pdf') 
                        or self.ingnorelist.search(parsed_uri.netloc.lower()) 
                        or link.lower().endswith('pdf')
                        or self.ingnorelink.search(link)):
                        extractarticle = ExtractArticle()
                        print ('--------Extracting Link: '+ link)
                        try:
                            article = extractarticle.extractArticle(link)
                            if (article is None):
                                self.errorcount=self.errorcount+1
                                self.logger.error("Error Processing Article for entity %s and link %s",pageno,link)
                                continue
                        except (requests.ConnectionError,requests.ConnectTimeout,requests.ReadTimeout):
                            self.errorcount=self.errorcount+1
                            self.logger.error("Connection Error While processing %s and link %s",pageno,link)
                        else:       
                            extractedSummary=article.summary
                            extractedTitle=article.title
                            summarytext = BeautifulSoup(extractedSummary,features="lxml").get_text().rstrip("\n")
                                       
                            # title = g.find('h3').text
                            # item = {
                            #     "title": title,
                            #     "link": link
                            # }
                            self.links.append(link)
                            yield [id,pageno,keyword.strip('"'),link,extractedTitle, summarytext]
        else:
            self.errorcount=self.errorcount+1
            self.logger.error("Non 200 response Error Processing %s and link %s",pageno,URL)
            return 'error'
    def scrapEntitykeywordList(self,id,pageno,keywords):
        for key in keywords:
            for o in self.scrapEntity(id,pageno,key) :
                yield o