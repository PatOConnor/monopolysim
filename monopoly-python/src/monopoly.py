from common.cards import chance, community_chest
from common.boards import standard_board
from investor import Investor#, Player


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
            if self.type == ['LAND']:
                self.price = info['PRICE']
                self.house_cost = info['HOUSE_COST']
                self.suit = info['SUIT']
                self.rents = info['RENTS']
                self.houses = 0
                self.owned = False
                self.owner = None

    def __init__(self, board, player_count):
        #making investors
        self.investors = [Investor(starting_funds=1500, name='Player_'+str(x)) for x in range(player_count)]
        #making monopoly board
        self.board = [Space(space_data) for space_data in board]

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


    def commerce(self, investor, land):
            if not land.owned:
                if investor.money > land.price:
                    self.buy(investor,land)
                else:
                    self.auction(land)
            else:
                if land.type == 'RAILROAD':
                    railroad_owners = [self.board[5].owner, self.board[15].owner,
                                      self.board[25].owner, self.board[35].owner]
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
                landlord = self.investors[self.board[investor.position].owner]
                status = self.deduct(investor, rent, landlord)
                if not status:
                    return False #investor got broke paying rent

    def deduct(self, investor, debt, landlord=None):
        if landlord==None:
            landlord=self.bank

        while(investor.money < debt): #can't pay
            if investor.assets:
                #investor mortgages assets
            else:
                landlord.money += investor.money
                return False#you lose
        landlord.money += investor.money




''''

                NEXT STEP: REFORMAT THE FOLLOWING METHOD INTO A MORTGAGING METHOD


''''
    def charge_rent(self, investor, rent):
        while(investor.money < rent):

            if investor.assets = []:
                landlord.money += investor.money
                investor.deduct(investor.money)
                return False #couldn't pay rent


        if investor.money >= rent:
            investor.deduct(rent)
            landlord.money += rent
        else:
            while(investor.money)


                if investor.money >= rent:
                    investor.money -= rent
                    self.investors[land.owner].money += rent
                else: #not enough money to cover rent
                    difference = rent - investor.money
                    investor.money -= rent
                    while(len(investor.assets) > 0):
                        #mortgage a random LAND towards the difference
                        mortgage = self.mortgage(investor)
                        difference -= mortgage
                        self.investors[land.owner].money += mortgage
                        if difference <= 0:
                            investor.money -= difference#get money back
                            break
                    if not investor.assets and investor.money < 0:




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
