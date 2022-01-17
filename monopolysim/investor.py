from numpy import random
class Investor:
    def __init__(self, starting_funds):
        self.position = 0 #Start Space
        self.doubles_counter = 0
        self.in_jail = False

        self.money = starting_funds



class Player(Investor):
    def __init__(self):
