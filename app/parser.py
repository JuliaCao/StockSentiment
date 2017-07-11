import requests
from bs4 import BeautifulSoup as Soup
from app.blueprints.app import analyze
import pandas
import datetime
import time

df = pandas.read_csv('secwiki_tickers.csv')

SEEKING_ALPHA = "https://seekingalpha.com/symbol/{}/news"

proxies = {
    "http" : "nyc-webproxy.blackrock.com:8080",
    "https" : "nyc-webproxy.blackrock.com:8080"
}

class Article():
    def __init__(self, title=None, link=None, time=None):
        self.title = title
        self.link = link
        self.time = time
        self.ticker = None
        self.sentiment = None
        self.company = None

    def __str__(self):
        return "Title: {}\nLink: {}\nTime: {}\nTicker: {}\nSentiment: {}\nCompany: {}".format(self.title,self.link,self.time,
                                                                                   self.ticker, self.sentiment, self.company)

    def parse_date(self, date):
        l = date.split(",")
        # d = datetime.datetime()
        if l[0] == "Today":
            d = datetime.datetime.strptime("".join(l[1:]), " %I:%M %p")
            today = datetime.datetime.today()
            self.date = d.replace(day=int(today.strftime("%d")),year=2017)
            # d.replace(day=datetime.datetime.today())
        elif l[0] == "Yesterday":
            d = datetime.datetime.strptime("".join(l[1:]), " %I:%M %p")
            today = datetime.datetime.today() - datetime.timedelta(1)
            self.date = d.replace(day=int(today.strftime("%d")),year=2017)
        else:
            # "Sat, Jul. 8, 9:53 AM"
            self.date = datetime.datetime.strptime(date,"%a, %b. %d, %I:%M %p")
            self.date = self.date.replace(year=2017)
            # self.date = self.date.to
            # print(self.date)

        self.time = time.mktime(self.date.timetuple())
        # self.time = self.date

    def parse_link(self,bullets):
        div = bullets.find("a", {"class": "market_current_title"})
        self.title = div.text
        self.link = div["href"]

    def get_sentiment(self, text):
        self.sentiment = analyze(text, self.company)

    def set_ticker(self, tick):
        self.ticker = tick
        self.company = list((df[df.Ticker==tick]).Name.values)[0]
        
    def to_tuple(self):
        return (self.time,self.ticker,self.title,self.link,self.sentiment)

def get_bullets_for_ticker(tick):
    res = requests.get(SEEKING_ALPHA.format(tick), proxies=proxies)
    print(res)
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
    articles = get_articles(["AAPL","AMD"])
