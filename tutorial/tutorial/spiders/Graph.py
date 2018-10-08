from tutorial.tutorial.spiders.Database import Database
import numpy as np
import logging
import json

class Graph:
    actor_dict={}
    movie_dict={}
    graph =[]
    top =[]
    old =[]
    db = Database()

    # initialize the graph function
    def __init__(self,db):
        self.graph = np.zeros([len(db.movie),len(db.actor)])

        self.db =db
        self.store_data(db)
        self.sort_rank()

    # sort the age and salary
    def sort_rank(self):
        self.top =[]
        self.old =[]
        def getkey(elem):
            return elem[1]
        for actor_name in self.actor_dict:
            index = self.actor_dict[actor_name][1]
            actor = self.actor_dict[actor_name][0]
            total = (self.graph[:,index].sum())
            self.old.append((actor_name,actor.age_int))
            self.top.append((actor_name,total))
        self.top.sort(key=getkey)
        self.old.sort(key=getkey)

    # the actor attribute of the graph. Store in a dictionary. actor name as the
    # key and (actor object, index) as the value
    def store_actor_index(self, db):
        for actor in db.actor:
            if actor.name not in self.actor_dict.keys():
                index = len(self.actor_dict)
                self.actor_dict[actor.name] = (actor,index)

    # the movie attribute of the graph. Store in a dictionary. movie name as the
    # key and (movie object, index) as the value
    def store_movie_index(self, db):
        for movie in db.movie:
            if movie.name not in self.movie_dict.keys():
                index = len(self.movie_dict)
                self.movie_dict[movie.name] = (movie,index)

    # implement the graph
    def store_data(self,db):
        self.store_actor_index(db)
        self.store_movie_index(db)
        for name in self.actor_dict:
            actor = self.actor_dict[name][0]
            actor_index = self.actor_dict[name][1]
            movies = actor.movie
            for movie in movies:
                if movie in self.movie_dict.keys():
                    movie_obj = self.movie_dict[movie][0]
                    movie_index = self.movie_dict[movie][1]
                    gross = movie_obj.money
                    if gross == 0:
                        gross = 1000000
                        movie_obj.money = gross
                    self.graph[movie_index][actor_index]=gross

        for name in self.movie_dict:
            movie = self.movie_dict[name][0]
            movie_index = self.movie_dict[name][1]
            stars = movie.star
            gross = movie.money
            if gross ==0:
                gross = 1000000
                movie.money = gross
            for star in stars:
                if star in self.actor_dict.keys():
                    star_index = self.actor_dict[star][1]
                    self.graph[movie_index][star_index] = gross

    # query function that find salary based on movie name
    def find_gross(self,movie_name):
        if movie_name not in self.movie_dict.keys():
            logging.error("the movie not in the graph")
        else:
            movie = self.movie_dict[movie_name][0]
            return movie.money

    # search actor given a movie name,
    # return "actor info not available" if not found
    def search_actor_by_movie(self, movie_name):
        if movie_name not in self.movie_dict.keys():
            logging.error("the movie not in the graph")
        else:
            movie = self.movie_dict[movie_name][0]
            if len(movie.star)>0:
                return ",".join(movie.star)
            else:
                return "actor info not available"

    # search movie given an actor name,
    #  return "movie info not available" if not found
    def search_movie_by_actor(self,actor_name):
        if actor_name not in self.actor_dict.keys():
            logging.error("the actor not in the graph")
        else:
            actor = self.actor_dict[actor_name][0]
            if len(actor.movie)>0:
                return ",".join(actor.movie)
            else:
                return "movie info not available"

    # get function for the top salary
    def get_top(self,num):
        ret_val =[]
        for actor in self.top[-num:]:
            ret_val.append(actor[0])
        ret_val.reverse()
        return ",".join(ret_val)

    # get function for the eldest
    def get_old(self,num):
        ret_val =[]
        for actor in self.old[-num:]:
            ret_val.append(actor[0])
        ret_val.reverse()
        return ",".join(ret_val)

    # query the actor given a year
    def actor_in_year (self,num):
        year = 2018-num
        ret_val =[]
        for actor_name in self.actor_dict:
            actor = self.actor_dict[actor_name][0]
            if (actor.age_int ==year):
                ret_val.append(actor.name)
        if len(ret_val) ==0:
            return "actor not found"
        return ",".join(ret_val)

    # query the movie given a year
    def movie_in_year (self,num):
        return self.db.find_movie(num)

    def read_json(self):
        with open("database.json", "r") as read_file:
            data = json.load(read_file)
        return data

    def query(self):
        # 1. Find how much a movie has grossed
        print(1, self.find_gross("Garden of Evil"))

        # 2. Find which movies an actor has worked in
        print(2, self.search_movie_by_actor("Marisa Tomei"))

        # 3. List which actors worked in a movie
        print(3, self.search_actor_by_movie("Garden of Evil"))

        # 4. List the top X actors with the most total grossing value
        print(4, self.get_top(3))

        # List the oldest X actors
        print(5, self.get_old(3))

        # List all the movies for a given year
        print(6, self.actor_in_year(1972))

        # List all the actors for a given year
        print(7, self.movie_in_year(1977))


db = Database()
db.store_actor("actor.txt")
db.store_movie("movie.txt")
graph = Graph(db)
graph.query()
