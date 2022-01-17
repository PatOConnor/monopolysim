'''
    The monopoly board is structured as a list of the data used to construct a
    list of Space objects
'''
standard_board = [
    {'NAME':'GO', 'TYPE':'GO'},
    {'NAME':'Mediterranean Avenue', 'TYPE':'LAND', 'SUIT':'BROWN', 'PRICE':60,
    'RENTS':[2,10,30,90,160,250], 'HOUSE_COST':50},
    {'NAME':'Community Chest', 'TYPE':'COMMUNITY_CHEST',},
    {'NAME':'Baltic Avenue', 'TYPE':'LAND', 'SUIT':'BROWN', 'PRICE':60,
    'RENTS':[4,20,60,180,320,450],, 'HOUSE_COST':50},
    {'NAME':'Income Tax', 'TYPE':'INCOME_TAX'},

    {'NAME':'Reading Railroad', 'TYPE':'RAILROAD', 'PRICE':200},
    {'NAME':'Oriental Avenue', 'TYPE':'LAND', 'SUIT':'LIGHT_BLUE', 'PRICE':100,
    'RENTS':[6,30,90,270,400,550], 'HOUSE_COST':50},
    {'NAME':'Chance', 'TYPE':'CHANCE'},
    {'NAME':'Vermont Avenue', 'TYPE':'LAND', 'SUIT':'LIGHT_BLUE', 'PRICE':100,
    'RENTS':[6,30,90,270,400,550], 'HOUSE_COST':50},
    {'NAME':'Connecticut Avenue', 'TYPE':'LAND', 'SUIT':'LIGHT_BLUE', 'PRICE':120,
    'RENTS':[8,40,100,300,450,600],  'HOUSE_COST':50},

    {'NAME':'Jail / Just Visiting', 'TYPE':'JAIL'},
    {'NAME':'St. Charles Place', 'TYPE':'LAND', 'SUIT':'PINK', 'PRICE':140,
    'RENTS':[10,50,150,450,625,750], 'HOUSE_COST':100},
    {'NAME':'Electric Company', 'TYPE':'UTILITY', 'PRICE':150},
    {'NAME':'States Avenue', 'TYPE':'LAND', 'SUIT':'PINK', 'PRICE':140,
    'RENTS':[10,50,150,450,625,750], 'HOUSE_COST':100},
    {'NAME':'Virginia Avenue', 'TYPE':'LAND', 'SUIT':'PINK', 'PRICE':160,
    'RENTS':[12,60,180,500,700,900], 'HOUSE_COST':100},

    {'NAME':'Pennsylvania Railroad', 'TYPE':'RAILROAD', 'PRICE':200},
    {'NAME':'St. James Place', 'TYPE':'LAND', 'SUIT':'ORANGE', 'PRICE':180,
    'RENTS':[14,70,200,550,750,950], 'HOUSE_COST':100},
    {'NAME':'Community Chest', 'TYPE':'COMMUNITY_CHEST'},
    {'NAME':'Tenessee Avenue', 'TYPE':'LAND', 'SUIT':'ORANGE', 'PRICE':180,
    'RENTS':[14,70,200,550,750,950], 'HOUSE_COST':100},
    {'NAME':'New York Avenue', 'TYPE':'LAND', 'SUIT':'ORANGE', 'PRICE':200,
    'RENTS':[16,80,220,600,800,1000], 'HOUSE_COST':100},

    {'NAME':'Free Parking', 'TYPE':'FREE_PARKING'},
    {'NAME':'Kentucky Avenue', 'TYPE':'LAND', 'SUIT':'RED', 'PRICE':220,
    'RENTS':[18,90,250,700,875,1050], 'HOUSE_COST':150},
    {'NAME':'Chance', 'TYPE':'CHANCE'},
    {'NAME':'Indiana Avenue', 'TYPE':'LAND', 'SUIT':'RED', 'PRICE':220,
    'RENTS':[18,90,250,700,875,1050], 'HOUSE_COST':150},
    {'NAME':'Illinois Avenue', 'TYPE':'LAND', 'SUIT':'RED', 'PRICE':240,
    'RENTS':[20,100,300,750,925,1100], 'HOUSE_COST':150},

    {'NAME':'B & O Railroad', 'TYPE':'RAILROAD', 'PRICE':200},
    {'NAME':'Atlantic Avenue', 'TYPE':'LAND', 'SUIT':'YELLOW', 'PRICE':260,
    'RENTS':[22,110,330,800,975,1150], 'HOUSE_COST':150},
    {'NAME':'Ventnor Avenue', 'TYPE':'LAND', 'SUIT':'YELLOW', 'PRICE':260,
    'RENTS':[22,110,330,800,975,1150], 'HOUSE_COST':150},
    {'NAME':'Water Works', 'TYPE':'UTILITY', 'PRICE':150},
    {'NAME':'Marvin Gardens', 'TYPE':'LAND', 'SUIT':'YELLOW', 'PRICE':280,
    'RENTS':[24,120,360,850,1025,1200], 'HOUSE_COST':150},

    {'NAME':'Go To Jail', 'TYPE':'GO_TO_JAIL'},
    {'NAME':'Pacific Avenue', 'TYPE':'LAND', 'SUIT':'GREEN', 'PRICE':300,
    'RENTS':[26,130,390,900,1100,1275], 'HOUSE_COST':200},
    {'NAME':'North Carolina Avenue', 'TYPE':'LAND', 'SUIT':'GREEN', 'PRICE':300,
    'RENTS':[26,130,390,900,1100,1275], 'HOUSE_COST':200},
    {'NAME':'Community Chest', 'TYPE':'COMMUNITY_CHEST'},
    {'NAME':'Pennsylvania Avenue', 'TYPE':'LAND', 'SUIT':'GREEN', 'PRICE':320,
    'RENTS':[28,150,450,1000,1200,1400], 'HOUSE_COST':200},

    {'NAME':'Short Line', 'TYPE':'RAILROAD', 'PRICE':200},
    {'NAME':'Chance', 'TYPE':'CHANCE'},
    {'NAME':'Park Place', 'TYPE':'LAND', 'SUIT':'BLUE', 'PRICE':350,
    'RENTS':[35,175,500,1100,1300,1500], 'HOUSE_COST':200},
    {'NAME':'LUXURY_TAX', 'TYPE':'LUXURY_TAX'},
    {'NAME':'Boardwalk', 'TYPE':'LAND', 'SUIT':'BLUE', 'PRICE':400,
    'RENTS':[50,200,600,1400,1700,2000], 'HOUSE_COST':200},
]
