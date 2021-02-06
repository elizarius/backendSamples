#!/usr/bin/python3

import argparse
import os

import requests
from pprint import pprint
import json
import webbrowser

from PIL import Image
from io import BytesIO
from http import HTTPStatus as httpstatus

print(f'Requests: {requests.__version__}')
print(requests.__copyright__)

def get_request():
    print('\n***** GET request demo ***\n')
    resp = requests.get('https://swapi.dev/api/planets/3/')
    print(httpstatus(resp.status_code))

    print('Type:\t {}'.format(type(resp)))
    print('\nHeaders:\n {}'.format(resp.headers))
    print('\nData:')
    pprint(json.loads(resp.text))

    print('\n***** GET request  AKA web browsing ***')
    resp = requests.get('https://www.wikipedia.org/')
    print('WIKI URL:  {}'.format(resp.url))
    webbrowser.open(resp.url)

    print('\n***** GET request with parameters ***')
    pars ={'q' : 'alexander tikhonov biathlon'}
    resp = requests.get(url='https://www.youtube.com/search', params=pars)
    print('search URL:  {}'.format(resp.url))
    webbrowser.open(resp.url)

def post_request():
    print('\nPOST request used as search demo ***\n')
    resp = requests.post('https://www.wikipedia.org/w/index.php', data={'search' : 'skillsoft'})
    print(httpstatus(resp.status_code))
    #pprint(resp.text)

def head_request():
    print('\n***** HEAD request ***')
    resp = requests.head('http://example.com')
    print(httpstatus(resp.status_code))
    pprint(resp.content)
    pprint(resp.headers)
    
    print('\n***** HEAD request 2 ***')
    resp = requests.head('http://alexander-tikhonov.ru')
    print(httpstatus(resp.status_code))
    # pprint(resp.content)
    # pprint(resp.headers)
    pprint(resp.headers['Set-Cookie'])

def options_request():
    print('\n***** OPTIONS request, ACCESS CONTROL methods!!! ***')
    resp = requests.options('https://httpbin.org/get')
    pprint(type(resp))
    pprint(resp.headers)

def delete_request():
    print('\n***** DELETE request EXAMPLE  ***')
    resp = requests.options('https://httpbin.org/delete')
    print(httpstatus(resp.status_code))
    pprint(resp.text)

def mask_request_header():
    print('\n*****Setting specific fields in HEADER, f.i. simulate another browser  ***')
    headers = {'user-agent' : 'Googlechrome'}  # simulate request from different browser. 
    resp = requests.get('https://swapi.dev/api/people/3/', headers=headers)
    pprint(resp.headers)
    pprint(resp.headers['content-type'])
    pprint(resp.request.headers)
    pprint(resp.request.headers['user-agent'])

def encode_response():
    print('\n*****Encoding of received objects  ***')
    resp = requests.get('https://github.com/timeline.json')
    pprint(resp.encoding)
    pprint(resp.text)
    print('\n**** Change encoding type and see same same response ***')
    resp.encoding = 'ISO-8859-1'
    pprint(resp.encoding)
    pprint(resp.text)

def process_binary():
    print('\n*** Processing of binary data  ***\n')
    resp = requests.get('https://upload.wikimedia.org/wikipedia/commons/4/4c/Moon_and_Aurora.jpg')
    pprint(type(resp.content))
    image = Image.open(BytesIO(resp.content))
    pprint(type(image))
    image.save('aurora.png')
    Image.open('aurora.png')

def process_resp_formats():
    print('\n*** Handling of responses in different formats ***')
    resp = requests.get('https://swapi.dev/api/vehicles/4/')
    print('\n****response by json()****')
    pprint(type(resp.json()))   # actually the same as json.loads()
    pprint(resp.json())
    print('\n****response by json.loads()****')
    pprint(type(json.loads(resp.text)))
    pprint(json.loads(resp.text))
    print('\n****response by resp.txt****')
    pprint(type(resp.text))
    pprint(resp.text)

    print('\n*** Handling of Non JSON responses ***')
    resp = requests.get('https://yahoo.com')
    if (resp.headers['content-type'] != 'application/json'):
        print('Not JSON response data received {}'.format(
            resp.headers['content-type']))

def streaming():
    print('\n*** Handling of streaming request (to speed up for large obejcts ) ***')
    resp = requests.get('https://swapi.dev/api/vehicles/4/', stream=True)
    print(resp.raw)
    print(resp.raw.read(10))
    # it could be dumped to file and later processed, f.i.
    # for chunk in resp.iter_content(1000):
    #    x.write(chunk)


def redirects():
    print('\n*** Handling of redirects ***')
    resp = requests.get('http://gmail.com')
    print(httpstatus(resp.status_code))
    pprint(resp.history)
    for red in resp.history:
        print(' Redirection:  {} : {}'.format(red.status_code, red.url))
        pprint(red.is_redirect)
        pprint(red.is_permanent_redirect)
    print(' Final Redirected URL:  {}'.format(resp.url))
    pprint(resp.is_redirect)
    # Note: 
    #   - allow_redirect=true, false to get correct status code.
    #   - timeout = xx in req , to limit time and this raises ConnectionError exception


def parse_arguments():
    parser = argparse.ArgumentParser(
                      description='HTTP requests demo ',
                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-g', '--get', action='store_true', required=False,
                        help='GET method demo')
    parser.add_argument('-p', '--post', action='store_true', required=False,
                        help='POST method demo')
    parser.add_argument('-he', '--head', action='store_true', required=False,
                        help='HEAD method demo')
    parser.add_argument('-o', '--options', action='store_true', required=False,
                        help='OPTIONS method demo')
    parser.add_argument('-d', '--delete', action='store_true', required=False,
                        help='DELETE method demo')
    parser.add_argument('-mh', '--mask', action='store_true', required=False,
                        help='MODIFY HEADER demo')
    parser.add_argument('-e', '--encode', action='store_true', required=False,
                        help='Encode response in different encoding schema')
    parser.add_argument('-b', '--binary', action='store_true', required=False,
                        help='Process received binary data')
    parser.add_argument('-f', '--formats', action='store_true', required=False,
                        help='Process response in different formats')
    parser.add_argument('-s', '--stream', action='store_true', required=False,
                        help='Streaming example')
    parser.add_argument('-r', '--redirect', action='store_true', required=False,
                        help='Redirects processing example')


    args = parser.parse_args()
    return parser, args

def main():
    parser,args = parse_arguments()
    #print (args)
    #print (args._get_kwargs())

    for arg in args._get_kwargs():
        if True in arg:
            break
    else:
        parser.print_help()

    if args.get:        get_request()
    if args.post:       post_request()
    if args.head:       head_request()
    if args.options:    options_request()
    if args.delete:     delete_request()
    if args.mask:       mask_request_header()
    if args.encode:     encode_response()
    if args.binary:     process_binary()
    if args.formats:    process_resp_formats()
    if args.stream:     streaming()
    if args.redirect:   redirects()



if __name__ == "__main__":
    main()
