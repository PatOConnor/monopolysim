from common.cards import chance, community_chest
from common.boards import standard_board
from investor import Investor#, Player
from numpy import random
from feedback import feedback#, user_feedback




def run(iswatching=True):
    game = Monopoly(board=standard_board, player_count=4, watching=iswatching)
    running = True
    if game.watching: feedback('GAME_START')
    #input()
    while(running):#TODO while at least two players aren't bankrupt
        if game.watching:
            game.turn_status()
            input()
        for investor in game.investors:
            #input()
            player_status = game.take_turn(investor)
            if not player_status:
                if game.watching: feedback('PLAYER_BANKRUPT', investor)
                game.debtors.append(investor)
                game.investors.remove(investor)
        game.turn_count += 1
    print(game.investors[0].name+' Wins with an account of $'+game.investors[0].money)

class Space:
    def __init__(self, info):
        self.name = info['NAME']
        self.type = info['TYPE']
        if self.type in  ['LAND', 'UTILITY', 'RAILROAD']:
            self.price = info['PRICE']
            self.owned = False
            self.owner = None
        if self.type == 'LAND':
            self.house_cost = info['HOUSE_COST']
            self.suit = info['SUIT']
            self.rents = info['RENTS']
        self.id = 0

class Monopoly:

    def __init__(self, board, player_count, watching):
        #making investors
        self.investors = [Investor(starting_funds=1500, name='Player_'+str(x)) for x in range(player_count)]
        #making monopoly board
        self.board = [Space(space_data) for space_data in board]
        for i in range(len(self.board)):
            self.board[i].id = i
        self.debtors = []#for bankrupt players
        self.bank = Investor(starting_funds=19080,name='Bank') #for mortgaged properties
        self.chance_discard = []
        self.chest_discard = []
        self.watching = watching
        self.turn_count = 1
        self.chance = chance
        self.chest = community_chest

    def turn_status(self):
        print('*'*15)
        print('Turn '+str(self.turn_count))
        for investor in self.investors:
            print(investor.name + ' has $' + str(investor.money) + '  and  ' + str(len(investor.assets)) + ' properties')
        print('*'*15)



    def take_turn(self, investor):
        if self.watching: feedback(investor, 'TURN_START')
        #print(investor.money)
        self.jail_check(investor)
        diceroll = self.roll_dice(investor)
        print(diceroll)
        #moving to new space
        if not investor.in_jail:
            newposition = (investor.position + diceroll) % 40
            self.move(investor, newposition)
            self.board_effect(investor, diceroll)
            player_survives = investor.money >= 0 or len(investor.assets) > 0
            if not player_survives:
                return False #bankrupt

        #self.free_action(investor)

        if investor.doubles_counter > 0:
            self.take_turn(investor)
        return True #player survives turn

    def free_action(self, investor):
        pass
        #where the player can buy houses, trade properties, unmortgage, etc.

    def jail_check(self, investor):
        if not investor.in_jail: return

        if investor.jail_cards > 0:
            investor.jail_cards -= 1
            investor.in_jail = False
        else:
            coinflip = random.random() > 0.5
            if coinflip and investor.money > 50:
                self.deduct(investor,50)
                investor.in_jail = False

    def roll_dice(self, investor):
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        if die1 != die2:
            investor.doubles_counter = 0
            if self.watching: feedback('DICE_STD', investor, str(die1+die2))
        else:
            investor.doubles_counter += 1
            if self.watching: feedback('DICE_DBL', investor, str(die1+die2))
            if investor.in_jail: #doubles gets you out of jail
                investor.in_jail = False
            if investor.doubles_counter == 3:
                self.move(investor,10) #3x doubles gets you into jail
                investor.doubles_counter = 0
                investor.in_jail = True
        return die1+die2

    def move(self,investor, target_location, pass_go=True):
        if self.watching: feedback('MOVEMENT', investor, self.board[target_location].name)
        if investor.position > target_location:
            if pass_go:
                investor.money += 200
        investor.position = target_location

    def board_effect(self, investor, diceroll=None, double_rent=False):
        land = self.board[investor.position]
        if land.type in ['GO', 'JAIL', 'FREE_PARKING']:
            pass
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
            self.land_actions(investor, land, diceroll, double_rent)

    def land_actions(self, investor, land, diceroll, double_rent=False):
        if not land.owned:
            if self.watching: feedback('UNOWNED_LAND',data=[land.name, str(land.price)])
            buy_cond = investor.money > land.price
            if buy_cond:
                self.buy(investor, land)
            else:
                self.auction(land)
            return True
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
                if double_rent:
                    rent *= 2

            elif land.type == 'UTILITY':
                if double_rent or self.board[12].owner == self.board[28].owner:#both utilities
                    rent = diceroll * 10
                else:
                    rent = diceroll * 7
            else: #standard property
                houses = land.owner.assets[land.id]['HOUSES']
                rent = land.rents[houses]

            #charge the rent
            landlord = self.board[investor.position].owner
            if self.watching: feedback('RENT',investor, [landlord.name, str(rent)])
            status = self.deduct(investor, rent, landlord)
            if not status:
                return False #investor got broke paying rent
        return True

    def deduct(self, investor, debt, landlord=None):
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
                        land_ID = random.choice(unmortgaged)
                        self.mortgage(investor, land_ID)
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
        return True

    def sell_house(self, investor, land_ID):
        if self.watching: feedback('SELL_HOUSE',investor, self.boards[land_ID].name)
        investor.assets[land_ID]['HOUSES'] -= 1
        investor.money += self.board[land_ID]['HOUSE_COST']/2

    def mortgage(self, investor, land_ID):
        if self.watching: feedback('MORTGAGE_PROPERTY', investor, self.boards[land_ID].name)
        investor.money += self.board[land_ID].price/2
        investor.asset[land_ID]['MORTGAGED'] = True

    def bank_auction(self):
        if self.watching: feedback('BANK_AUCTION')
        for a in self.bank.assets:
            self.auction(a)

    def buy(self, investor, land):
        if self.watching: feedback('BUY',investor, land.name)
        investor.money -= land.price
        newland = {'MORTGAGED':False, 'HOUSES':0}
        investor.assets[land.id] = newland
        land.owned = True
        land.owner = investor

    def auction(self, land, is_mortgaged=False):
        bid = 0
        while(True):#until property is sold
            print(bid)
            #if self.watching: feedback('AUCTION_ANNOUNCEMENT',str(bid))
            buyers = [x for x in self.investors if x.money > bid]
            if len(buyers) > 1:
                bidder = random.choice(buyers)
                #bid increases by no more than 50
                bid += random.randint(bid,min(bidder.money, bid+50))
            #1 out of 3 shot for now
            win_cond = 0.25 < random.random() or len(buyers) == 0
            if win_cond:
                if self.watching: feedback('AUCTION_BUY',bidder, [land.name, str(bid)])
                bidder.money -= bid
                newland = {'MORTGAGED':is_mortgaged, 'HOUSES':0}
                bidder.assets[land.id] = newland
                break

    def luxury_tax(self, investor):
        if self.watching: feedback('TAX',investor,'75')
        self.deduct(investor, 75)

    def income_tax(self, investor):
        if investor.money > 2000:
            tax = 200
        else:
            tax = investor.money//10
        self.deduct(investor,tax)
        feedback('TAX', investor, str(tax))


    def draw(self, investor, deck):
        if deck == 'CHANCE':
            if len(self.chance) == 0:
                self.chance, self.chance_discard = self.chance_discard, self.chance
                random.shuffle(self.chance)
            card = self.chance.pop()
            self.chance_discard.append(card)
        else:
            if len(self.chest) == 0:
                self.chest, self.chest_discard = self.chest_discard, self.chest
                random.shuffle(self.chest)
            card = self.chest.pop()
            self.chest_discard.append(card)

        if self.watching: feedback('DRAW_CARD', investor, card['TEXT'])

        if card['EFFECT'] == 'TRAVEL':
            self.move(investor,card['LOCATION'])
            self.board_effect(investor)
        elif card['EFFECT'] == 'RAIL':
            newposition = (investor.position//10 + 1)*10 + 5
            if newposition == 45: newposition = 5#catch the overflow
            self.move(investor, newposition)
            self.board_effect(investor, double_rent=True)
        elif card['EFFECT'] == 'UTIL':
            if 12 < investor.position < 28:
                self.move(investor, 28)#waterworkd
            else:
                self.move(investor, 12)#electric Company
            dice = random.randint(1,6)+random.randint(1,6)
            self.board_effect(investor, double_rent=True, diceroll=dice)
        elif card['EFFECT'] == 'PUSH':
            newposition = investor.position - 3
            if newposition < 0:
                newposition += 40
            self.move(investor, newposition)
            self.board_effect(investor)
        elif card['EFFECT'] == 'GET_OUT_OF_JAIL':
            if self.watching: feedback('GET_OUT_OF_JAIL', investor)
            investor.jail_cards += 1
        elif card['EFFECT'] == 'GO_TO_JAIL':
            self.move(investor,10,pass_go=False)
            investor.in_jail = True
        elif card['EFFECT'] == 'CHAIR':
            others = self.investors
            others.remove(investor)
            for player in others:
                self.deduct(investor,50,player)
        elif card['EFFECT'] == 'BIRTHDAY':
            others = self.investors
            print(others)
            others.remove(investor)
            for player in others:
                self.deduct(player,10,investor)
        elif card['EFFECT'] in ['REPAIR_1', 'REPAIR_2']:
            #25, 100
            has_houses = [x for x in investor.assets if investor.assets[x]['HOUSES'] > 0]
            if len(has_houses) > 0:
                hotels = 0
                houses = 0
                for house_quantity in has_houses:
                    if house_quantity == 5:
                        hotels += 1
                    else:
                        houses += house_quantity
                feedback('REPAIRS', investor, [houses,hotels])
                if card['EFFECT'] == 'REPAIR_1':
                    self.deduct(investor, hotels*100 + houses*25)
                else:
                    self.deduct(investor, hotels*115 + houses*40)
        elif card['EFFECT'] == 'GIFT':
            investor.money += card['AMOUNT']
        elif card['EFFECT'] == 'COST':
            self.deduct(investor, card['AMOUNT'])
