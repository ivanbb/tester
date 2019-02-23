import interface as i

def init():

    return 'INIT_SUCCESS'


def on_tick():
    price = i.iOpen(i.symbol(), 'M15', 0)
    print(price)
    request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 10, 'type': 'ORDER_TYPE_BUY',
               'price': i.symbol_info(i.symbol(),'SYMBOL_ASK')}
    print(i.OrderSend(request))
    request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 10, 'type': 'ORDER_TYPE_SELL',
               'price': i.symbol_info(i.symbol(),'SYMBOL_BID')}
    print(i.OrderSend(request))

