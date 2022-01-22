from common.cards import chance, community_chest
from common.boards import std_board
from investor import Investor, Bank
from feedback import feedback

from numpy import random
from os import system

def run(iswatching=True):
    game = Monopoly(board=std_board,
                    player_count=4,
                    watching=iswatching)
    if game.watching:
        feedback('GAME_START')
    while(game.no_monopoly_yet()):
        if game.watching:
            game.turn_status()
        for investor in game.investors:
            if not game.no_monopoly_yet():
                break#check every player move
            if game.watching:
                feedback('TURN_START', investor)
            game.take_turn(investor)
        game.turn_count += 1
        if game.turn_count%10==1:
            system('cls')
    print(game.investors[0].name+' Wins with an account of $'+str(game.investors[0].money))

class Monopoly:
    def __init__(self, board, player_count, watching):
        #making investors
        self.investors = [Investor(starting_funds=1500, name='Player '+str(x)) for x in range(1,player_count+1)]
        self.bank = Bank(starting_funds=20580-len(self.investors)*1500, name='Bank')

        self.board = board
        self.watching = watching
        self.turn_count = 1

    def turn_status(self):
        print('\n'+'*'*15)
        print('Beginning of Turn '+str(self.turn_count))
        for investor in self.investors:
            print(investor.name + ' has $' + str(investor.money) + '  and  ' + str(len(investor.assets)) + ' properties')
        print('*'*15)

    '''Primary Methods for Game Processing'''
    def take_turn(self, investor):
        if self.watching:
            feedback(investor, 'TURN_START')
        self.free_action(investor)
        self.jail_check(investor)
        diceroll = self.roll_dice(investor)
        if not investor.in_jail:
            newposition = (investor.position + diceroll) % 40
            self.move(investor, newposition)
            self.board_effect(investor, diceroll)
        self.free_action(investor)
        if investor.doubles_counter > 0:
            self.take_turn(investor)
        return

    def move(self, investor, newposition, pass_go=True):
        if self.watching:
            feedback('MOVEMENT', investor, self.board[newposition].name)
        if investor.position > newposition:
            if pass_go:
                investor.money += 200
        investor.position = newposition

    def board_effect(self, investor, diceroll=None, double_rent=False):
        land = self.board[investor.position]
        if land.type in ['GO', 'JAIL', 'FREE_PARKING']:
            pass
        elif land.type == 'COMMUNITY_CHEST':
            self.draw_card(investor, community_chest)
        elif land.type == 'CHANCE':
            self.draw_card(investor, chance)
        elif land.type == 'LUXURY_TAX':
            self.luxury_tax(investor)
        elif land.type == 'INCOME_TAX':
            self.income_tax(investor)
        elif land.type == 'GO_TO_JAIL':
            self.move(investor,10,pass_go=False)
            investor.in_jail = True
        elif land.type in ['LAND','RAILROAD','UTILITY']:
            self.land_actions(investor, land, diceroll, double_rent)

    def free_action(self, investor):
        #if you can afford to unmortgage your land, you do so
        mortgaged_land = investor.mortgaged_land()
        unmortgaged_land = investor.unmortgaged_land()
        if mortgaged_land != 0:
            #pick most expensive one
            for land in mortgaged_land:
                mortgage_price = land.price*11/20
                if investor.can_pay(mortgage_price):
                    investor.unmortgage(land)
                    break#one unmortgage per free_action()


        #if you can buy a house, you do so
        if bank.has_buildings():
            for land in unmortgaged_land[::-1]:
                if investor.can_pay(land.house_cost):
                    if land.houses == 4 and bank.has_hotels():
                        if self.watching:
                            feedback('BUILD_HOUSE',investor, land.name)
                        investor.build_hotel(land, bank)
                    elif bank.has_houses():
                        if self.watching:
                            feedback('BUILD_HOUSE',investor, land.name)
                        investor.build_house(land, bank)

        #TRADING
        needed = investor.needed_for_monopoly()
        if needed != []: #if the investor is close to a monopoly,
            for land in needed[::-1]:
                if not land.is_owned:
                    continue #no one to trade with; check the others
                else:
                    good_trades = land.owner.needed_for_monopoly() #missing lands for other players
                    for land_2 in good_trades[::-1]:
                        if land_2 in investor.assets:
                            investor.trade(land.owner,land,land_2) #both players achieve monopoly
                            break
        elif self.all_land_owned():
            land = random.choice(investor.assets)
            for player in self.investors:
                if player != investor and land not in player.needed_for_monopoly():
                    otherland = random.choice(player.assets)
                    if otherland not in investor.needed_for_monopoly():
                        investor.trade(player,land,otherland)



    def all_land_owned(self):
        return True if sum([len(player.assets) for player in self.investors]) is 28 else False


    '''Property Stuff'''

    def land_actions(self, investor, land, diceroll, double_rent=False):
        if not land.is_owned:
            if self.watching:
                feedback('UNOWNED_LAND',data=[land.name, str(land.price)])
            if investor.money > land.price:
                if self.watching:
                    feedback('BUY',investor, land.name)
                investor.buy(land)
            else:
                self.auction(land)
        else:
            if land.type == 'RAILROAD':
                rent = land.owner.railroad_rent()
            elif land.type == 'UTILITY':
                if double_rent or self.board[12].owner == self.board[28].owner:
                    rent = diceroll * 10
                else:
                    rent = diceroll * 7
            else: #standard property
                rent = land.rents[land.houses]
            #charge the rent
            landlord = self.board[investor.position].owner
            if self.watching:
                feedback('RENT',investor, [landlord.name, str(rent)])
            investor.pay_to(rent, landlord, self.bank)
        return

    def auction(self, land):
        bid = 0
        while(True):#until property is sold
            #if self.watching: feedback('AUCTION_ANNOUNCEMENT',str(bid))
            bidders = [x for x in self.investors if x.money > bid]
            if len(bidders) > 1:
                bidder = random.choice(bidders)
                #bid increases by no more than 50
                bid += random.randint(bid,min(bidder.money, bid+50))
            #1 out of 5 shot for now
            win_cond = 0.2 < random.random() or len(bidders) == 1
            if win_cond:
                if self.watching:
                    feedback('AUCTION_BUY', bidder, [land.name, str(bid)])
                bidder.pay_to(bid,self.bank)
                land.owner = bidder
                break

    def bank_auction(self):
        if self.watching:
            feedback('BANK_AUCTION')
        for land in self.bank.assets:
            self.auction(land)



    '''Other Tiles'''

    def luxury_tax(self, investor):
        if self.watching:
            feedback('TAX',investor,'75')
        investor.pay_to(75,self.bank)

    def income_tax(self, investor):
        if investor.money > 2000:
            tax = 200
        else:
            tax = investor.money//10
        if self.watching:
            feedback('TAX', investor, str(tax))
        investor.pay_to(tax,self.bank)

    def draw_card(self, investor, deck):
        if deck.needs_to_shuffle():
            deck.shuffle_deck()
        card = deck.draw()
        if self.watching:
            feedback('DRAW_CARD', investor, card.text)
        self.card_effect(investor,card)

    def card_effect(self,investor,card):
        if card.effect == 'TRAVEL':
            self.move(investor, card.amount)
            self.board_effect(investor, diceroll=None)

        elif card.effect == 'RAIL':
            newposition = (investor.position//10 + 1)*10 + 5
            if newposition == 45: newposition = 5#catch the overflow
            self.move(investor, newposition)
            self.board_effect(investor, double_rent=True)

        elif card.effect =='UTIL':
            if 12 < investor.position < 28:
                self.move(investor, 28)#waterworkd
            else:
                self.move(investor, 12)#electric Company
            dice = random.randint(1,6)+random.randint(1,6)
            self.board_effect(investor, double_rent=True, diceroll=dice)

        elif card.effect == 'PUSH':
            newposition = investor.position - 3
            if newposition < 0:
                newposition += 40
            self.move(investor, newposition)
            self.board_effect(investor)

        elif card.effect == 'GET_OUT_OF_JAIL':
            if self.watching:
                feedback('GET_OUT_OF_JAIL', investor)
            investor.jail_cards += 1
            card.in_inventory = True

        elif card.effect == 'GO_TO_JAIL':
            self.move(investor,10,pass_go=False)
            investor.in_jail = True

        elif card.effect == 'GIFT':
            investor.money += card.amount

        elif card.effect == 'COST':
            investor.pay_to(card.amount, self.bank)

        elif card.effect == 'CHAIR':
            for player in self.investors:
                if player != investor:
                    player.pay_to(50,investor)

        elif card.effect == 'BIRTHDAY':
            for player in investors:
                if player != investor:
                    player.pay_to(10,investor)

        elif card.effect == 'REPAIR_1':
            houses = investor.count_houses()
            hotels = investor.count_hotels()
            if self.watching:
                feedback('REPAIRS', investor, [houses,hotels])
            investor.pay_to(hotels*100+houses*25,self.bank)

        elif card.effect == 'REPAIR_2':
            houses = investor.count_houses()
            hotels = investor.count_hotels()
            if self.watching:
                feedback('REPAIRS', investor, [houses,hotels])
            investor.pay_to(hotels*115+houses*40,self.bank)




    '''Helper Methods'''
    def no_monopoly_yet(self):
        found_player = False
        for investor in self.investors:
            if investor.is_bankrupt == False:
                if not found_player:
                    found_player = True
                else:
                    return True
        return False

    def jail_check(self, investor):
        if not investor.in_jail: return
        if investor.jail_cards > 0:
            investor.jail_cards -= 1
            investor.in_jail = False
        else:
            coinflip = random.random() > 0.5
            if coinflip and investor.money > 50:
                investor.pay_to(50,self.bank)
                investor.in_jail = False

    def roll_dice(self, investor):
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        if die1 != die2:
            investor.doubles_counter = 0
            if self.watching:
                feedback('DICE_STD', investor, str(die1+die2))
        else:
            investor.doubles_counter += 1
            if self.watching:
                feedback('DICE_DBL', investor, str(die1+die2))
            if investor.in_jail: #doubles gets you out of jail
                investor.in_jail = False
            if investor.doubles_counter == 3:
                self.move(investor,10) #3x doubles gets you into jail
                investor.doubles_counter = 0
                investor.in_jail = True
        return die1+die2
