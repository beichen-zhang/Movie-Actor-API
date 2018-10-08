from tutorial.tutorial.spiders.Graph import Graph
from tutorial.tutorial.spiders.Database import Database

import unittest

class Test_Data_Structure(unittest.TestCase):

    def test_store(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        graph = Graph(db)
        self.assertEqual(len(graph.actor_dict), 3)
        self.assertEqual(len(graph.movie_dict), 2)

    def test_gross(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        graph = Graph(db)
        self.assertEqual(graph.find_gross("abc"), 111000000000)
        self.assertEqual(graph.find_gross("Garden of Evil"), 3100000 )

    def test_top(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        graph = Graph(db)
        self.assertEqual(graph.get_top(1),"abc")
        self.assertEqual(graph.get_top(2), "abc,ddd")
    def test_old(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        graph = Graph(db)
        self.assertEqual(graph.get_old(1), "ddd")
        self.assertEqual(graph.get_old(2), "ddd,abc")

    def test_year(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        graph = Graph(db)
        self.assertEqual(graph.actor_in_year(1995),"abc")
        self.assertEqual(graph.movie_in_year(1995),"movie1,movie2,movie3")
    def test_type(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        graph = Graph(db)
        dict = {}
        self.assertEqual(type(graph.actor_dict), type(dict))
        self.assertEqual(type(graph.movie_dict), type(dict))

    def test_db_store(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        self.assertEqual(len(db.actor),3)
        self.assertEqual(len(db.movie),2)

    def test_db_value(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        actor = db.actor[0]
        self.assertEqual(actor.name, "abc")
        self.assertEqual(actor.age," 23")
        self.assertEqual(actor.age_int,23)

    def test_db_actor_movie(self):
        db = Database()
        db.store_actor("actor_test1.txt")
        db.store_movie("movie_test1.txt")
        actor = db.actor[0]
        print(actor.movie[0])
        self.assertEqual(actor.movie[0], "movie1")
        self.assertEqual(actor.movie[1], "movie2")
        self.assertEqual(actor.movie[2], "movie3")

    def test_db_count(self):
        db = Database()
        db.store_movie("movie.txt")
        db.store_actor("actor.txt")
        self.assertTrue(len(db.actor)>250)
        self.assertTrue(len(db.movie) > 125)

if __name__ == '__main__':
    unittest.main()
