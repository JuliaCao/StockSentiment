import sqlite3
import datetime

from Article import Article

DB_PATH = "data/stockSentiment.db"

class DB(object):

    def __init__(self, purge=False):
        self.db = None
        self.init_db(purge=purge)

    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if not self.db:
            self.db = self.connect_db()
        return self.db

    def init_db(self, purge):
        """Initializes the database."""
        db = self.get_db()
        if purge:
            with open('resources/schema.sql') as f:
                db.cursor().executescript(f.read())
        db.commit()

    def connect_db(self):
        """Connects to the specific database."""
        rv = sqlite3.connect('data/stockSentiment.db', check_same_thread=False)
        rv.row_factory = sqlite3.Row
        return rv

    def insert(self, art):
        db = self.get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO entries (ticker, time, title, link, sentiment) VALUES (?, ?, ?, ?, ?)", art.to_tuple())
        db.commit()

    def get_articles(self, tickers):
        db = self.get_db()
        articles = []
        for tick in tickers:
            print tick
            cur = db.cursor()
            q = "SELECT ticker, time, title, link, sentiment FROM entries WHERE ticker='{}' ORDER BY time DESC LIMIT 1".format(tick.upper())
            print q
            cur.execute(q)
            recs = cur.fetchall()
            for rec in recs:
                print rec
                articles.append(Article(rec[0],rec[1],rec[2],rec[3],rec[4]))
        return articles

    def get_general_articles(self):
        db = self.get_db()
        cur = db.cursor()
        cur.execute("SELECT DISTINCT ticker FROM entries")
        rows = cur.fetchall()
        articles = []

        for row in rows:
            cur = db.cursor()
            q = "SELECT ticker, time, title, link, sentiment FROM entries WHERE ticker='{}' ORDER BY time DESC LIMIT 1".format(str(row[0]).decode('utf8'))
            cur.execute(q)
            recs = cur.fetchall()
            for rec in recs:
                d = datetime.datetime.fromtimestamp(int(rec[1])).strftime('%Y-%m-%d %H:%M:%S')
                sent = float(rec[4]) * 100
                articles.append(Article(rec[0],d,rec[2],rec[3],rec[4]))
        return articles


        # a = Article('AAPL', "1234", "TITLE", "https://google.com", "-.5")
        # b = Article('AAPL', "1aadf234", "othertitle", "https://google.com", ".5")
        # c = Article('AAPL', "1234", "TITLE", "https://google.com", "-.75")
        # d = Article('AAPL', "1aadf234", "othertitle", "https://google.com", "1")
        # e = Article('AAPL', "1aadf234", "othertitle", "https://google.com", "0")
