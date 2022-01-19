'''
dictionaries of chance and community chest cards

keys are integer IDs, and the value is itself a dictionary with string keys

    'TEXT', 'EFFECT'
'''
chance = [
        {'TEXT':'Advance to GO', 'EFFECT':'TRAVEL', 'LOCATION':0,},
        {'TEXT':'Advance to Boardwalk', 'EFFECT':'TRAVEL', 'LOCATION':39,},
        {'TEXT':'Advance to Illinois Avenue', 'EFFECT':'TRAVEL', 'LOCATION':0,},
        {'TEXT':'Advance to St Charles Place', 'EFFECT':'TRAVEL', 'LOCATION':0,},
        {'TEXT':'Advance to Reading Railroad', 'EFFECT':'TRAVEL', 'LOCATION':0,},

        {'TEXT':'Advance to nearest Railroad', 'EFFECT':'RAIL'},
        {'TEXT':'Advance to nearest Railroad', 'EFFECT':'RAIL'},
        {'TEXT':'Advance to nearest Utility', 'EFFECT':'UTIL'},

        {'TEXT':'Go Back Three Spaces', 'EFFECT':'PUSH', 'DISTANCE':-3},
        {'TEXT':'Get Out Of Jail Free', 'EFFECT':'GET_OUT_OF_JAIL',},
        {'TEXT':'Go Directly To Jail', 'EFFECT':'GO_TO_JAIL',},
        {'TEXT':'You Have Been Elected Chairman of the Board: Pay $50 Each', 'EFFECT':'CHAIR'},
        {'TEXT':'Make General Repairs on All Property', 'EFFECT':'REPAIR_1'},

        {'TEXT':'Bank Pays You $50 Dividend', 'EFFECT':'GIFT', 'AMOUNT':50},
        {'TEXT':'Building Loan Matures: $150', 'EFFECT':'GIFT', 'AMOUNT':150},
        {'TEXT':'Speeding Fine: $15', 'EFFECT':'COST', 'AMOUNT':15},
        ]

community_chest = [
        {'TEXT':'Advance to GO', 'EFFECT':'TRAVEL', 'LOCATION':0,},
        {'TEXT':'Get Out Of Jail Free', 'EFFECT':'GET_OUT_OF_JAIL',},
        {'TEXT':'Go Directly To Jail', 'EFFECT':'GO_TO_JAIL',},

        {'TEXT':'Bank Error In Your Favor', 'EFFECT':'GIFT', 'AMOUNT':200},
        {'TEXT':'Sale of Stock gets you $50', 'EFFECT':'GIFT', 'AMOUNT':50},
        {'TEXT':'Holiday Fund Matures: $100', 'EFFECT':'GIFT', 'AMOUNT':100},
        {'TEXT':'Life Insurance Matures: $100', 'EFFECT':'GIFT', 'AMOUNT':100},
        {'TEXT':'Income Tax Refund', 'EFFECT':'GIFT', 'AMOUNT':20},
        {'TEXT':'Recieve $25 Consultancy Fee', 'EFFECT':'GIFT', 'AMOUNT':25},
        {'TEXT':'You Win Second Prize in a Beauty Contest!', 'EFFECT':'GIFT', 'AMOUNT':10},
        {'TEXT':'Inherit $100', 'EFFECT':'GIFT', 'AMOUNT':100},

        {'TEXT':'Its Your Birthday! Collect $10 from each player', 'EFFECT':'BIRTHDAY'},
        {'TEXT':'Assessed for Street Repair', 'EFFECT':'REPAIR_2'},

        {'TEXT':'Doctors Fee: $50', 'EFFECT':'COST', 'AMOUNT':50},
        {'TEXT':'Hospital Fee: $100', 'EFFECT':'COST', 'AMOUNT':100},
        {'TEXT':'School Fee: $50', 'EFFECT':'COST', 'AMOUNT':50},
]
