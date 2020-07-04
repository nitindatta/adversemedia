import requests
from readability import Document
import re
import logging

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"

class ExtractArticle:
    def extractArticle(self,link):
        #self.response = requests.get(link)
        resp = requests.get(link,timeout=3,headers = {"user-agent": USER_AGENT})
        if (resp.status_code==200):
            contenttype=resp.headers['Content-Type']            
            if (re.search(r'text/html',contenttype)):  
                doc = Document(resp.text)
                try:
                    article = Article(doc.summary(),doc.title())
                except Exception as e:
                    print('error article')
                    logging.exception("Error while processing article for link %s",link)
                    return None           
                return article
            else:    
                logging.error("Response Content Type expected text/html received %s for link %s",contenttype,link)
                return None
        else:
            logging.error("Response Non 200 for link %s and status code %s",link,resp.status_code)
            return None

class Article:

    def __init__(self,summary,title):
        self.summary = summary
        self.title = title        

    def summary(self):
        return self.summary

    def title(self):
        return self.title