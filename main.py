# ★☆☆☆☆
# 宇宙中最浪漫的事情，就是为喜欢的动画送上一颗星星

import requests as r
import json
from tqdm import tqdm
from fake_useragent import UserAgent

proxies = {
    "http": "http://127.0.0.1:7980",
    "https": "http://127.0.0.1:7980"
}


def percentage_difference(a, b):
    diff = a - b
    percentage = (diff / b) * 100
    return percentage


def closest_number(n):
    closest = 2
    for i in [4, 6, 8, 10]:
        if abs(i - n) < abs(closest - n):
            closest = i
    return closest


def score(x: int) -> str:
    match x:
        case 2:
            return "★☆☆☆☆"
        case 4:
            return "★★☆☆☆"
        case 6:
            return "★★★☆☆"
        case 8:
            return "★★★★☆"
        case 10:
            return "★★★★★"
    return "☆☆☆☆☆"


media_basic_info_api = "https://api.bilibili.com/pgc/review/user"  # 参数:media_id
short_comments_api = "https://api.bilibili.com/pgc/review/short/list"
long_comments_api = "https://api.bilibili.com/pgc/review/long/list"
media_id = input("请输入要查询的剧集的mdid(media_id):")
data = json.loads(r.get(media_basic_info_api, params={'media_id': media_id}).text)
title = data['result']['media']['title']
display_score = data['result']['media']['rating']['score']
type_name = data['result']['media']['type_name']
print(f"[{type_name}]{title}的B站评分为{display_score}")

short_comments_total = (int(
    json.loads(r.get(short_comments_api, params={'media_id': media_id, 'ps': '30', 'sort': '0'}).text)['data'][
        'total']) // 30) * 30
long_comments_total = (int(
    json.loads(r.get(long_comments_api, params={'media_id': media_id, 'ps': '30', 'sort': '0'}).text)['data'][
        'total']) // 30) * 30

short_comments_score = 0
scores = [0, 0, 0, 0, 0, 0]
print("宇宙中最浪漫的事情，就是为喜欢的动画送上一颗星星😅👍★☆☆☆☆")

with tqdm(total=short_comments_total, desc="统计短评中", leave=True, unit="comments") as pbar:
    headers = {'User-Agent': str(UserAgent().random)}
    req = r.get(short_comments_api, params={'media_id': media_id, 'ps': '30', 'sort': '0'}, proxies=proxies,
                headers=headers)
    for i in range(0, short_comments_total, 30):
        d = json.loads(req.text)['data']
        next_comments = d['next']
        lists = d['list']
        for v in lists:
            short_comments_score += v['score']
            scores[int(v['score'] / 2)] += 1
            pbar.set_postfix_str("当前评论分数:" + score(closest_number(v['score'])))
        pbar.update(30)
        req = r.get(short_comments_api,
                    params={'media_id': media_id, 'ps': '30', 'sort': '0', 'cursor': next_comments})
    pbar.set_postfix_str("检索完毕")

long_comments_score = 0

with tqdm(total=long_comments_total, desc="统计长评中", leave=True, unit="comments") as pbar:
    req = r.get(long_comments_api, params={'media_id': media_id, 'ps': '30', 'sort': '0'}, proxies=proxies,
                headers=headers)
    for i in range(0, long_comments_total, 30):
        d = json.loads(req.text)['data']
        next_comments = d['next']
        lists = d['list']
        for v in lists:
            long_comments_score += v['score']
            scores[int(v['score'] / 2)] += 1
            pbar.set_postfix_str("当前评论分数:" + score(closest_number(v['score'])))
        pbar.update(30)
        req = r.get(long_comments_api,
                    params={'media_id': media_id, 'ps': '30', 'sort': '0', 'cursor': next_comments})
    pbar.set_postfix_str("检索完毕")

real_score = (short_comments_score + long_comments_score) / (short_comments_total + long_comments_total)
short_comments_score /= short_comments_total
long_comments_score /= long_comments_total
percentage = percentage_difference(display_score, real_score)
compress_or_expand = ["缩水", "膨胀"]
print(
    f"{title}的真实评分为:{real_score:.2f}，显示的评分{display_score}相比真实评分{compress_or_expand[percentage >= 0]}了{abs(percentage):.3f}%，其中短评评分{short_comments_score:.3f}，长评评分{long_comments_score:.3f}")
print(f"得分分布：{scores[1:]}")
