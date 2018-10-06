import scrapy
from tutorial.tutorial.spiders.Actor import Actor
import re
import csv
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
import os
import random


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    actor_name = ""
    actor = Actor("","",[])
    url = ""
    id =0

    movie_name = ""
    gross = ""
    star = []

    def __init__(self, term=None, *args, **kwargs):
        print("new Quotes")
        super(QuotesSpider, self).__init__(*args, **kwargs)
        file = open("id.txt", "r")
        lines = file.readlines()
        for line in lines:
            if line =="a":
                self.id =1
            else:
                self.id =2

        file = open("id.txt", "w")
        if self.id ==1:
            file.write("b")
        else:
            file.write("a")

        if (self.id == 1):
            print("actor crawl")
        else:
            print("movie crawl")

        if(self.id ==1):

            file = open("actor_stack.txt", "r")
        else:
            file = open("movie_stack.txt", "r")
        lines = file.readlines()
        url_left = []

        for line in lines:
            if line!="":
                for lin in line.split(",,"):
                    url_left.append(lin)
        self.url = url_left[(int)(random.uniform(1, 1000))]

        print("actor left number", url_left[:10])
        file.close()

        #count =0
        #if (self.id == 1):
        #    file = open("actor_stack.txt", "w")
        #else:
        #    file = open("movie_stack.txt", "w")
        #for line in url_left:
        #    file.write(lines[len(self.url)+2:])
        #file.close()

    def start_requests(self):
        if self.id ==1:
            print("url:", self.url)
            print(len(self.url))
            actor_name = self.url[30:]
            print(actor_name)
            self.actor_name = actor_name
            yield scrapy.Request(url=self.url, callback=self.parse1)
        else:
            print("this url:", self.url)
            self.movie_name = self.url[30:]
            yield scrapy.Request(url=self.url, callback=self.parse2)


    def parse1(self, response):
        print("parse1")
        films = response.xpath("//div[@id='mw-content-text']//table[@class='wikitable sortable']//tbody").extract()
        films_tr = []
        if(len(films)==0):
            return
        for a in list(re.finditer('<tr>', films[0])):
            films_tr.append((a.start(),a.end()))
        film_link =[]
        table = response.xpath('//*[@class="infobox biography vcard"]//tbody').extract()
        if (len(table)==0):
            return
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
                if len(link)>7:
                    a.write(link)
                    a.write(',,')


    def parse2(self, response):
        print("parse2")
        table = response.xpath('//*[@class="infobox vevent"]//tbody').extract()
        if(len(table)==0):
            return;
        index = table[0].find("Box office")
        index_gross =  table[0][index:].find("$")
        gross_end = table[0][index:].find("illion")
        gross_end+=index +6
        index_gross+=index+1
        print(table[0][index_gross:gross_end])
        self.gross=table[0][index_gross:gross_end]

        index_Starring = table[0].find("Starring")
        index_Starring_end = table[0][index_Starring:].find("<tr>")
        Starring_text = table[0][index_Starring:index_Starring+index_Starring_end]
        for a in list(re.finditer('title', Starring_text)):
            next = a.start()
            end = ">" + Starring_text[next + 7]
            end_index = Starring_text[next:].find(end)
            end_index += next
            self.star.append("https://en.wikipedia.org/wiki/"+Starring_text[next + 7:end_index - 1])
        print("new movie content:",[self.movie_name,self.gross]+self.star)
        with open("movie.txt", 'a') as a:
            a.write(self.movie_name+","+self.gross+ '\n')

        num_row =0
        with open("actor_stack.txt", 'r') as count:
            lines = count.readlines()
            num_row = len(str(lines).split(",,"))
        with open("actor_stack.txt", 'a') as a:
            print("add to actor link:",str(self.star))
            for link in self.star:
                a.write(link)
                a.write(",,")

