import requests
from pprint import pprint
import json
import webbrowser

print(requests.__version__)
print(requests.__copyright__)

resp = requests.get('https://swapi.dev/api/planets/3/', verify=False)
print(resp.status_code)
print('Type:\t {}'.format(type(resp)))
print('\n\n\nStar Headers:\ {}'.format(resp.headers))
data =json.loads(resp.text)
print('\nData:\n')
pprint(data)

print('\n***** GET request  AKA web browsing ***\n')
resp = requests.get('https://www.wikipedia.org/', verify=False)
print('WIKI URL:  {}'.format(resp.url))
webbrowser.open(resp.url)


print('\n***** GET request with parameters ***\n')
pars ={'q' : 'alexander tikhonov biathlon'}
resp = requests.get(url='https://www.youtube.com/search',
                    params=pars, 
                    verify=False)
print('search URL:  {}'.format(resp.url))
webbrowser.open(resp.url)


print('\n***** POST request ***\n')
resp = requests.post('https://www.wikipedia.org/w/index.php', 
                    data={'search' : 'skillsoft'},
                    verify=False)
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

