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
            if self.type == ['PROPERTY']:
                self.price = info['PRICE']
                self.house_cost = info['HOUSE_COST']
                self.suit = info['SUIT']
                self.rents = info['RENTS']
                self.houses = 0

    def __init__(self, board, player_count):
        #making investors
        self.investors = [Investor(starting_funds=1500, name='Player_'+str(x)) for x in range(player_count)]
        #making monopoly board
        self.board = [Space(space_data) for space_data in board]

        self.debtors = []#for bankrupt players

        self.bank = [] #for mortgaged properties

        self.chance_discard = []
        self.chest_discard = []



    def take_turn(self, investor):
        #check if in jail
        if investor.in_jail:
            pass#
            # #TODO option for buying way out of jail
            #

        #
        # option to trade/mortgage
        #

        #roll dice
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        if die1 == die2:
            investor.doubles_counter += 1
            if investor.in_jail: #doubles gets you out of jail
                investor.in_jail = False
            if investor.doubles_counter == 3:
                investor.position = 10 #3x doubles gets you into jail
                investor.doubles_counter = 0
        else:
            investor.doubles_counter = 0

        #
        #  option to trade/mortgage
        #

        #moving to new space
        if not investor.in_jail:
            investor.position += die1 + die2

        if investor.position > len(self.board): #passing GO
            investor.position -= len(self.board)
        #space takes effect
        landing = self.board[investor.position]
        if landing.type == 'GO':
            pass#
        elif landing.type == 'CHANCE':
            self.draw(chance, investor)
        elif landing.type == 'COMMUNITY_CHEST':
            self.draw(community_chest, investor)
        elif landing.type == 'LUXURY_TAX':
            self.luxury_tax(investor)
        elif landing.type == 'INCOME_TAX':
            self.income_tax(investor)
        elif landing.type == 'GO_TO_JAIL':
            investor.position = 10 #Jail
            investor.in_jail = True
        elif landing.type == 'JAIL':
            pass#either walking by or some other effect set .in_jail to True
        elif landing.type == 'FREE_PARKING':
            pass
        elif landing.type in ['PROPERTY','RAILROAD','UTILITY']:
            #
            #   buy property outright
            #
            #   hold auction for property
            #
            #   property is owned
            #
            if landing.type == 'RAILROAD':

            elif landing.type == 'UTILITY':
                pass
        #
        #
        #   Another Opportunity for Free Actions
        #
        #
        return True #player survives turn
