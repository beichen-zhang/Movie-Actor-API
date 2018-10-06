import scrapy
from tutorial.tutorial.spiders.Actor import Actor
import re
import csv
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    actor_name = ""
    actor = Actor("","",[])
    url = ""

    def __init__(self, term=None, *args, **kwargs):
        print("new Quotes")
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.url = term
        file = open("actor_stack.txt", "r")
        lines = file.readlines()
        url_left = []
        print("!!!!", str(lines))
        for line in lines:
            if line!="":
                for lin in line.split(",,"):
                    url_left.append(lin)
        self.url = url_left[0]

        file.close()
        file = open("actor_stack.txt", "w")
        for line in url_left:
            if line != self.url:
                file.write(line + ",,")
        file.close()

    def get_actor(self):
        print(23 ,self.actor.name)
        return self.actor

    def start_requests(self):
        print("url:", self.url)
        print(len(self.url))
        actor_name = self.url[30:]
        print(actor_name)
        self.actor_name = actor_name
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        films = response.xpath("//div[@id='mw-content-text']//table[@class='wikitable sortable']//tbody").extract()
        films_tr = []
        if(len(films)==0):
            return;
        for a in list(re.finditer('<tr>', films[0])):
            films_tr.append((a.start(),a.end()))
        film_link =[]
        table = response.xpath('//*[@class="infobox biography vcard"]//tbody').extract()
        with open("table.txt", 'w') as f:
            index = table[0].find("(age")
            f.write(table[0][index+4:index+7])
            f.write('\n')

            for i in range (0,len(films_tr)):
                interval = ""
                if(i!=len(films_tr)-1):
                    interval = films[0] [films_tr[i][1] : films_tr[i+1][0] ]
                title_start = interval.find("title=\"")
                if(title_start!=-1):
                    query = ">"+interval[title_start+7]
                    title_end = interval[title_start+8:].find(query)
                    film_link.append("https://en.wikipedia.org/wiki/"+interval[title_start+7:title_start+7+title_end])
            f.write(str(film_link))
        print("56"+self.actor_name)
        newactor = Actor(self.actor_name,table[0][index+4:index+7],film_link)
        self.actor = newactor

        with open("actor.txt", 'a') as a:
            a.write(self.actor_name+","+table[0][index+4:index+7]+'\n')

        num_row = 0
        with open("movie_stack.txt", 'r') as count:
            lines = count.readlines()
            num_row = len(str(lines).split(",,"))
        with open("movie_stack.txt", 'a') as a:
            for link in film_link:
                a.write(link)
                a.write(',,')



