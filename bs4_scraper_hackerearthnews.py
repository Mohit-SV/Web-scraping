import urllib.request
from bs4 import BeautifulSoup
import json

url = "https://news.ycombinator.com/"

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
request = urllib.request.Request(url, headers={'User-Agent': user_agent})

html = urllib.request.urlopen(request).read()

print(html)

soup = BeautifulSoup(html, 'html.parser')

items = soup.find_all('a', attrs={'class': 'storylink'})

extracted_records = []

for item in items:

    title = item.text
    url = item['href']

    tag = item.parent.parent.findNext('tr').contents[1]

    scored = tag.find('span', attrs={'class': 'score'})
    user = tag.find('a', attrs={'class': 'hnuser'})
    age = tag.find('span', attrs={'class': 'age'})
    commentss = tag.find_all('a')[-1]

    username = user.text
    userlink = user['href']
    score = scored.text
    comments = commentss.text
    commentlink = commentss['href']

    if not url.startswith('http'):
        url = "https://news.ycombinator.com" + url

    if not userlink.startswith('http'):
        userlink = "https://news.ycombinator.com" + userlink

    if not commentlink.startswith('http'):
        commentlink = "https://news.ycombinator.com" + commentlink

    record = {'title': title, 'url': url, 'score': score, 'username': username, 'userlink': userlink, 'comments': comments, 'commentlink': commentlink}
    extracted_records.append(record)

with open('news.json', 'w') as outfile:
    json.dump(extracted_records, outfile, indent=4)
    # mongo.dump(extracted_records, outfile, indent=4)

