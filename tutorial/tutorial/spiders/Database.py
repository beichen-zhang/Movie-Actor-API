from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from tutorial.tutorial.spiders.quotes_spider import QuotesSpider
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from tutorial.tutorial.spiders.Actor import Actor
import csv
from tutorial.tutorial.spiders.Movie import Movie
from tutorial.tutorial.spiders.website_spider import website_spider
from multiprocessing import Process, Queue
from twisted.internet import reactor
from multiprocessing import Process, Queue
from twisted.internet import reactor, defer
import time


class Database ():
    actor = []
    movie = []

    def __init__(self):
        self.actor =[]
        self.movie =[]

    def append_actor(self,actor_):
        self.actor.append(actor_)
        if len(self.actor) > 260:
            return False

    def append_moive(self,movie_):
        self.movie.append(movie_)
        if len(self.movie) > 130:
            return False

    def add_actor(self):
        with open('actor.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            print(type(spamreader))
            for row in spamreader:
                name = row[0]
                age = row[1]
                film = row[2:]
                actor = Actor(name, age, film)
                print(name,age,film)
                db.append_actor(actor)

    def add_movie(self):
        with open('movie.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                name = row[0]
                gross = row[1]
                star = row[2:]
                movie = Movie(name, gross, star)
                db.append_moive(movie)

    def check_full(self):
        if len(self.actor)< 250:
            return False
        if len(self.movie)< 125:
            return False
        return True

    def check_actor_exist(self, name):
        for each in self.actor:
            if each.name == name:
                return True
        return False

    def check_movie_exist(self, name):
        for each in self.movie:
            if each.name == name:
                return True
        return False

    def crawl(self,obj,url):
        def _crawl(queue):
            print(80)
            # Assume we have a spider class called: WebSpider
            runner = CrawlerRunner()
            res = runner.crawl(obj,term=url)
            #res.addBoth(lambda _: reactor.stop())
            queue.put(res)
            print(85)
            return;

        print(87)
        q = Queue()
        p = Process(target=_crawl, args=(q,))
        print(90)
        p.start()
        print(92)
        res = q.get()
        print(94)
        p.join()
        return res

    def run_actor_crawler(self,url):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()

        d = runner.crawl(QuotesSpider(), term=url)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        self.add_actor()

    def run_movie_crawler(self,url):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()

        d = runner.crawl(website_spider(), term=url)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        self.add_movie()


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(QuotesSpider(),term =1)
    yield runner.crawl(QuotesSpider(), term =2)
    time.sleep(3)

    #reactor.stop()

for i in range(0,10):
    print("round",i)
    crawl()
reactor.run()













