from pprint import pprint
from pyquery import PyQuery as pq
import requests
import json

pg = 1
while True:
    url = f"https://techcrunch.com/wp-json/wp/v2/tc_video?page={pg}&per_page=100&_embed=true&_envelope=true&cachePrevention=0"
    raw = requests.get(url).text
    data = json.loads(raw)
    list_posts = []
    try:
        if data["body"]["data"]["status"] == 400:
            print("Out of scope")
            break
    except:
        for j in range(1):
            i=j+2
            post = {}
            post["post_id"] = data["body"][i]["id"]
            post["post_date"] = data["body"][i]["date_gmt"]
            post["post_sec_title"] = data["body"][i]["title"]["rendered"]
            post["post_link"] = data["body"][i]["link"]
            post["post_auth_link1"] = data["body"][i]["_links"]["authors"][0]["href"]
            post["post_auth_name"] = data["body"][i]["_embedded"]["authors"][0]["name"]
            post["post_auth_id"] = data["body"][i]["_embedded"]["authors"][0]["id"]
            post["post_auth_link2"] = data["body"][i]["_embedded"]["authors"][0]["link"]
            list_posts.append(post)
        pg += 1
        break


# pprint(list_posts)


for link in list_posts:
    post_url = link["post_link"]
    content = pq(post_url)
    jason = content("script").attr("type", "text/javascript").eq(17).text()[34:-11]
    ext = json.loads(jason)
    hash = ext["entities"]["posts"][0]["vidible_hash"]
    time = link["post_date"]
    link["video_link"] = f"https://videos.vidible.tv/prod/{hash}/{time[:10]}/{hash}_1920x1080_v4.mp4"
    link["description"] = content("div.article-content")("p").attr("id","speakable-summary").text()

pprint(list_posts)

