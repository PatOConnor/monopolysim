from numpy import random

class Bank(Investor):
    def __init__(self):
        Investor.__init__(self)
        self.houses = 32
        self.hotels = 12

    def has_buildings(self):
        if self.houses > 0 or self.hotels > 0:
            return True
        else:
            return False
                                        #readability methods
    def has_houses(self):
        if self.houses > 0:
            return True
        else:
            return False

    def has_hotels(self):
        if self.hotels > 0:
            return True
        else:
            return False

class Investor:
    def __init__(self, starting_funds, name=''):
        self.position = 0 #Start Space
        self.doubles_counter = 0
        self.in_jail = False
        self.is_bankrupt = False
        self.name = name
        self.money = starting_funds
        self.assets = []
        self.jail_cards = 0

    #bank is always present but it sometimes the landlord
    def pay_to(self, amount, landlord, bank=None):
        while not self.can_pay(amount):
            if self.land_with_houses() != []:
                house_land = self.land_with_houses()
                location = random.choice(house_land) #random house
                #location = house_land[-1] #most valuable house
                self.sell_house(location, bank)
            elif self.has_property():
                unmortgaged = self.unmortgaged_land()
                location = random.choice(unmortgaged)
                #location = unmortgaged[-1]
                self.mortgage(location, bank)
            else:
                #lose sequence
                landlord.money += self.money
                self.money = 0
                self.is_bankrupt = True
                self.repo_assets(bank)
                return
        self.money -= amount
        landlord.money += amount
        return

    def buy(self, land):
        self.money -= land.price
        land.is_owned = True
        land.owner = self
        self.assets.append(land)

    def mortgage(self, land, bank):
        if self.watching: feedback('MORTGAGE_PROPERTY', self, land.name)
        bank.pay_to(land.price/2, self)
        land.is_mortgaged = True

    def unmortgage(self, land, bank):
        if self.watching: feedback('UNMORTGAGE_PROPERTY', self, land.name)
        self.pay_to(land.price/2 * 1.1, bank)

    def land_with_houses(self):
        result = []
        for land in self.assets:
            if land.houses > 0 or land.has_hotel:
                result.append(land)
        return result


    def build_house(self, land, bank):
        self.pay_to(land.house_cost, bank)
        land.houses += 1


    def mortgaged_land(self):
        result = []
        for land in self.assets:
            if land.is_mortgaged:
                result.append(land)
        return result

    def trade(self, opponent, land, otherland):
        self.assets.append(otherland)
        otherland.owner = self
        opponent.assets.remove(otherland)

        opponent.assets.append(land)
        land.owner = opponent
        self.assets.remove(land)
        return




    def unmortgaged_land(self):
        result = []
        for land in self.assets:
            if not land.is_mortgaged:
                result.append(land)
        return result

    def can_pay(self, amount):
        if amount < self.money:
            return True
        return False


    def count_houses(self):
        if self.assets == []:
            return 0
        i = 0
        for asset in self.assets:
            i += asset.houses
        return i

    def count_hotels(self):
        if self.assets == []:
            return 0
        i = 0
        for asset in self.assets:
            if asset.has_hotel:
                i += 1
        return i

    def count_railroads(self):
        i = 0
        if self.assets == []:
            return 0
        else:
            for land in self.assets:
                if land.id in [5,15,25,35]:
                    i += 1
            return i

    def repo_assets(self, bank):
        for land in self.assets:
            land.owner = None
            bank.assets.append(land)
            self.assets.remove(land)

    '''returns the amount of rent due to the tenant
    landing on this investor's railroad'''
    def railroad_rent(self):
        rr = self.count_railroads()
        if rr==1: return 25
        if rr==2: return 50
        if rr==3: return 100
        if rr==4: return 200


    #returns list of the spaces this player needs to get a full suit
    def needed_for_monopoly(self):
        result = []



        #check the player assets

















#
