import requests
from pprint import pprint
import json
import webbrowser

from PIL import Image
from io import BytesIO

# AELZ write CLI processor to demo http options by input from command line

print(requests.__version__)
print(requests.__copyright__)

resp = requests.get('https://swapi.dev/api/planets/3/')
print(resp.status_code)
print('Type:\t {}'.format(type(resp)))
print('\n\n\nStar Headers:\ {}'.format(resp.headers))
data =json.loads(resp.text)
print('\nData:\n')
pprint(data)

print('\n***** GET request  AKA web browsing ***\n')
resp = requests.get('https://www.wikipedia.org/')
print('WIKI URL:  {}'.format(resp.url))
# Uncomment for full demo with web browsers
#webbrowser.open(resp.url)


print('\n***** GET request with parameters ***\n')
pars ={'q' : 'alexander tikhonov biathlon'}
resp = requests.get(url='https://www.youtube.com/search',
                    params=pars)
print('search URL:  {}'.format(resp.url))
#webbrowser.open(resp.url)

print('\nPOST request ***\n')
resp = requests.post('https://www.wikipedia.org/w/index.php',
                    data={'search' : 'skillsoft'})
#pprint(resp.text)


print('\n***** HEAD request ***\n')
resp = requests.head('http://example.com')
pprint(resp.status_code)
pprint(resp.content)
pprint(resp.headers)

print('\n***** HEAD request 2 ***\n')
resp = requests.head('http://alexander-tikhonov.ru')
pprint(resp.status_code)
pprint(resp.content)
pprint(resp.headers)
pprint(resp.headers['Set-Cookie'])

print('\n***** OPTIONS request, see access control methods ***\n')
resp = requests.options('https://httpbin.org/get')
#resp = requests.head('http://alexander-tikhonov.ru')
pprint(type(resp))
pprint(resp.headers)

print('\n***** DELETE request EXAMPLE  ***\n')
resp = requests.options('https://httpbin.org/delete')
pprint(resp.text)

print('\n*****Setting specific fields in HEADER  ***\n')
headers = {'user-agent' : 'Googlechrome'}  # simulate request from different browser. 
resp = requests.get('https://swapi.dev/api/people/3/', headers=headers)
pprint(resp.headers)
pprint(resp.headers['content-type'])
pprint(resp.request.headers)
pprint(resp.request.headers['user-agent'])


print('\n*****Encoding of received objects  ***\n')
resp = requests.get('https://github.com/timeline.json')
pprint(resp.text)
pprint(resp.encoding)
print('\n**** Change encoding type and see same same response ***\n')
resp.encoding = 'ISO-8859-1'
pprint(resp.encoding)
pprint(resp.text)

print('\n*** Processing of binary data  ***\n')
resp = requests.get('https://upload.wikimedia.org/wikipedia/commons/4/4c/Moon_and_Aurora.jpg')
pprint(resp.status_code)
pprint(type(resp.content))

image = Image.open(BytesIO(resp.content))
pprint(type(image))
image.save('aurora.png')
Image.open('aurora.png')



print('\n*** Handling of responses in different formats ***\n')
resp = requests.get('https://swapi.dev/api/vehicles/4/')
pprint(resp.status_code)
print('\n*response by json()*\n')
pprint(type(resp.json()))   # actually the same as json.loads()
pprint(resp.json())
print('\n*response by json.loads()*\n')
pprint(type(json.loads(resp.text)))
pprint(json.loads(resp.text))
print('\n*response by resp.txt*\n')
pprint(type(resp.text))
pprint(resp.text)

print('\n*** Handling of Non JSON responses ***\n')
resp = requests.get('https://yahoo.com')
pprint(resp.status_code)
if (resp.headers['content-type'] != 'application/json'):
    print('Not JSON response data received {}'.format(
        resp.headers['content-type']))

print('\n*** Handling of streaming request (to speed up for large obejcts ) ***\n')
resp = requests.get('https://swapi.dev/api/vehicles/4/',
                    stream=True)
pprint(resp.status_code)
print(resp.raw)
print(resp.raw.read(10))
# it could be dumped to file and later processed, f.i.
# for chunk in resp.iter_content(1000):
#    x.write(chunk)


print('\n*** Handling of status codes ***\n')
resp = requests.get('http://example.com')
pprint(resp.status_code)
pprint(resp.ok)
resp = requests.get('https://yahoo.com/12345678910')
pprint(resp.status_code)
pprint(resp.ok)
# use raise_for_status to raise exception


print('\n*** Handling of redirects ***\n')
resp = requests.get('http://gmail.com')
pprint(resp.status_code)
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

