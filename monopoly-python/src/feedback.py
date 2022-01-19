def feedback(msg_type, investor=None, data=None):

    if type == 'GAME_START':
        print('Welcome To Monopoly Simulator!')
    elif type=='TURN_START':
        print(investor.name+' begins their turn!')
    elif type=='PLAYER_BANKRUPT':
        print(investor.name+' has gone bankrupt and has left the game!')
    elif type=='JAIL':
        print(investor.name+' is in jail.')
    elif type=='GET_OUT_OF_JAIL':
        print(investor.name+' recieves a Get Out Of Jail Free Card!')
    elif type=='DICE_STD':
        print(investor.name+' rolled a '+data'.')
    elif type=='DICE_DBL':
        print(investor.name+' rolled a '+data'. Doubles!')

    elif type=='MOVEMENT':
        print(investor.name+' proceeds to '+data+'.')

    elif type=='UNOWNED_LAND':
        print(data[0]+' is for sale at $'+data[1])
    elif type=='BUY':
        print(investor.name+' buys '+data)
    elif type=='RENT':
        print(investor.name+' owes '+data[0]+' $'+data[1]+' in rent.')

    elif type=='INSUFFICIENT':
        print(investor.name+' has insufficient funds for this transaction.')
    elif type=='SELL_HOUSE':
        print(investor.name+' sells house located at '+data)
    elif type=='MORTGAGE_PROPERTY':
        print(investor.name+' mortgages property '+data)


    elif type=='BANK_AUCTION':
        print('The players assets will now be auctioned by the bank.')

    elif type=='AUCTION_ANNOUNCEMENT':
        print('The Current Bid is '+data)

    elif type=='AUCTION_BUY':
        print(investor.name+' buys '+data[0]+' for the price of '+data[1]+'')

    elif type=='TAX':
        print(investor.name+'pays an tax of '+data)

    elif type=='DRAW_CARD':
        print(investor.name+' draws: '+data+'!')


    elif type=='REPAIRS':
        print(investor.name+' has '+data[0]+' houses and '+data[1]+' hotels.')
