from datetime import datetime
import csv
import os
from scrap import Scrap
import re
import requests
from requests.exceptions import Timeout,ReadTimeout
import logging
import argparse
import math
def start_scrapping():
    print('started processing')
    id=1000000
    filename="data/tasks.csv"
    writer = csv.writer(open(filename, "w", encoding="utf-8"))
    writer.writerow(['id','keyword','link','title', 'summarytext'])
    with open('data/articleextractnews0.csv') as csv_file:    
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            id=id+1
            writer.writerow([id,row['keyword'],row['link'],row['title'],row['summarytext']])           


logging.basicConfig(filename='app.log',filemode='w')
start_scrapping()
#keywords = ['"money laundering"']
#print(keywords[0].strip('"'))
#ingnorelist=re.compile(r'Annual')
#if not(ingnorelist.search('https://crdbbank.co.tz/wp-content/uploads/2019/05/Annual%20Report%202018.pdf')):
#    print('u')
#ingnorelist=re.compile(r'text/html')
#print(re.search(r'text/html','text/html; charset=utf-8'))
#resp = requests.get("https://internationalbanker.com/banking/commercial-bank-kuwait-convert-islamic-banking/",timeout=3)
#print(resp.text)