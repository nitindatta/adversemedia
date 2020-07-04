from datetime import datetime
#from airflow import DAG
#from airflow.operators.dummy_operator import DummyOperator
#from airflow.operators.python_operator import PythonOperator
import csv
import os
from scrap import Scrap

def start_scrapping():
    print('started processing')
    keywords = ["money laundering",'"market abuse" OR "market manipulation"',"insider trading","regulatory breach","tax evasion",'bribery OR smuggling","extortion","orgainzed crime"] # dynamic input, how ?
    #keywords = ["money laundering"] # dynamic input, how ?
    #print(" OR ".join(keywords))
    #return
    #AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
    #print(AIRFLOW_HOME)
    #print(os.path.abspath("~/airflow/dags/articleextract.csv"))
    writer = csv.writer(open('/data/articleextract.csv', "w", encoding="utf-8"))
    writer.writerow(['entity','keyword','link','title', 'summarytext'])
    scrap = Scrap()
    entitycount=0
    with open('input.csv') as csv_file:    
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            entity=row[0]
            print('-------Started Processing: ' + entity)
            writer.writerows(scrap.scrapEntitykeywordList(entity,keywords))
            print('-------End Processing: ' + entity)
            entitycount=entitycount+1
    #print('-------Total Entities Processed: ' + entitycount)
start_scrapping()
#dag = DAG('article_scrap', description='Simple tutorial DAG',
#          schedule_interval='0 12 * * *',
#          start_date=datetime(2020, 5, 18), catchup=False)

#dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

#hello_operator = PythonOperator(task_id='article_scrap', python_callable=start_scrapping, dag=dag)

#hello_operator