from common.cards import chance, community_chest
from common.boards import standard_board
from investor import Investor#, Player
from numpy import random


def run():
    game = Monopoly(board=standard_board, player_count=4)
    running = True
    while(running):#TODO while at least two players aren't bankrupt
        for investor in game.investors:
            player_status = game.take_turn(investor)
            if not player_status:
                game.debtors.append(investor)
                game.investors.remove(investor)
    print(game.investors[0].name+' Wins with an account of $'+game.investors[0].money)




class Monopoly:
    class Space:
        def __init__(self, info):
            self.name = info['NAME']
            self.type = info['TYPE']
            if self.type in  ['LAND', 'UTILITY', 'RAILROAD']:
                self.price = info['PRICE']
                self.owned = False
                self.owner = None
            if self.type == info['LAND']:
                self.house_cost = info['HOUSE_COST']
                self.suit = info['SUIT']
                self.rents = info['RENTS']
            self.id = 0


    def __init__(self, board, player_count):
        #making investors
        self.investors = [Investor(starting_funds=1500, name='Player_'+str(x)) for x in range(player_count)]
        #making monopoly board
        self.board = [Space(space_data) for space_data in board]
        for i in len(self.board):
            self.board.id = i


        self.debtors = []#for bankrupt players

        self.bank = Investor(starting_funds=19080,name='Bank') #for mortgaged properties

        self.chance_discard = []
        self.chest_discard = []



    def take_turn(self, investor):
        #check if in jail
        if investor.in_jail:
            pass#
            # #TODO option for buying way out of jail

        #roll dice
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        if die1 != die2:
            investor.doubles_counter = 0
        else:
            investor.doubles_counter += 1
            if investor.in_jail: #doubles gets you out of jail
                investor.in_jail = False
            if investor.doubles_counter == 3:
                self.move(investor,10) #3x doubles gets you into jail
                investor.doubles_counter = 0

        #moving to new space
        if not investor.in_jail:
            newposition = (investor.position + die1 + die2) % 40
            self.move(investor, newposition)
            liquidity = self.board_effect(investor)
            if not liquidity:
                return False #bankrupt
        if investor.doubles_counter > 0:
            self.take_turn(investor)
        return True #player survives turn



    def move(self,investor, target_location, pass_go=True):
        if investor.position > target_location:
            if pass_go:
                investor.money += 200
        investor.position = target_location


    def board_effect(self, investor):
        land = self.board[investor.position]
        if land.type in ['GO', 'JAIL', 'FREE_PARKING']:
            pass#nothing happens when you land on these
        elif land.type in ['COMMUNITY_CHEST', 'CHANCE']:
            self.draw(investor, land.type)
        elif land.type == 'LUXURY_TAX':
            self.luxury_tax(investor)
        elif land.type == 'INCOME_TAX':
            self.income_tax(investor)
        elif land.type == 'GO_TO_JAIL':
            self.move(investor,10,pass_go=False)
            investor.in_jail = True
        elif land.type in ['LAND','RAILROAD','UTILITY']:
            self.land_actions(investor, land)


    def land_actions(self, investor, land):
        if not land.owned:
            if investor.money > land.price:
                self.buy(investor,land)
            else:
                self.auction(land)
        else:
            #calculate value of rent
            if land.type == 'RAILROAD':
                railroads = [5,15,25,35]
                railroad_owners = [self.board[x].owner for x in railroads]
                matches = 0
                for r in railroad_owners:
                    if r == land.owner:
                        matches += 1
                if matches == 1:
                    rent = 25
                elif matches == 2:
                    rent = 50
                elif matches == 3:
                    rent = 100
                elif matches == 4:
                    rent = 200
            elif land.type == 'UTILITY':
                if self.board[12].owner == self.board[28].owner:#both utilities
                    rent = (die1 + die2) * 10
                else:
                    rent = (die1 + die2) * 7
            else: #standard property
                rent = land.rent[land.houses]

            #charge the rent
            landlord = self.investors[self.board[investor.position].owner]
            status = self.deduct(investor, rent, landlord)
            if not status:
                return False #investor got broke paying rent
        return True

    def deduct(self, investor, debt, landlord=None):
        if landlord==None:
            landlord=self.bank

        while(investor.money < debt): #can't pay
            if investor.assets:
                has_houses = []]
                for a in investor.assets:
                    if a['HOUSES'] > 0:
                        has_houses.append(a)
                if len(has_houses) > 0:
                    land_ID = random.choice(has_houses)
                    self.sell_house(investor,land_ID)
                else: #time to mortgage property
                    unmortgaged = {}
                    for asset in investor.assets:
                        if asset['MORTGAGED'] == False:
                            unmortgaged[asset] = investor.assets[asset]
                    if len(unmortgaged) > 0:
                        land_ID = max(unmortgaged, key=unmortgaged.get)
                        self.mortgage(investor, land_ID)
                    else: #all properties mortgaged, houses sold, and still not enough
                        landlord.money += investor.money
                        for a in investor.assets:
                            #transfer mortgaged property to bank
                            self.bank.assets[a] = investor.assets[a]
                        self.bank_auction()
                        return False#you lose
            else:
                landlord.money += investor.money
                return False#you lose
        investor.money -= debt
        landlord.money += debt
        return True

    def sell_house(self, investor, land_ID):
        investor.assets[land_ID]['HOUSES'] -= 1
        investor.money += self.board[land_ID]['HOUSE_COST']/2


    def mortgage(self, investor, land_ID):
        investor.money += self.board[land_ID].price/2
        investor.asset[land_ID]['MORTGAGED'] = True


    def bank_auction(self):
        for a in self.bank.assets:
            self.auction(a)


    def buy(self, investor, land_ID):
        investor.money -= self.board[land_ID].price
        newland = {'MORTGAGED':False, 'HOUSES':0}
        investor.assets[land_ID] = newland

    def auction(self, land_ID, is_mortgaged=False):
        bid = 0
        while(True):#until property is sold
            buyers = [x for x in self.investors if x.money > bid]:
            if len(buyers) > 1:
                bidder = random.choice(buyers)
                #bid increases by no more than 50
                bid += random.randint(bid,min(bidder.money, bid+50))
            #1 out of 3 shot for now
            win_cond = 0.25 < random.random()
            if win_cond or len(buyers) == 0:
                bidder.money -= bid
                newland = {'MORTGAGED':is_mortgaged, 'HOUSES':0}
                bidder.assets[land_ID] = newland.id
                break


    def luxury_tax(self, investor):
        investor.money -= 75
        if investor.money < 0:
            investor.money += self.mortgage(investor)

    def income_tax(self, investor):
        if investor.money > 2000:
            investor.money -= 200
        else:
            investor.money -= investor.money//10


    def draw(self, investor, deck):
        if deck == 'CHANCE':
            card = chance.pop()
            chance_discard.append(card)
        else:
            card = community_chest.pop()
            chest_discard.append(card)
        if card['EFFECT'] = travel:
