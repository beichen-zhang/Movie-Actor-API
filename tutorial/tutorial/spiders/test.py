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
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(QuotesSpider(),"https://en.wikipedia.org/wiki/Chris_Hemsworth")
    yield runner.crawl(website_spider(),"https://en.wikipedia.org/wiki/Avengers:_Infinity_War")
    reactor.stop()

crawl()
reactor.run()