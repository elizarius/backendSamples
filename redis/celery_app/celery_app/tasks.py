from celery_app.app import celery_app
from datetime import datetime

@celery_app.task
def another_task(name: str) -> str:
    return f"Hello {name}"

@celery_app.task
def hello(name: str) -> str:
    return f"Hello {name}"

@celery_app.task
def kuku(name) :
    print( f"Hello {name}")


@celery_app.task(serializer='pickle')
def send_file(name, data, serializer='pickle'):
    print("Received file:  {}  size Kb:  {}".format(name, int(len(data)/1024)))
    now = datetime.now()
    out_path = '/home/ealexel/tmp/1/' + name
    outFile = open(out_path, "wb")
    outFile.write(data)
    later = datetime.now()
    difference = (later - now).total_seconds()
    print("Received file in {} secs".format(difference))
 
    
