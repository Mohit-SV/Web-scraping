from bs4 import BeautifulSoup
import urllib.request

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'


def get_proxies():
    url = 'https://free-proxy-list.net/'

    request = urllib.request.Request(url, headers={'User-Agent': user_agent})
    r = urllib.request.urlopen(request).read()

    soup = BeautifulSoup(r, "html.parser")
    soup_table = soup.find('table', attrs={'id': "proxylisttable"})
    # print(soup_table.text)
    tr_list = soup_table.find_all("tr")
    proxies = []

    for n, tr in enumerate(tr_list[1:20]):
        td_list = tr.find_all('td')
        # for td in td_list:
        #     print(td.text)
        # print(td_list[0].text)
        if td_list[6].text == 'yes':
            proxies.append(td_list[0].text + ':' + td_list[1].text)
        if len(proxies) == 10:
            break

    return proxies


print(get_proxies())
# print(len(get_proxies()))

