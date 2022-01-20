from numpy import random
'''
dictionaries of chance and community chest cards

keys are integer IDs, and the value is itself a dictionary with string keys

    'text', 'effect'
'''
deckdata_chance = [
        {'text':'Advance to GO', 'effect':'TRAVEL', 'location':0,},
        {'text':'Advance to Boardwalk', 'effect':'TRAVEL', 'location':39,},
        {'text':'Advance to Illinois Avenue', 'effect':'TRAVEL', 'location':0,},
        {'text':'Advance to St Charles Place', 'effect':'TRAVEL', 'location':0,},
        {'text':'Advance to Reading Railroad', 'effect':'TRAVEL', 'location':0,},

        {'text':'Advance to nearest Railroad', 'effect':'RAIL'},
        {'text':'Advance to nearest Railroad', 'effect':'RAIL'},
        {'text':'Advance to nearest Utility', 'effect':'UTIL'},

        {'text':'Go Back Three Spaces', 'effect':'PUSH', 'distance':-3},
        {'text':'Get Out Of Jail Free', 'effect':'GET_OUT_OF_JAIL',},
        {'text':'Go Directly To Jail', 'effect':'GO_TO_JAIL',},
        #{'text':'You Have Been Elected Chairman of the Board: Pay $50 Each', 'effect':'CHAIR'},
        #{'text':'Make General Repairs on All Property', 'effect':'REPAIR_1'},

        {'text':'Bank Pays You $50 Dividend', 'effect':'GIFT', 'amount':50},
        {'text':'Building Loan Matures: $150', 'effect':'GIFT', 'amount':150},
        {'text':'Speeding Fine: $15', 'effect':'COST', 'amount':10000},
        ]

deckdata_community_chest = [
        {'text':'Advance to GO', 'effect':'TRAVEL', 'location':0,},
        {'text':'Get Out Of Jail Free', 'effect':'GET_OUT_OF_JAIL',},
        {'text':'Go Directly To Jail', 'effect':'GO_TO_JAIL',},

        {'text':'Bank Error In Your Favor', 'effect':'GIFT', 'amount':200},
        {'text':'Sale of Stock gets you $50', 'effect':'GIFT', 'amount':50},
        {'text':'Holiday Fund Matures: $100', 'effect':'GIFT', 'amount':100},
        {'text':'Life Insurance Matures: $100', 'effect':'GIFT', 'amount':100},
        {'text':'Income Tax Refund', 'effect':'GIFT', 'amount':20},
        {'text':'Recieve $25 Consultancy Fee', 'effect':'GIFT', 'amount':25},
        {'text':'You Win Second Prize in a Beauty Contest!', 'effect':'GIFT', 'amount':10},
        {'text':'Inherit $100', 'effect':'GIFT', 'amount':100},

        #{'text':'Its Your Birthday! Collect $10 from each player', 'effect':'BIRTHDAY'},
        #{'text':'Assessed for Street Repair', 'effect':'REPAIR_2'},

        {'text':'Doctors Fee: $50', 'effect':'COST', 'amount':50},
        {'text':'Hospital Fee: $100', 'effect':'COST', 'amount':100},
        {'text':'School Fee: $50', 'effect':'COST', 'amount':50},
]

class Card:
    def __init__(self, data):
        #convert to a class instead of a dictionary lookup
        for (key,val) in data:
            self.key = val
        self.flipped = False
        self.in_inventory = False

class Deck:
    def __init__(self, cards_list):
        self.cards = [Card(x) for x in cards_list]

    def needs_to_shuffle(self):
        for c in self.cards:
            if not c.flipped:
                return False
        return True

    def shuffle_deck(self):
        for c in self.cards:
            if not c.in_inventory:
                c.flipped = False
        random.shuffle(self.cards)
        return

    def draw(self):
        for card in deck:
            if not card.flipped:
                card.flipped = True
                return card


chance = [Deck(x) for x in deckdata_chance]
community_chest = [Deck(x) for x in deckdata_community_chest]
