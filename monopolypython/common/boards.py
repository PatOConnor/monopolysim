class Space:
    def __init__(self, info):
        self.id = info['ID']
        self.name = info['NAME']
        self.type = info['TYPE']
        if self.type in  ['LAND', 'UTILITY', 'RAILROAD']:
            self.price = info['PRICE']
            self.suit = info['SUIT']
            self.is_owned = False
            self.owner = None
            self.is_mortgaged = False
        if self.type == 'LAND':
            self.house_cost = info['HOUSE_COST']
            self.rents = info['RENTS']
            self.houses = 0
            self.has_hotel = False

    def __repr__(self):
        return self.name


'''
    The monopoly board is structured as a list of the data used to construct a
    list of Space objects
'''
std_board_data = [
    {'ID':0, 'NAME':'GO', 'TYPE':'GO'},
    {'ID':1, 'NAME':'Mediterranean Avenue', 'TYPE':'LAND', 'SUIT':'BROWN', 'PRICE':60,
    'RENTS':[2,10,30,90,160,250], 'HOUSE_COST':50},
    {'ID':2, 'NAME':'Community Chest', 'TYPE':'COMMUNITY_CHEST',},
    {'ID':3, 'NAME':'Baltic Avenue', 'TYPE':'LAND', 'SUIT':'BROWN', 'PRICE':60,
    'RENTS':[4,20,60,180,320,450], 'HOUSE_COST':50},
    {'ID':4, 'NAME':'Income Tax', 'TYPE':'INCOME_TAX'},

    {'ID':5, 'NAME':'Reading Railroad', 'TYPE':'RAILROAD', 'SUIT':'RAILROAD', 'PRICE':200},
    {'ID':6, 'NAME':'Oriental Avenue', 'TYPE':'LAND', 'SUIT':'LIGHT_BLUE', 'PRICE':100,
    'RENTS':[6,30,90,270,400,550], 'HOUSE_COST':50},
    {'ID':7, 'NAME':'Chance', 'TYPE':'CHANCE'},
    {'ID':8, 'NAME':'Vermont Avenue', 'TYPE':'LAND', 'SUIT':'LIGHT_BLUE', 'PRICE':100,
    'RENTS':[6,30,90,270,400,550], 'HOUSE_COST':50},
    {'ID':9, 'NAME':'Connecticut Avenue', 'TYPE':'LAND', 'SUIT':'LIGHT_BLUE', 'PRICE':120,
    'RENTS':[8,40,100,300,450,600],  'HOUSE_COST':50},

    {'ID':10, 'NAME':'Jail / Just Visiting', 'TYPE':'JAIL'},
    {'ID':11, 'NAME':'St. Charles Place', 'TYPE':'LAND', 'SUIT':'PINK', 'PRICE':140,
    'RENTS':[10,50,150,450,625,750], 'HOUSE_COST':100},
    {'ID':12, 'NAME':'Electric Company', 'TYPE':'UTILITY', 'SUIT':'UTILITY', 'PRICE':150},
    {'ID':13, 'NAME':'States Avenue', 'TYPE':'LAND', 'SUIT':'PINK', 'PRICE':140,
    'RENTS':[10,50,150,450,625,750], 'HOUSE_COST':100},
    {'ID':14, 'NAME':'Virginia Avenue', 'TYPE':'LAND', 'SUIT':'PINK', 'PRICE':160,
    'RENTS':[12,60,180,500,700,900], 'HOUSE_COST':100},

    {'ID':15, 'NAME':'Pennsylvania Railroad', 'TYPE':'RAILROAD', 'SUIT':'RAILROAD', 'PRICE':200},
    {'ID':16, 'NAME':'St. James Place', 'TYPE':'LAND', 'SUIT':'ORANGE', 'PRICE':180,
    'RENTS':[14,70,200,550,750,950], 'HOUSE_COST':100},
    {'ID':17, 'NAME':'Community Chest', 'TYPE':'COMMUNITY_CHEST'},
    {'ID':18, 'NAME':'Tenessee Avenue', 'TYPE':'LAND', 'SUIT':'ORANGE', 'PRICE':180,
    'RENTS':[14,70,200,550,750,950], 'HOUSE_COST':100},
    {'ID':19, 'NAME':'New York Avenue', 'TYPE':'LAND', 'SUIT':'ORANGE', 'PRICE':200,
    'RENTS':[16,80,220,600,800,1000], 'HOUSE_COST':100},

    {'ID':20, 'NAME':'Free Parking', 'TYPE':'FREE_PARKING'},
    {'ID':21, 'NAME':'Kentucky Avenue', 'TYPE':'LAND', 'SUIT':'RED', 'PRICE':220,
    'RENTS':[18,90,250,700,875,1050], 'HOUSE_COST':150},
    {'ID':22, 'NAME':'Chance', 'TYPE':'CHANCE'},
    {'ID':23, 'NAME':'Indiana Avenue', 'TYPE':'LAND', 'SUIT':'RED', 'PRICE':220,
    'RENTS':[18,90,250,700,875,1050], 'HOUSE_COST':150},
    {'ID':24, 'NAME':'Illinois Avenue', 'TYPE':'LAND', 'SUIT':'RED', 'PRICE':240,
    'RENTS':[20,100,300,750,925,1100], 'HOUSE_COST':150},

    {'ID':25, 'NAME':'B & O Railroad', 'TYPE':'RAILROAD', 'SUIT':'RAILROAD', 'PRICE':200},
    {'ID':26, 'NAME':'Atlantic Avenue', 'TYPE':'LAND', 'SUIT':'YELLOW', 'PRICE':260,
    'RENTS':[22,110,330,800,975,1150], 'HOUSE_COST':150},
    {'ID':27, 'NAME':'Ventnor Avenue', 'TYPE':'LAND', 'SUIT':'YELLOW', 'PRICE':260,
    'RENTS':[22,110,330,800,975,1150], 'HOUSE_COST':150},
    {'ID':28, 'NAME':'Water Works', 'TYPE':'UTILITY', 'SUIT':'UTILITY',  'PRICE':150},
    {'ID':29, 'NAME':'Marvin Gardens', 'TYPE':'LAND', 'SUIT':'YELLOW', 'PRICE':280,
    'RENTS':[24,120,360,850,1025,1200], 'HOUSE_COST':150},

    {'ID':30, 'NAME':'Go To Jail', 'TYPE':'GO_TO_JAIL'},
    {'ID':31, 'NAME':'Pacific Avenue', 'TYPE':'LAND', 'SUIT':'GREEN', 'PRICE':300,
    'RENTS':[26,130,390,900,1100,1275], 'HOUSE_COST':200},
    {'ID':32, 'NAME':'North Carolina Avenue', 'TYPE':'LAND', 'SUIT':'GREEN', 'PRICE':300,
    'RENTS':[26,130,390,900,1100,1275], 'HOUSE_COST':200},
    {'ID':33, 'NAME':'Community Chest', 'TYPE':'COMMUNITY_CHEST'},
    {'ID':34, 'NAME':'Pennsylvania Avenue', 'TYPE':'LAND', 'SUIT':'GREEN', 'PRICE':320,
    'RENTS':[28,150,450,1000,1200,1400], 'HOUSE_COST':200},

    {'ID':35, 'NAME':'Short Line', 'TYPE':'RAILROAD', 'SUIT':'RAILROAD', 'PRICE':200},
    {'ID':36, 'NAME':'Chance', 'TYPE':'CHANCE'},
    {'ID':37, 'NAME':'Park Place', 'TYPE':'LAND', 'SUIT':'BLUE', 'PRICE':350,
    'RENTS':[35,175,500,1100,1300,1500], 'HOUSE_COST':200},
    {'ID':38, 'NAME':'LUXURY_TAX', 'TYPE':'LUXURY_TAX'},
    {'ID':39, 'NAME':'Boardwalk', 'TYPE':'LAND', 'SUIT':'BLUE', 'PRICE':400,
    'RENTS':[50,200,600,1400,1700,2000], 'HOUSE_COST':200},
]
std_board = [Space(data) for data in std_board_data]
