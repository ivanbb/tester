from account import Account
from currency import Symbol
from datetime import datetime
from objects import DATE_FORMAT, TIME_FORMAT
from market import Market, SymbolPrices
import bot as bot
import objects
import matplotlib.pyplot as plt
from dbconnect import insert_balance, query_with_fetchall
import sys


def init(args):
    objects.start = int(args[1])
    objects.end = int(args[2])
    objects.time_frame = args[3]
    objects.balance = int(args[4])
    objects.leverage = int(args[5])
    symbols = query_with_fetchall(args[6])

    for symb in symbols:
        objects.symbols_list.append(list(symb))

    print("Start time: {0}, End time: {1}, time_frame: {2}, balance: {3}, leverage: {4}, symbol: {5}"
          " \n testing started".format(
                                objects.start,
                                objects.end,
                                objects.time_frame,
                                objects.balance,
                                objects.leverage,
                                objects.symbols_list[0][0])
          )


def run():
    """Running market"""
    bal = []
    for __time in range(objects.start, objects.end, 60):
        objects.market.datetime = __time
        objects.datetime = __time
        objects.market.set_price()

        insert_balance(__time, objects.market.account.account_info('ACCOUNT_BALANCE'),
                       objects.market.account.account_info('ACCOUNT_EQUITY'))  # add balance to database
        bal.append([objects.market.account.account_info('ACCOUNT_BALANCE'),
                    objects.market.account.account_info('ACCOUNT_EQUITY')])

        bot.on_tick()
        objects.market.account.calc()
        objects.market.open_position()

    plt.plot(bal)
    plt.show()


if __name__ == '__main__':
    """Tester starting from command line with parameters start datetime, 
    end datetime, time frame, initial balance, leverage, symbol"""
    # init(sys.argv)  # initialise tester

    account = Account(objects.balance, objects.currency, objects.leverage)  # создаем аккаунт
    for sym in objects.symbols_list:
        objects.symbols[sym[0]] = Symbol(sym[0], sym[1], sym[2], sym[3],
                                         sym[4], sym[5], sym[6], sym[7])  # создаем символы
        objects.candles[sym[0]] = SymbolPrices(sym[0])  # создаем символы
    objects.market = Market(objects.start, account, objects.symbols, objects.candles)
    objects.market.set_price()
    bot.init()
    run()



