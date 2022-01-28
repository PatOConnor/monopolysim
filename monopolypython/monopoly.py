from common.cards import chance, community_chest
from common.boards import std_board
from investor import Investor, Bank
from feedback import feedback

from numpy import random
from os import system

'''
    STATUS:
            The Game Logic is mostly complete as far as i can tell

            the bots won't buy houses or trade with each other, i need to fix
            that part of the logic

            at that point... what? Will that mean that I'm done? is that the
            point where i abstract to other boards? create a real AI?
'''

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
        if game.turn_count%10==1 and game.watching:
            system('cls')
    print(game.investors[0].name+' Wins with an account of $'+str(game.investors[0].money))

class Monopoly:
    def __init__(self, board, player_count, watching):
        #making investors
        self.investors = [Investor(starting_funds=1500, name='Player '+str(x)) for x in range(1,player_count+1)]
        self.bank = Bank(starting_funds=20580-len(self.investors)*1500)

        self.board = board
        self.watching = watching
        self.turn_count = 1

    def turn_status(self):
        print('\n'+'*'*15)
        print('Beginning of Turn '+str(self.turn_count))
        for investor in self.investors:
            print('\n'+investor.name + ' has $' + str(investor.money) + '  and these properties:')
            for asset in investor.assets:
                try:
                    print(asset.name[0:12:], '\t'+asset.suit, '\tmortgaged?'+str(asset.is_mortgaged),
                          '\t'+str(asset.houses)+' houses', 'hotel?'+str(asset.has_hotel))
                except AttributeError:
                    print(asset.name[0:12:], '\t\tmortgaged?'+str(asset.is_mortgaged))
        print('*'*15)
        input()

    '''Primary Methods for Game Processing'''
    def take_turn(self, investor):
        investor.sort_land()
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
        if self.bank.has_buildings():
            for land in unmortgaged_land[::-1]:
                if land.type in ('RAILROAD', 'UTILITY'):
                    continue #can't buy houses on these properties
                if investor.can_pay(land.house_cost):
                    print('BUYING HOUSE DEBUG: I AM HERE')
                    if land.houses == 4 and self.bank.has_hotels():
                        if self.watching:
                            feedback('BUILD_HOUSE',investor, land.name)
                        investor.build_hotel(land, bank)
                    elif self.bank.has_houses() and self.is_part_of_monopoly(land):
                        if self.watching:
                            feedback('BUILD_HOUSE',investor, land.name)
                        investor.build_house(land, self.bank)

        #TRADING
        needed_for_monopoly = self.needed_for_monopoly(investor)
        if needed_for_monopoly != None: #if the investor is close to a monopoly,
            for land in needed_for_monopoly[::-1]:
                if not land.is_owned:
                    continue #no one to trade with; check the others
                else:
                    good_trades = self.needed_for_monopoly(land.owner) #missing lands for other players
                    for otherland in good_trades[::-1]:
                        if otherland in investor.assets:
                            #both players achieve monopoly
                            investor.trade(land.owner,otherland, land)
                            break
        elif self.all_land_owned():
            #'hey, anyone want this?'
            print('ALL LAND OWNED DEBUG')
            land = random.choice(investor.assets)
            for player in self.investors:
                if player != investor and land not in self.needed_for_monopoly(player):
                    otherland = random.choice(player.assets)
                    if otherland not in self.needed_for_monopoly(investor):
                        investor.trade(player,land,otherland)

    def needed_for_monopoly(self, investor):
        if investor.assets == []:
            return
        suits_dict = {}
        near_suits = []
        needed_land = []
        for land in investor.assets:
            try:
                suits_dict[land.suit] += 1
            except KeyError:
                suits_dict[land.suit] = 1
#        print(suits_dict)
        for key in suits_dict:
            rail_cond = key=='RAILROAD' and suits_dict[key] == (2 or 3)
            util_cond = key=='UTILITY' and suits_dict[key] == 1
            land_cond = key!=('LAND' or 'UTILITY') and suits_dict[key] == 2
            if rail_cond or util_cond or land_cond:
                near_suits.append(key)
        for land in self.board:
            try:
                if land.suit in near_suits and land.owner != investor:
                    needed_land.append(land)
            except AttributeError:
                continue #this occurs when scanning a space with no suit
        print(needed_land)
        return needed_land


    def is_part_of_monopoly(self, land):
        board_index = self.board.index(land)
        spacerange = self.board[board_index-3:board_index+3]
        suit = land.suit
        for space in spacerange:
            try:
                if land.suit != space.suit:
                    return False
            except AttributeError:
                continue
        return False




    def all_land_owned(self):
        return True if sum([len(player.assets) for player in self.investors]) == 28 else False


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
