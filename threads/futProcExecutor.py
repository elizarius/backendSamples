import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import  as_completed
import urllib.request

# See training on performance benchmarks examples when use and not pools
# Process pools are extremally useful with several CPUs HW architecture
# ThreadPools are useful when IO tasks or network bound (latency) tasks !!!!!
# See example on cpu bound tasks in training course


url_list = ['http://www.loonycorn.com/',
            'http://reuters.com/',
            'http://wwf.panda.org/',
            'https://en.unesco.org/']

num_list = [1, 2, 3, 4, 5, 6]

def url_loader(url, time):
    with urllib.request.urlopen(url, timeout=time) as conn:
        return conn.read()

def main_processpool():
    start = time.time()

    with ProcessPoolExecutor(max_workers=7) as executor:
        future_to_page = {executor.submit(url_loader, url, 60): url for url in url_list}

        print('Process pool future benchmarks ')
        for future in as_completed(future_to_page):
            url = future_to_page[future]
            result = future.result()
            print('The page %r is %d bytes' % (url, len(result)))
    print('Total time taken:', time.time() - start)


def main_threatpool():
    start = time.time()

    with ThreadPoolExecutor(max_workers=7) as executor:
        future_to_page = {executor.submit(url_loader, url, 60): url for url in url_list}

        print('\n\n')
        print('Thread pool future benchmarks ')
        for future in as_completed(future_to_page):
            url = future_to_page[future]
            result = future.result()
            print('The page %r is %d bytes' % (url, len(result)))
    print('Total time taken:', time.time() - start)


main_processpool()
main_threatpool()

