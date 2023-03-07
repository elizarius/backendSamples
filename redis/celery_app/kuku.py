from celery_app.app import hello
from celery_app.tasks import another_task, kuku, send_file
from datetime import datetime


files = ['156K.zip', '750K.tgz', '13M.tar.gz', '28M.tar.gz', '36M.tar.gz' ]
for name in files:
    full_path = '/home/ealexel/tmp/'+name 
    with open(full_path, 'rb') as zf:
        now = datetime.now()
        data = zf.read()
        result = send_file.delay(name, data, serializer='pickle')
        result.get()
        later = datetime.now()
        difference = (later - now).total_seconds()
        print("File: {}  sent in {} secs".format(name, difference))

#result = kuku.delay("AELS **")
#result.get() # will output 'Hello KUKU'
