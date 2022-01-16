'''
    The monopoly board is structured as a list of the data used to construct a
    list of Space objects
'''
standard_board = [
    {'NAME':'START', 'TYPE':'START', 'SUIT':None, 'PRICE':0},
    {'NAME':'Mediterranean Avenue', 'TYPE':'PROPERTY', 'SUIT':'BROWN'},
    {'NAME':'Baltic Avenue00', 'TYPE':'PROPERTY', 'SUIT':'BROWN'},
    {'NAME':'Income Tax', 'TYPE':'INCOME_TAX', 'SUIT':None, 'PRICE':None},
    {'NAME':'Oriental Avenue', 'TYPE':'PROPERTY', 'SUIT':'LIGHT_BLUE'}
    {'NAME':'Vermont Avenue', 'TYPE':'PROPERTY', 'SUIT':'LIGHT_BLUE'}
    {'NAME':'Connecticut Avenue', 'TYPE':'PROPERTY', 'SUIT':'LIGHT_BLUE'}

    {'NAME':'St. Charles Place', 'TYPE':'PROPERTY', 'SUIT':'PINK'}
    {'NAME':'States Avenue', 'TYPE':'PROPERTY', 'SUIT':'PINK'}
    {'NAME':'Virginia Avenue', 'TYPE':'PROPERTY', 'SUIT':'PINK'}

    {'NAME':'St. James Place', 'TYPE':'PROPERTY', 'SUIT':'ORANGE'}
    {'NAME':'Tenessee Avenue', 'TYPE':'PROPERTY', 'SUIT':'ORANGE'}
    {'NAME':'New York Avenue', 'TYPE':'PROPERTY', 'SUIT':'ORANGE'}

    {'NAME':'Kentucky Avenue', 'TYPE':'PROPERTY', 'SUIT':'RED'}
    {'NAME':'Indiana Avenue', 'TYPE':'PROPERTY', 'SUIT':'RED'}
    {'NAME':'Illinois Avenue', 'TYPE':'PROPERTY', 'SUIT':'RED'}

    {'NAME':'Atlantic Avenue', 'TYPE':'PROPERTY', 'SUIT':'YELLOW'}
    {'NAME':'Ventnor Avenue', 'TYPE':'PROPERTY', 'SUIT':'YELLOW'}
    {'NAME':'Marvin Gardens', 'TYPE':'PROPERTY', 'SUIT':'YELLOW'}

    {'NAME':'Pacific Avenue', 'TYPE':'PROPERTY', 'SUIT':'GREEN'}
    {'NAME':'North Carolina Avenue', 'TYPE':'PROPERTY', 'SUIT':'GREEN'}
    {'NAME':'Pennsylvania Avenue', 'TYPE':'PROPERTY', 'SUIT':'GREEN'}

    {'NAME':'Park Place', 'TYPE':'PROPERTY', 'SUIT':'BLUE', 'PRICE':350}
    {'NAME':'Boardwalk', 'TYPE':'PROPERTY', 'SUIT':'BLUE', 'PRICE':400}


]
