import datetime
import time
import pandas

df = pandas.read_csv('resources/secwiki_tickers.csv')


SEEKING_ALPHA = "https://seekingalpha.com/symbol/{}/news"
SEEKING_ALPHA_ROOT = "https://seekingalpha.com"

proxies = {
    "http" : "nyc-webproxy.blackrock.com:8080",
    "https" : "nyc-webproxy.blackrock.com:8080"
}

# proxies = {}


class Article(object):
    def __init__(self, ticker=None, time=None, title=None, link=None, sentiment=None):
        self.title = title
        self.link = link
        self.time = time
        self.ticker = ticker
        self.sentiment = sentiment
        self.company = None
        self.date = None

    def __str__(self):
        return self.ticker
        # return "Title: {}\nLink: {}\nTime: {}\nTicker: {}\nSentiment: {}\nCompany: {}".format(self.title,self.link,self.time,self.ticker, self.sentiment, self.company)

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


    def set_ticker(self, tick):
        self.ticker = tick
        try:
            self.company = list((df[df.Ticker==tick]).Name.values)[0]
        except Exception:
            pass


    def to_tuple(self):
        return (self.ticker, self.time, self.title, self.link, self.sentiment)