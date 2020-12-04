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

print('\nGet request with parameters AKA web browsing ***\n')
resp = requests.get('https://www.wikipedia.org/', verify=False)
print('WIKI URL:  {}'.format(resp.url))
webbrowser.open(resp.url)

pars ={'q' : 'alexander tikhonov biathlon'}
resp = requests.get(url='https://www.youtube.com/search',
                    params=pars, 
                    verify=False)
print('search URL:  {}'.format(resp.url))
webbrowser.open(resp.url)


print('\nPOST request ***\n')
resp = requests.post('https://www.wikipedia.org/w/index.php', 
                    data={'search' : 'skillsoft'},
                    verify=False)
pprint(resp.text)

               