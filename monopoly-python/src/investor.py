from numpy import random
class Investor:
    def __init__(self, starting_funds, name):
        self.position = 0 #Start Space
        self.doubles_counter = 0
        self.in_jail = False

        self.money = starting_funds
        self.assets = []



#class Player(Investor):
    #def __init__(self):
