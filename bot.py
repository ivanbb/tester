import interface as i


def init():
    # request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 10, 'type': 'ORDER_TYPE_BUY',
    #            'price': i.symbol_info(i.symbol(), 'SYMBOL_ASK')}
    # request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 1, 'type': 'ORDER_TYPE_SELL',
    #            'price': i.symbol_info(i.symbol(),'SYMBOL_BID')}
    # print(i.OrderSend(request))
    return 'INIT_SUCCESS'


def on_tick():
    if i.iClose(i.symbol(), 'M15', 2) > i.iOpen(i.symbol(), 'M15', 0):

        if i.t != -1:
            request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 10, 'type': 'ORDER_TYPE_SELL',
                       'price': i.symbol_info(i.symbol(),'SYMBOL_BID')}
            i.t = -1
            print(i.OrderSend(request))
            print('SELL')
    if i.iClose(i.symbol(), 'M15', 2) < i.iOpen(i.symbol(), 'M15', 0):
        if i.t != 1:
            request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 10, 'type': 'ORDER_TYPE_BUY',
                       'price': i.symbol_info(i.symbol(),'SYMBOL_ASK')}
            i.t = 1
            print(i.OrderSend(request))
            print('BUY')
    print('BALANCE ', i.AccountInfo("ACCOUNT_BALANCE"))
