import requests
from datetime import datetime
import time

def log (url, content, latency):
    print ('URL: {}\tContent: {}\tLatency(s): {}'.format(url, content, latency))

def get_latency(start_time):
    end_time = datetime.now()
    return (end_time - start_time).seconds

def parse_config_file(path):
    print("Reading %s... {}.".format(path))
    content_string = None
    urls = []
    timeout = 5
    with open(path, 'r') as f:
        metadata = f.read()
        splitted =metadata.splitlines()
        for x in splitted:
            if "Content" in x:
                cont = x.split(':')
                content_string = cont[1]
            elif "Timeout" in x:
                tm = x.split(':')
                timeout = int(tm[1])
            else:
                urls.append(x)
    return urls,content_string,timeout

def main():

    content_state = 'NOT found'
    start_stamp = 0
    latency = 0

    urls,content,timeout = parse_config_file('config.txt')

    while True:
        print ('Sleeping for {} seconds ...'.format(timeout))
        time.sleep(timeout)
        for url in urls:
            try:
                start_stamp = datetime.now()
                resp = requests.get(url)
                resp.raise_for_status()
                if content in resp.text:
                    content_state = 'found'
                else:
                    content_state = 'NOT found'
                latency =  get_latency(start_stamp)
                log (url, content_state, latency)
            except requests.HTTPError as e:
                content_state  = 'HTTP Connection error'
                latency =  get_latency(start_stamp)
                log (url, content_state, latency)
            except Exception as e:
                print ('Generic exception appeared {}'.format(e))

if __name__ == '__main__':
    main()
