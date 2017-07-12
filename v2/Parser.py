import requests
import time
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features
from bs4 import BeautifulSoup as Soup
import pandas
from watson_developer_cloud import NaturalLanguageUnderstandingV1

from Article import Article

SEEKING_ALPHA = "https://seekingalpha.com/symbol/{}/news"
SEEKING_ALPHA_ROOT = "https://seekingalpha.com"

proxies = {
    "http" : "nyc-webproxy.blackrock.com:8080",
    "https" : "nyc-webproxy.blackrock.com:8080"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# proxies = {}


class Parser(object):

    def __init__(self, db):
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            username="33ef4781-a0cc-4486-b186-28d5e78bdc06",
            password="hN7h6o6sTnD4",
            version="2017-07-11")
        self.db=db

    def get_bullets_for_ticker(self, tick):
        res = requests.get(SEEKING_ALPHA.format(tick), proxies=proxies, headers=headers)
        if res.status_code != 200:
            print("Trouble getting articles for {}".format(tick))
            return []

        soup = Soup(res.text, "lxml")
        results = []
        for bullets in soup.findAll("li", {"class": "mc_list_li"}):
            try:
                art = Article()
                art.set_ticker(tick)
                art.parse_date(bullets.text.split('\n')[2:3][0])
                art.sentiment = self.analyze(''.join(bullets.text.split('\n')[3:-4]),art.ticker)
                art.parse_link(bullets)
                results.append(art)
            except Exception:
                pass

        for r in results:
            print(r)
        return results

    def get_articles(self, tickers):
        articles = []
        for ticker in tickers:
            time.sleep(1)
            articles += self.get_bullets_for_ticker(ticker)
        return articles


    def analyze(self, content, keyword):

        response = self.natural_language_understanding.analyze(
            text=content,
            features=[
                Features.Sentiment(
                    # Emotion options
                    targets=[keyword]
                )
            ]
        )
        score = response["sentiment"]["document"]["score"]
        return score

    def populate(self, tickers):
        articles = self.get_articles(tickers)
        for a in articles:
            self.db.insert(a)
