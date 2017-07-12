import requests
from bs4 import BeautifulSoup as Soup
from blueprints.app import analyze
import pandas
import datetime
import time

df = pandas.read_csv('secwiki_tickers.csv')

SEEKING_ALPHA = "https://seekingalpha.com/symbol/{}/news"
SEEKING_ALPHA_ROOT = "https://seekingalpha.com"

# proxies = {
#     "http" : "nyc-webproxy.blackrock.com:8080",
#     "https" : "nyc-webproxy.blackrock.com:8080"
# }

proxies = {}

class Article():
    def __init__(self, title=None, link=None, time=None):
        self.title = title
        self.link = link
        self.time = time
        self.ticker = None
        self.sentiment = None
        self.company = None
        self.date = None

    def __str__(self):
        return "Title: {}\nLink: {}\nTime: {}\nTicker: {}\nSentiment: {}\nCompany: {}".format(self.title,self.link,self.time,
                                                                                   self.ticker, self.sentiment, self.company)

    def parse_date(self, date):
        l = date.split(",")
        if l[0] == "Today":
            d = datetime.datetime.strptime("".join(l[1:]), " %I:%M %p")
            today = datetime.datetime.today()
            self.date = d.replace(day=int(today.strftime("%d")), year=2017)
        elif l[0] == "Yesterday":
            d = datetime.datetime.strptime("".join(l[1:]), " %I:%M %p")
            today = datetime.datetime.today() - datetime.timedelta(1)
            self.date = d.replace(day=int(today.strftime("%d")), year=2017)
        else:
            self.date = datetime.datetime.strptime(date,"%a, %b. %d, %I:%M %p")
            self.date = self.date.replace(year=2017)

        self.time = time.mktime(self.date.timetuple())

    def parse_link(self,bullets):
        div = bullets.find("a", {"class": "market_current_title"})
        self.title = div.text
        self.link = SEEKING_ALPHA_ROOT + div["href"]

    def get_sentiment(self, text):
        self.sentiment = analyze(''.join(text), self.ticker)

    def set_ticker(self, tick):
        self.ticker = tick
        self.company = list((df[df.Ticker==tick]).Name.values)[0]


def get_bullets_for_ticker(tick):
    res = requests.get(SEEKING_ALPHA.format(tick), proxies=proxies)
    if res.status_code != 200:
        print("Trouble getting articles for {}".format(tick))
        return []

    soup = Soup(res.text, "lxml")
    results = []
    for bullets in soup.findAll("li", {"class": "mc_list_li"}):
        art = Article()
        art.set_ticker(tick)
        art.parse_date(bullets.text.split('\n')[2:3][0])
        art.get_sentiment(bullets.text.split('\n')[3:-4])
        art.parse_link(bullets)
        results.append(art)

    for r in results:
        print(r)
    return results


def get_articles(tickers):
    articles = []
    for ticker in tickers:
        articles += get_bullets_for_ticker(ticker)
    return articles


if __name__ == "__main__":
    articles = get_articles(["AAPL","FB"])
