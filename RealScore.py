import json
import requests
from tqdm import tqdm
from fake_useragent import UserAgent
import numpy


class RealScore:
    _ANIME_BASIC_INFO_API = "https://api.bilibili.com/pgc/review/user"
    _SHORT_COMMENTS_API = "https://api.bilibili.com/pgc/review/short/list"
    _LONG_COMMENTS_API = "https://api.bilibili.com/pgc/review/long/list"

    def __init__(self, media_id: str):
        self._media_id = media_id
        self.anime_title, self.display_score, self.type_name = self._get_anime_info_by_mdid()
        self._short_comments_quantity, self._long_comments_quantity = self._get_concrete_quantity_of_comments()
        self._next_comments_cursor = None

    def _get_anime_info_by_mdid(self) -> (str, float, str):
        data = json.loads(requests.get(self._ANIME_BASIC_INFO_API, params={'media_id': self._media_id}).text)
        anime_title = data['result']['media']['title']
        display_score = data['result']['media']['rating']['score']
        type_name = data['result']['media']['type_name']
        return anime_title, display_score, type_name

    def _get_quantity_of_comments(self, api_url: str) -> int:
        return int(json.loads(
            requests.get(api_url, params={'media_id': self._media_id, 'ps': '30', 'sort': '0'}).text)[
                       'data']['total']) // 30 * 30

    def _get_concrete_quantity_of_comments(self) -> (int, int):
        return self._get_quantity_of_comments(self._SHORT_COMMENTS_API), self._get_quantity_of_comments(
            self._LONG_COMMENTS_API)

    def _get_comments_score(self, api_url: str, total: int) -> (int, list[int]):
        headers = {'User-Agent': str(UserAgent().random)}
        req = requests.get(api_url, params={'media_id': self._media_id, 'ps': total, 'sort': '0',
                                            'cursor': self._next_comments_cursor}, headers=headers)
        api_return_data = json.loads(req.text)['data']
        self._next_comments_cursor = api_return_data['next']
        rating_list = api_return_data['list']
        comments_score_total = 0
        concrete_score_distribution = [0, 0, 0, 0, 0]
        for v in rating_list:
            comments_score_total += v['score']
            concrete_score_distribution[int(v['score'] / 2) - 1] += 1
        return comments_score_total, concrete_score_distribution

    def calculate_scores(self) -> (float, float, float, list[int]):
        short_comments_score_total = long_comments_score_total = 0
        score_distribution = [0, 0, 0, 0, 0]

        with tqdm(total=self._short_comments_quantity, desc="统计短评", unit="comments") as pbar:
            for i in range(0, self._short_comments_quantity, 30):
                comments_score_total, concrete_score_distribution = self._get_comments_score(self._SHORT_COMMENTS_API,
                                                                                             30)
                short_comments_score_total += comments_score_total
                score_distribution = list(numpy.add(score_distribution, concrete_score_distribution))
                pbar.update(30)
            short_comments_average_score = float(short_comments_score_total) / float(self._short_comments_quantity)
            pbar.set_postfix_str(f"统计完毕，短评平均评分{short_comments_average_score:.3f}")
        self._next_comments_cursor = None
        with tqdm(total=self._long_comments_quantity, desc="统计长评", unit="comments") as pbar:
            for i in range(0, self._long_comments_quantity, 30):
                comments_score_total, concrete_score_distribution = self._get_comments_score(self._LONG_COMMENTS_API,
                                                                                             30)
                long_comments_score_total += comments_score_total
                score_distribution = list(numpy.add(score_distribution, concrete_score_distribution))
                pbar.update(30)
            long_comments_average_score = float(long_comments_score_total) / float(self._long_comments_quantity)
            pbar.set_postfix_str(f"统计完毕，长评平均评分{long_comments_average_score:.3f}")
        comments_average_score = float(short_comments_score_total + long_comments_score_total) / float(self._short_comments_quantity + self._long_comments_quantity)
        return comments_average_score, short_comments_average_score, long_comments_average_score, score_distribution
