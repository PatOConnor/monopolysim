from numpy import random
class Investor:
    def __init__(self, starting_funds, name=''):
        self.position = 0 #Start Space
        self.doubles_counter = 0
        self.in_jail = False
        self.name = name
        self.money = starting_funds
        #format: {LAND_ID:{'MORTGAGED':True/False, 'HOUSES':N}}
        self.assets = {}
        self.jail_cards = 0


#class Player(Investor):
    #def __init__(self):
