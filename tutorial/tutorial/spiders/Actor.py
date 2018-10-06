
class Actor ():
    name = ""
    age = ""
    movie = []



    def __init__(self, name_, age_, movie_list):
        self.name =name_
        self.age =age_
        self.movie=movie_list.copy()

    def print(self):
        print(self.name)
        print(self.age)
        print(self.movie)