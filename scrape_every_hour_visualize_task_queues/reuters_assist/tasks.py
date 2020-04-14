from .config import celery, client, user_agent
import datetime
from bs4 import BeautifulSoup
import urllib.request
from .helpers.test_flatten import all_keys_count


@celery.task(bind=True)
def scra_per(self):
    db = client.reuters_news
    col = db.news_items

    reg_url = "https://in.reuters.com/"
    request1 = urllib.request.Request(reg_url, headers={'User-Agent': user_agent})
    r = urllib.request.urlopen(request1).read()
    soup1 = BeautifulSoup(r, "html.parser")
    lang_bar = soup1.find("ul", {"class": "edition-list"})
    aa = lang_bar.find_all("a")
    lang_sites = {}
    for item in aa:
        try:
            lang_sites[item.text] = "https:" + item['href']
        except:
            continue
    # print(lang_sites)
    news_items = []

    i = 0
    tot = len(lang_sites)
    for lang in lang_sites:
        i += 1
        if lang in ['India', 'United States', 'United Kingdom', 'Deutschland', 'América Latina']:
            lang_url = lang_sites.get(lang)
            request2 = urllib.request.Request(lang_url, headers={'User-Agent': user_agent})
            rr = urllib.request.urlopen(request2).read()
            soup2 = BeautifulSoup(rr, "html.parser")
            nav_bar = soup2.find("ul", {"class": "horizontal-list nav-list"})
            # print(nav_bar)
            a = nav_bar.find_all("a", {"class": "nav-link-sec"})
            categories = {}
            for item in a:
                try:
                    if "\n" not in item.text:
                        categories[item.text] = "https://in.reuters.com/news/archive" + item['href'] \
                                                + "?view=page&page=1&pageSize=10"
                except:
                    continue
            # print(categories)

            for category in categories:
                for page in range(0, 3):
                    page = page + 1
                    page_url = f"{categories.get(category)[:-13]}{page}&pageSize=10"
                    # print(page_url)
                    request3 = urllib.request.Request(page_url, headers={'User-Agent': user_agent})
                    rrr = urllib.request.urlopen(request3).read()
                    soup3 = BeautifulSoup(rrr, "html.parser")
                    all_posts = soup3.find_all('article', class_="story")
                    # print(all_posts,"\n\n\n\n")
                    for item in all_posts:
                        d = {}
                        story_content = item.find("div", {"class": "story-content"})
                        post = story_content.find("a")
                        content = list(filter(None, story_content.text.split("\n")))
                        post_link = post.get('href')
                        # print(content[1], "\n\n")
                        d['post_link'] = f"https://in.reuters.com/{post_link}"
                        if len(content) == 3:
                            d['region'] = lang
                            d['category'] = category
                            d["post_title"] = content[0].strip()
                            d["post_content"] = content[1]
                            d["date_created"] = content[2]
                        if len(d) == 6:
                            news_items.append(d)
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': tot,
                                'status': f"{lang}"})

    index = 0
    today = datetime.datetime.now()
    for item in news_items:
        index += 1
        item['updated_at'] = today
        item['post_id'] = index
        update_news = col.insert(item)
        message = f"{update_news}"
        print(message)

    return {'current': tot, 'total': tot, 'status': 'Task1 completed!',
            'result': "Yo... Today's news has been inserted into your DB"}


# @celery.task(bind=True)
# def build_hourly_collection(self):
#     print("build_hourly_collection started")
#     hourly_collection = {}
#     db = client.reuters_news
#     col = db.news_items
#     today = datetime.datetime.now() - datetime.timedelta(days=6)
#     for h in range(48):
#         starttime = today - datetime.timedelta(hours=h)
#         endtime = today - datetime.timedelta(hours=h + 1)
#         hourly_collection[starttime.strftime("%d/%m/%Y, %H to %H+1")] = col.find(
#             {'$or': [{'add_doc_date': {'$gt': endtime, '$lt': starttime}},
#                      {'updated_at': {'$gt': endtime, '$lt': starttime}}]})
#         message = f"Ran schema check of DB added in one hour before {h} hours"
#         print(message)
#         self.update_state(state='PROGRESS',
#                           meta={'current': h, 'total': 48,
#                                 'status': message})
#         print({'current': h, 'total': 48, 'status': message})
#     return {'current': 48, 'total': 48, 'status': 'Task2 completed!',
#             'result': hourly_collection}


@celery.task(bind=True)
def build_hourly_key_details(self):
    print("build_hourly_collection started")
    hourly_collection = {}
    db = client.reuters_news
    col = db.news_items
    today = datetime.datetime.now()
    many_days = 28
    for h in range(many_days):
        starttime = today - datetime.timedelta(days=h)
        endtime = today - datetime.timedelta(days=h + 1)
        hourly_collection[starttime.strftime("%d/%m/%Y, %H to %H+1")] = col.find(
            {'$or': [{'add_doc_date': {'$gt': endtime, '$lt': starttime}},
                     {'updated_at': {'$gt': endtime, '$lt': starttime}}]})
        message = f"Running schema check of DB added in one hour before {h} hours"
        print(message)
        self.update_state(state='PROGRESS',
                          meta={'current': h, 'total': many_days,
                                'status': message})
        print({'current': h, 'total': many_days})
    print(hourly_collection)
    print("build_hourly_key_details started")
    # for i,x in hourly_collection.items():
    #     for y in x:
    #         print(y)
    hourly_key_details = {}
    for item in hourly_collection:
        # print(item)
        # print(all_keys_count(hourly_collection.get(item)))
        hourly_key_details[item] = all_keys_count(hourly_collection.get(item))
    col1 = db.news_items_key_freq
    col1.drop()
    insert_keys = col1.insert(hourly_key_details)
    return {'current': many_days, 'total': many_days, 'status': 'Task2 completed!',
            'result': "check the table now"}

#
# @celery.task()
# def infer_schema():
#     ch = chord(build_hourly_collection.s() | build_hourly_key_details.s())
#     pprint.pprint(ch)
#     return ch
