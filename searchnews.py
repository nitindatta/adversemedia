from datetime import datetime
import csv
import os
from scrapnews import ScrapNews
import re
import requests
from requests.exceptions import Timeout,ReadTimeout
import logging
import argparse
import math
def start_scrapping():
    print('started processing')
    #keywords = ['"money laundering"','"market abuse" OR "market manipulation"','"insider trading"','"regulatory breach"','tax evasion','bribery OR smuggling or fraud or illegal or extortion'] # dynamic input, how ?
    #keywords = ['money laundering','market abuse OR market manipulation','insider trading','regulatory breach','"tax evasion"'] # dynamic input, how ?
    keywords = ['"money laundering"','"market abuse"','"market manipulation"','"insider trading"','"regulatory breach"','tax evasion','bribery', 'smuggling', 'fraud', 'extortion','"organized crime"','trafficking','illegal','penalty','embezzle','terrorist','corruption','criminal'] # dynamic input, how ?

    #keywords = ['money laundering'] # dynamic input, how ?
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--foperand", required=False,help="file rollover")
    ap.add_argument("-p", "--soperand", required=False,help="pages to be processed")
    ap.add_argument("-c", "--checkpoint", required=False,help="checkpoint to continue from")
    ap.add_argument("-m", "--filemode", required=False,help="file mode for writing")

    args = vars(ap.parse_args())
    
    if (args['foperand']):
        print('filerollover:' + args['foperand'])
        filerollover=int(args['foperand'])
    else:
        filerollover=10

    if (args['soperand']):
        print('pagestobeprocessed:' + args['soperand'])
        pagestobeprocessed=int(args['soperand'])
    else:
        pagestobeprocessed=1
    
    if (args['checkpoint']):
        print('entitytobeprocessed:' + args['checkpoint'])
        resumecheckpoint=int(args['checkpoint'])
    else:
        resumecheckpoint=0

    if (args['filemode']):
        print('filemode:' + args['filemode'])
        filemode=args['filemode']
    else:
        filemode='w'

    #print(str(resumecheckpoint/entitytobeprocessed))
    
    if (resumecheckpoint>0):
        
        filecounter=math.ceil(resumecheckpoint/pagestobeprocessed)-1
        #filename = 'data/articleextractnews{0}.csv'.format(filecounter)       
        #writer = csv.writer(open(filename, "a", encoding="utf-8"))
        pagestobeprocessed = pagestobeprocessed+resumecheckpoint
    
    id=0
    checkpoint=0
    filename=''
    #writer = csv.writer(open(filename, "w", encoding="utf-8"))
    checkpointwriter=open("checkpoint.txt", "w")
    scrap = ScrapNews()

    #with open('data/input.csv') as csv_file:    
        #reader = csv.DictReader(csv_file, delimiter=',')
    for pageno in range(resumecheckpoint*10, pagestobeprocessed*10,10):
        id=id+1
        #entity=row['entity']
     
        print('-------Total pages Processed: ' + str(pageno))
        try:
            #if (pageno==pagestobeprocessed):
            #    break
            scrapedentity=scrap.scrapEntitykeywordList(id,pageno,keywords)

            if ((pageno/10)%filerollover==0):
                filename = 'data/articleextractnews{0}.csv'.format(int(int(pageno/filerollover)/10))
                print(filename)
                writer = csv.writer(open(filename, filemode, encoding="utf-8"))
                writer.writerow(['id','keyword','link','title', 'summarytext'])                    
            if (scrapedentity!='error'):
                print(scrapedentity)
                writer.writerows(scrapedentity)

        except (requests.ConnectionError,requests.ConnectTimeout,requests.ReadTimeout):
            print("error occured while processing: " + str(id))
        print('-------End Processing: ' + str(pageno))            
        #entitycount=entitycount+1
        checkpoint=pageno
        checkpointwriter.write(str(checkpoint))
    checkpointwriter.close()
    print('-------Total pages Processed: ' + str(id) + 
    ' Total Errors:' + str(scrap.errorcount))
    logging.error('-------Total pages Processed: ' + str(id) + 
    ' Total Errors:' + str(scrap.errorcount))

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