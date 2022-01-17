'''
dictionaries of chance and community chest cards

keys are integer IDs, and the value is itself a dictionary with string keys

    'TEXT', 'EFFECT'
'''
chance = [
        {'TEXT':'Get Out Of Jail Free', 'EFFECT':'GET_OUT_OF_JAIL',},
        {'TEXT':'Walk On The Boardwalk', 'EFFECT':'TRAVEL', 'LOCATION':39,},
        {'TEXT':'Clerical Error! Get $100', 'EFFECT':'GIFT', 'AMOUNT':100},
        {'TEXT':'Sudden Repair Bill! Pay $75', 'EFFECT':'COST', 'AMOUNT':},
]

community_chest = {
            0:{'TEXT':'Test', 'EFFECT':'Test'}
}
