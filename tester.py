from account import Account
from currency import Symbol
from datetime import datetime
from objects import DATE_FORMAT, TIME_FORMAT
from market import Market, SymbolPrices
import bot as bot
import objects
import matplotlib.pyplot as plt
from dbconnect import insert_balance
import sys


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
    for param in sys.argv:
        print(param)

    account = Account(objects.balance, objects.currency, objects.leverage)  # создаем аккаунт
    for sym in objects.symbols_list:
        objects.symbols[sym[0]] = Symbol(sym[0], sym[1], sym[2], sym[3],
                                         sym[4], sym[5], sym[6], sym[7])  # создаем символы
        objects.candles[sym[0]] = SymbolPrices(sym[0])  # создаем символы
    objects.market = Market(objects.start, account, objects.symbols, objects.candles)
    objects.market.set_price()
    bot.init()
    run()



