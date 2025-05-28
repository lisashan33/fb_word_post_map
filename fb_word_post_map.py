from dotenv import dotenv_values

import requests
import json
import jieba

import csv

config = dotenv_values("project_fb.env")  
access_token = config["access_token"] # 需更新access_token
url = f"https://graph.facebook.com/v21.0/me/posts?access_token={access_token}"

res = requests.get(url)
jd = json.loads(res.text)

# print(jd)



url = "https://www.facebook.com/xie.jia.shan.200591/posts/"

post_message = []

while "paging" in jd:
    for post in jd["data"]:
        if "message" in post:
            post_id = post["id"]
            post_time = post["created_time"]
            post_url = f"{url}{post_id}"
            words = jieba.cut(post["message"])

            for word in words:
                if len(word) >= 2:  # 過濾掉太短的詞
                    post_message.append([word,post_time,post_url])

    # 繼續下一頁
    if "next" in jd["paging"]:
        res = requests.get(jd["paging"]["next"])
        jd = json.loads(res.text)
    else:
        break

# 寫入 CSV
with open("./output/fb_word_post_map.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["post_word", "post_time", "post_url"])
    writer.writerows(post_message)

print("fb_word_post_map.csv 已輸出成功")