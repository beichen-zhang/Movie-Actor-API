import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import re
import csv


class website_spider(scrapy.Spider):
    name = "p1"
    movie_name = ""
    url = ""
    gross =""
    star = []

    def __init__(self, term=None, *args, **kwargs):
        print("new movie accept")
        super(website_spider, self).__init__(*args, **kwargs)
        file = open("movie_stack.txt", "r")
        lines = file.readlines()
        url_left = []
        print("!!!!",len(lines))
        for line in lines:
            if line!="":
                for lin in line.split(",,"):
                    url_left.append(lin)
        self.url = url_left[0]
        print("self.url=" , self.url)
        file.close()
        file = open("movie_stack.txt", "w")
        count =0
        for line in url_left:
            count += 1
            if (count > 50):
                continue
            if line != self.url and line !="":
                file.write(line + ",,")
        file.close()

    def start_requests(self):
        print("this url:", self.url)
        self.movie_name = self.url[30:]
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        table = response.xpath('//*[@class="infobox vevent"]//tbody').extract()

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






