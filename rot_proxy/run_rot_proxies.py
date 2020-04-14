import sys
sys.path.insert(0, "***path_to_dir***") #edit

from rot_proxies import get_proxies
from itertools import cycle
from bs4 import BeautifulSoup
import urllib.request


proxies = get_proxies()
proxy_pool = cycle(proxies)

url = 'https://httpbin.org/ip'

for i in range(1, 11):
    proxy = next(proxy_pool)
    print("Request #%d"%i)

    request = urllib.request.Request(url)
    rr = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(rr, "html.parser")

    try:
        # response = soup.get(url,proxies={"http": proxy, "https": proxy})
        print(response.json())
    except:
        print("Skipping. Connection error")
