from account import Account
from currency import Symbol
from datetime import datetime
from objects import DATE_FORMAT, TIME_FORMAT
from market import Market, SymbolPrices
import bot as bot
import objects


def run():
    """Running market"""
    for __time in range(objects.start, objects.end, 60):
        objects.market.datetime = __time
        objects.datetime = __time
        objects.market.set_price()
        bot.on_tick()
        objects.market.open_position()


if __name__ == '__main__':
    account = Account(objects.balance, objects.currency, objects.leverage)  # создаем аккаунт
    for sym in objects.symbols_list:
        objects.symbols[sym[0]] = Symbol(sym[0], sym[1], sym[2], sym[3],
                                         sym[4], sym[5], sym[6], sym[7])  # создаем символы
        objects.candles[sym[0]] = SymbolPrices(sym[0])  # создаем символы
    objects.market = Market(objects.start, account, objects.symbols, objects.candles)
    objects.market.set_price()
    run()



