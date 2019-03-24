import interface as i


def init():
    # request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 10, 'type': 'ORDER_TYPE_BUY',
    #            'price': i.symbol_info(i.symbol(), 'SYMBOL_ASK')}
    # request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 1, 'type': 'ORDER_TYPE_SELL',
    #            'price': i.symbol_info(i.symbol(),'SYMBOL_BID')}
    # print(i.OrderSend(request))
    return 'INIT_SUCCESS'


def double_exponential_smoothing(size, alpha, beta):
    result = [i.iClose(i.symbol(), 'M15', size)]
    for n in range(1, size+1):
        if n == 1:
            level, trend = i.iClose(i.symbol(), 'M15', size), i.iClose(i.symbol(), 'M15', size-1) - i.iClose(i.symbol(), 'M15', size)
        if n >= size: # прогнозируем
            value = result[-1]
        else:
            value = i.iClose(i.symbol(), 'M15', size-n)
        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend
        result.append(level+trend)
    return result

def on_tick():
    if double_exponential_smoothing(10, 0.9, 0.2)[-1] > i.iOpen(i.symbol(), 'M15', 0):

        if i.t != -1:
            request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 10, 'type': 'ORDER_TYPE_SELL',
                       'price': i.symbol_info(i.symbol(),'SYMBOL_BID')}
            i.t = -1
            print(i.OrderSend(request))
            print('SELL')
    if double_exponential_smoothing(10, 0.9, 0.2)[-1] < i.iOpen(i.symbol(), 'M15', 0):
        if i.t != 1:
            request = {'action': 'TRADE_ACTION_DEAL', 'symbol': i.symbol(), 'volume': 10, 'type': 'ORDER_TYPE_BUY',
                       'price': i.symbol_info(i.symbol(),'SYMBOL_ASK')}
            i.t = 1
            print(i.OrderSend(request))
            print('BUY')
    print('BALANCE ', i.AccountInfo("ACCOUNT_BALANCE"))
