import scrapy
from tutorial.tutorial.spiders.Actor import Actor
import re
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor,defer
import random
import time
import logging


class QuotesSpider(scrapy.Spider):
    # variable for actor crawler
    name = "quotes"
    actor_name = ""
    actor = Actor("","",[])
    url = ""
    id =0
    # variable for movie crawler
    movie_name = ""
    gross = ""
    star = []

    def __init__(self, term,url = None, *args, **kwargs):
        logger.debug("Start a crawler Success")
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.id = term
        if self.id == 1:
            logger.info("Crawler type: actor information crawler")
            file = open("actor_stack.txt", "r")
        else:
            logger.info("Crawler type: movie information crawler")
            file = open("movie_stack.txt", "r")
        lines = file.readlines()
        url_left = []
        for line in lines:
            if line != "":
                for lin in line.split(",,"):
                    url_left.append(lin)
        # select line from the stack
        self.url = url_left[int(random.uniform(1, 1000))]
        logger.info("crawling from website: %s",self.url)
        file.close()
        if url is not None:
            self.url = url

    # the start request function that call the parser
    def start_requests(self):
        if self.id ==1:
            print("url:", self.url)
            print(len(self.url))
            actor_name = self.url[30:]
            logger.debug("actor name: %s",actor_name)
            print(actor_name)
            self.actor_name = actor_name
            yield scrapy.Request(url=self.url, callback=self.parse_actor)
        else:
            print("this url:", self.url)
            self.movie_name = self.url[30:]
            logger.debug("movie name: %s", self.movie_name)
            yield scrapy.Request(url=self.url, callback=self.parse_movie)

    # parse information for actor
    # id number =1.
    # write the result into actor.txt and the movie link into movie_stack.txt
    def parse_actor(self, response):
        logger.info("enter actor parse function")
        films = response.xpath("//div[@id='mw-content-text']//table[@class='wikitable sortable']//tbody").extract()
        films_tr = []
        if len(films) == 0:
            logger.error("parse failed! Due to unexpected filmology format")
            return
        for a in list(re.finditer('<tr>', films[0])):
            films_tr.append((a.start(),a.end()))
        film_link = []
        table = response.xpath('//*[@class="infobox biography vcard"]//tbody').extract()
        if len(table) == 0:
            logger.error("parse failed! Due to unexpected age format")
            return
        index = table[0].find("(age")
        for i in range(0 ,len(films_tr)):
            interval = ""
            if i != len(films_tr)-1:
                interval = films[0] [films_tr[i][1] : films_tr[i+1][0] ]
            title_start = interval.find("title=\"")
            if title_start != -1:
                query = ">"+interval[title_start+7]
                title_end = interval[title_start+8:].find(query)
                film_link.append("https://en.wikipedia.org/wiki/"+interval[title_start+7:title_start+7+title_end])
        logger.info("name: %s, age: %s", self.actor_name, table[0][index+4:index+7])
        newactor = Actor(self.actor_name,table[0][index+4:index+7],film_link)
        self.actor = newactor
        with open("actor.txt", 'a') as a:
            a.write(self.actor_name+","+table[0][index+4:index+7]+","+",".join(film_link)+'\n')
        with open("movie_stack.txt", 'a') as a:
            for link in film_link:
                if len(link)>7:
                    a.write(link)
                    a.write(',,')

    # parse the gross information of movie
    # called by parse_movie
    def parse_gross(self,table):
        index = table[0].find("Box office")
        index_gross = table[0][index:].find("$")
        gross_end = table[0][index:].find("illion")
        gross_end += index + 6
        index_gross += index+1
        self.gross = table[0][index_gross:gross_end]

    # parse the starring information of movie
    # called by parse_movie
    def parse_starring(self,table):
        index_Starring = table[0].find("Starring")
        index_Starring_end = table[0][index_Starring:].find("<tr>")
        Starring_text = table[0][index_Starring:index_Starring + index_Starring_end]
        self.star = []
        for a in list(re.finditer('title', Starring_text)):
            next = a.start()
            end = ">" + Starring_text[next + 7]
            end_index = Starring_text[next:].find(end)
            end_index += next
            self.star.append("https://en.wikipedia.org/wiki/" + Starring_text[next + 7:end_index - 1])

    # parse information for movie
    # id number =2.
    # write the result into movie.txt and the actor link into actor_stack.txt
    def parse_movie(self, response):
        logger.info("enter actor parse function")
        table = response.xpath('//*[@class="infobox vevent"]//tbody').extract()
        if len(table) == 0:
            logger.error("parse failed! Due to unexpected info box format")
            return
        self.parse_gross(table)
        self.parse_starring(table)
        print("new movie content:",[self.movie_name,self.gross]+self.star)
        logger.debug("gross: %s, name: %s", self.gross, self.movie_name)
        with open("movie.txt", 'a') as a:
            a.write(self.movie_name+","+self.gross+ ","+",".join(self.star)+'\n')
        with open("actor_stack.txt", 'a') as a:
            for link in self.star:
                a.write(link)
                a.write(",,")


configure_logging()
logger = logging.getLogger('server_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log_status.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
cha = logging.StreamHandler()
cha.setLevel(logging.INFO)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
logger.addHandler(cha)
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(QuotesSpider(term=1),term =1)
    yield runner.crawl(QuotesSpider(term=2), term =1)
    time.sleep(3)

for i in range(0,2):
    logger.debug("the crwaling processing in round %s",str(i))
    crawl()
reactor.run()



