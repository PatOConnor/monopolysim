from numpy import random
class Investor:
    def __init__(self, starting_funds, name):
        self.position = 0 #Start Space
        self.doubles_counter = 0
        self.in_jail = False

        self.money = starting_funds
        #format: key is LAND_ID, value is mortgage status
        self.assets = {2:{'MORTGAGED':False, 'HOUSES':0}}
        self.jail_cards = 0


#class Player(Investor):
    #def __init__(self):
