from tutorial.tutorial.spiders.Movie import Movie
from tutorial.tutorial.spiders.Actor import Actor

import json



class Database ():
    actor = []
    movie = []
    def __init__(self):
        self.actor =[]
        self.movie =[]

    # parse the actor.txt to actor object, store in database
    def store_actor(self, filename):
        file = open(filename,"r")
        lines = file.readlines()
        for line in lines:
            if line[-1]=='\n':
                line = line[0:len(line)-1]
            if line.find(",") == -1:
                continue
            if line[0]=='<':
                continue
            attribute = line.split(",")
            if(len(attribute)<2):
                print("too short", attribute)
                continue
            self.parse_actor(attribute)
        file.close()

    def parse_actor(self,attribute):
        age = attribute[1]
        name = attribute[0]
        try:
            i = int(age)
        except ValueError:
            i = 20
        movie_list = []
        if len(attribute) > 2:
            for movie in attribute[2:]:
                movie_list.append(movie[30:])
        actor = Actor(name, age, movie_list)
        actor.age_int = i
        self.actor.append(actor)

    # parse the movie.txt to movie object, store in database
    def store_movie(self,filename):
        file = open(filename, "r")
        lines = file.readlines()
        for line in lines:
            if line[-1]=='\n':
                line = line[0:len(line)-1]
            if(line[0:3]=="<li"):
                self.handle_movie(line)
                continue
            attribute = line.split(",")
            if len(attribute)>=2:
                name = attribute[0]
                gross= attribute[1]
                movie = Movie(name,gross,[])
                movie.money = self.gross_to_money(gross)
            else:
                movie = Movie(attribute[0],"",[])
            actor_list =[]
            for actor in attribute[2:]:
                actor_list.append(actor[30:])
            movie.star = actor_list
            self.movie.append(movie)
        file.close()

    def gross_to_money(self,gross):
        parts = gross.split(" ")
        if len(parts) == 2:
            if parts[1] == "million":
                try:
                    return float(parts[0]) * 1000000
                except ValueError:
                    return 0
            if parts[1] == "billion":
                try:
                    return float(parts[0]) * 1000000000
                except ValueError:
                    return 0

    def handle_movie(self,line):
        index = line.find("title=")
        title = line[index+7:]
        title_end= title.find((">"+title[0]))
        title = title[0:title_end-1]
        self.movie.append(Movie(title,"",[]))

    # find the movie given a number
    def find_movie(self,num):
        year = 2018-num
        target = Actor("void","-1",[])
        for actor in self.actor:
            if actor.age_int == year:
                target = actor
                break
        ret_val = []
        for movie in target.movie:
            ret_val.append(movie)
        return ",".join(ret_val)

    # store the database into the json file with indentation of 4
    def store_json(self):
        with open('database.json', 'w') as outfile:
            actor_list = []
            for actor in self.actor:
                actor_dict = {}
                actor_dict["name"] = actor.name
                actor_dict["age"] = actor.age
                actor_dict["movie"] = actor.movie
                actor_dict["age_int"] = actor.age_int
                actor_list.append(actor_dict)

            movie_list = []
            for movie in self.movie:
                movie_dict = {}
                movie_dict["name"] = movie.name
                movie_dict["gross"] = movie.gross
                movie_dict["star"] = movie.star
                movie_dict["money"] = movie.money
                movie_list.append(movie_dict)

            dictionary = {}
            dictionary["actor"] = actor_list
            dictionary["movie"] = movie_list
            json.dump(dictionary, outfile, indent=4)

db = Database()
db.store_actor("actor.txt")
db.store_movie("movie.txt")











