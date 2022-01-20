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

    def pay_to(self, amount, landlord):



'''    def deduct(self, investor, debt, landlord=None):
        if landlord==None:
            landlord=self.bank
        while(investor.money < debt): #can't pay
            if self.watching: feedback('INSUFFICIENT', investor)
            if investor.assets:
                has_houses = [x for x in investor.assets if investor.assets[x]['HOUSES'] > 0]
                if len(has_houses) > 0:
                    land_ID = random.choice(has_houses)
                    self.sell_house(investor,land_ID)
                else: #time to mortgage property
                    #collect unmortgaged propertyies in one dict
                    unmortgaged = {}
                    for asset in investor.assets:
                        if investor.assets[asset]['MORTGAGED'] == False:
                            unmortgaged[asset] = investor.assets[asset]
                    #mortgage property if possible
                    if len(unmortgaged) > 0:
                        land_ID = random.choice([x for x in unmortgaged])#grab a key, not the dict entry
                        self.mortgage(investor, self.board[land_ID])
                    else: #losing sequence
                        landlord.money += investor.money
                        #transfer mortgaged property to bank
                        for a in investor.assets:
                            self.bank.assets[a] = investor.assets[a]
                        self.bank_auction()
                        return False
            else:#losing sequence
                landlord.money += investor.money
                return False
        #investor can afford it
        investor.money -= debt
        landlord.money += debt
        return True'''

    def buy(self, land):
        investor.money -= land.price
        land.is_owned = True
        land.owner = investor
        investor.assets.append(land)

    def mortgage(self, land):
        if self.watching: feedback('MORTGAGE_PROPERTY', investor, land.name)
        investor.money += land.price/2
        land.is_mortgaged = True

    def count_houses(self):
        if self.assets = []:
            return 0
        i = 0
        for asset in self.assets:
            i += asset.houses
        return i

    def count_hotels(self):
        if self.assets = []:
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

    '''returns the amount of rent due to the tenant
    landing on this investor's railroad'''
    def railroad_rent(investor):
        rr = self.count_railroads()
        if rr==1: return 25
        if rr==2: return 50
        if rr==3: return 100
        if rr==4: return 200
