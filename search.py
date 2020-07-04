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
    keywords = ['"money laundering"','"market abuse" OR "market manipulation"','"insider trading"','"regulatory breach"','tax evasion','bribery OR smuggling or fraud or illegal or extortion'] # dynamic input, how ?
    #keywords = ['"regulatory breach"'] # dynamic input, how ?
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--foperand", required=False,help="file rollover")
    ap.add_argument("-t", "--soperand", required=False,help="entity to be processed")
    ap.add_argument("-c", "--checkpoint", required=False,help="checkpoint to continue from")

    args = vars(ap.parse_args())
    
    if (args['foperand']):
        print('filerollover:' + args['foperand'])
        filerollover=int(args['foperand'])
    else:
        filerollover=100

    if (args['soperand']):
        print('entitytobeprocessed:' + args['soperand'])
        entitytobeprocessed=int(args['soperand'])
    else:
        entitytobeprocessed=10

    if (args['checkpoint']):
        print('entitytobeprocessed:' + args['checkpoint'])
        resumecheckpoint=int(args['checkpoint'])
    else:
        resumecheckpoint=0

    if (resumecheckpoint>0):
        filecounter=math.ceil(resumecheckpoint/filerollover)-1
        filename = 'data/articleextract{0}.csv'.format(filecounter)       
        writer = csv.writer(open(filename, "a", encoding="utf-8"))

    id=0
    checkpoint=0
    filename=''
    #writer = csv.writer(open(filename, "w", encoding="utf-8"))
    checkpointwriter=open("checkpoint.txt", "w")

    scrap = Scrap()
    entitycount=0
    with open('data/input.csv') as csv_file:    
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            id=row['id']
            entity=row['entity']
            print('-------Started Processing: ' + entity)
            print('-------Total Records Processed: ' + str(entitycount))
            try:
                if (entitycount<resumecheckpoint):
                    entitycount=entitycount+1
                    continue
                if (entitycount==entitytobeprocessed):
                    break
                scrapedentity=scrap.scrapEntitykeywordList(id,entity,keywords)

                if (entitycount%filerollover==0):
                    filename = 'data/articleextract{0}.csv'.format(int(entitycount/filerollover))
                    print(filename)
                    writer = csv.writer(open(filename, "a", encoding="utf-8"))
                    writer.writerow(['id','entity','keyword','link','title', 'summarytext'])                    
                if (scrapedentity!='error'):
                    writer.writerows(scrapedentity)
            except (requests.ConnectionError,requests.ConnectTimeout,requests.ReadTimeout):
                print("error occured while processing: " + str(id))
            print('-------End Processing: ' + entity)            
            entitycount=entitycount+1
            checkpoint=entitycount
            checkpointwriter.write(str(checkpoint))
    checkpointwriter.close()
    print('-------Total Entities Processed: ' + str(entitycount) + 
    ' Total Errors:' + str(scrap.errorcount))
    logging.error('-------Total Entities Processed: ' + str(entitycount) + 
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