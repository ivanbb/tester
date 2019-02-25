import objects
from datetime import datetime


def symbol():
    return objects.symbols_list[0][0]


def symbol_info(name, prop):
    return objects.symbols[name].symbol_info(prop)


def iOpen(symb, time_frame, shift):
    """Define iOpen function from Metatrader"""
    if time_frame == 'NULL':
        time_frame = objects.time_frame
    rates = {'M1': 1, 'M5': 5, 'M15': 15, 'M30': 30, 'H1': 60, 'H4': 240, 'D1': 1440, 'W1': 10080,
             'm1': 43800}  # minutes in period
    timestamp = int(objects.datetime/rates[time_frame])*rates[time_frame]  # round off time to multiple timeframe
    timestamp -= shift*rates[time_frame]*60
    date = datetime.fromtimestamp(timestamp).strftime(objects.DATE_FORMAT)  # get date from timestamp
    time = datetime.fromtimestamp(timestamp).strftime(objects.TIME_FORMAT)  # get time from timestamp
    return objects.candles[symb].i_open(time_frame, date, time)


def OrderSend(trade_request):
    trade_result = {}
    if trade_request['action'] == 'TRADE_ACTION_DEAL':
        ticket = objects.market.order_place(trade_request['symbol'], trade_request['volume'], trade_request['type'], trade_request['price'])
        trade_result = {'retcode': 0, 'ticket': ticket}
    return trade_result




