def feedback(msg_type, investor=None, data=None):
    if msg_type == 'GAME_START':
        print('\n\n\n')
        print('*'*30)
        print('*'*30)
        print('Welcome To Monopoly Simulator!')
    elif msg_type=='TURN_START':
        print('\n')
        print(investor.name+' begins their turn!')
    elif msg_type=='PLAYER_BANKRUPT':
        print(investor.name+' has gone bankrupt and has left the game!')
    elif msg_type=='JAIL':
        print(investor.name+' is in jail.')
    elif msg_type=='GET_OUT_OF_JAIL':
        print(investor.name+' recieves a Get Out Of Jail Free Card!')
    elif msg_type=='DICE_STD':
        print(investor.name+' rolled a '+data+'.')
    elif msg_type=='DICE_DBL':
        print(investor.name+' rolled a '+data+'. Doubles!')

    elif msg_type=='MOVEMENT':
        print(investor.name+' proceeds to '+data+'.')

    elif msg_type=='UNOWNED_LAND':
        print(data[0]+' is for sale at $'+data[1])
    elif msg_type=='BUY':
        print(investor.name+' buys '+data)
    elif msg_type=='RENT':
        print(investor.name+' owes '+data[0]+' $'+data[1]+' in rent.')

    elif msg_type=='INSUFFICIENT':
        print(investor.name+' has insufficient funds for this transaction.')
    elif msg_type=='SELL_HOUSE':
        print(investor.name+' sells house located at '+data)
    elif msg_type=='MORTGAGE_PROPERTY':
        print(investor.name+' mortgages property '+data)


    elif msg_type=='BANK_AUCTION':
        print('The players assets will now be auctioned by the bank.')

    elif msg_type=='AUCTION_ANNOUNCEMENT':
        print('The Current Bid is '+data)

    elif msg_type=='AUCTION_BUY':
        print(investor.name+' buys '+data[0]+' for the price of '+data[1]+'')

    elif msg_type=='TAX':
        print(investor.name+'pays an tax of '+data)

    elif msg_type=='DRAW_CARD':
        print(investor.name+' draws: '+data+'!')


    elif msg_type=='REPAIRS':
        print(investor.name+' has '+data[0]+' houses and '+data[1]+' hotels.')
