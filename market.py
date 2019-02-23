from time import strptime, mktime
from datetime import datetime
from objects import DATE_FORMAT, TIME_FORMAT


class Market(object):
    def __init__(self, timestamp, acc, symbols, candles):
        self.datetime = timestamp
        self.account = acc
        self.__order_book = [] #{'ticket', 'symbol', 'volume', 'type', 'price'}
        self.__symbols = symbols
        self.prices = candles

    def __merge_positions(self, symbol):
        keys = self.account.check_positions(symbol)  # get tickets of all positions by this symbol
        if keys is None:
            return
        try:
            amount = self.account.account_info('ACCOUNT_ASSETS')[symbol]  # getting amount of currency
        except KeyError:
            for key in keys:
                self.account.positions.pop(key)  # if assets eq. 0, pop all positions

    def __open_buy(self, order):
        """Executing buy orders"""
        self.account.orders.remove(order['ticket']) # removing order from account
        if self.__symbols[order['symbol']].symbol_info("SYMBOL_MARGIN") == 0:  # for non-margin assets
            order_amount = order['volume']*order['price']
            if self.account.account_info('ACCOUNT_LEVERAGE') == 1:  # for non-margin trading
                self.account.set_balance(order_amount*-1)  # changing balance
            else:
                self.account.set_margin(float(order_amount)/self.account.account_info('ACCOUNT_LEVERAGE'))

        else:  # else if asset using margin trading
            symbol_margin = self.__symbols[order['symbol']].symbol_info("SYMBOL_MARGIN")
            order_amount = order['volume'] * symbol_margin  # margin for order
            self.account.set_margin(float(order_amount) / self.account.account_info('ACCOUNT_LEVERAGE'))  # calculating margin for position

        self.account.set_assets((order['symbol'], order['volume']))  # adding asset to account
        self.account.positions[order['ticket']] = {'symbol': order['symbol'], 'volume': order['volume'],
                                                    'type': 'BUY', 'price': order['price'], 'time': self.datetime}  # adding a new position
        self.__merge_positions(order['symbol'])  # checking the presence of other positions for combining them into one
        self.__order_book.remove(order)  # then removing executed order from order book

    def __open_sell(self, order):
        """Executing buy orders"""
        self.account.orders.remove(order['ticket']) # removing order from account
        if self.__symbols[order['symbol']].symbol_info("SYMBOL_MARGIN") == 0:  # for non-margin assets
            order_amount = order['volume']*order['price']
            if self.account.account_info('ACCOUNT_LEVERAGE') == 1:  # for non-margin trading
                self.account.set_margin(order_amount)  # changing margin as amount of order
            else:
                self.account.set_margin(float(order_amount)/self.account.account_info('ACCOUNT_LEVERAGE'))

        else:  # else if asset using margin trading
            symbol_margin = self.__symbols[order['symbol']].symbol_info("SYMBOL_MARGIN")
            order_amount = order['volume'] * symbol_margin  # margin for order
            self.account.set_margin(float(order_amount) / self.account.account_info('ACCOUNT_LEVERAGE'))  # calculating margin for position

        self.account.set_assets((order['symbol'], order['volume']*-1))  # adding asset to account
        self.account.positions[order['ticket']] = {'symbol': order['symbol'], 'volume': order['volume'],
                                                   'type': 'SELL', 'price': order['price'], 'time': self.datetime}  # adding a new position
        self.__merge_positions(order['symbol'])  # checking the presence of other positions for combining them into one
        self.__order_book.remove(order)  # then removing executed order from order book

    def open_position(self):
        for order in list(self.__order_book):

            if order['type'] == 'ORDER_TYPE_BUY_LIMIT':
                if self.__symbols[order['symbol']].symbol_info("PRICE_BID") <= order['price']:
                    self.__open_buy(order)

            elif order['type'] == 'ORDER_TYPE_SELL_LIMIT':
                if self.__symbols[order['symbol']].symbol_info("PRICE_ASK") >= order['price']:
                    self.__open_sell(order)

            elif order['type'] == 'ORDER_TYPE_BUY_STOP':
                if self.__symbols[order['symbol']].symbol_info("PRICE_BID") <= order['price']:
                    self.__open_buy(order)

            elif order['type'] == 'ORDER_TYPE_SELL_STOP':
                if self.__symbols[order['symbol']].symbol_info("PRICE_ASK") >= order['price']:
                    self.__open_sell(order)

            elif order['type'] == 'ORDER_TYPE_BUY':  # for market order
                self.__open_buy(order)

            elif order['type'] == 'ORDER_TYPE_SELL':  # for market order
                self.__open_sell(order)

    def order_place(self, symbol, vol, order_type, price):
        from random import randint
        ticket = randint(1000, 9999)
        self.__order_book.append({'ticket': ticket, 'symbol': symbol, 'volume': vol, 'type': order_type, 'price': price})
        self.account.orders.append(ticket)
        return ticket
        pass

    def set_price(self):
        date = datetime.fromtimestamp(self.datetime).strftime(DATE_FORMAT)  # get date from timestamp
        time = datetime.fromtimestamp(self.datetime-60).strftime(TIME_FORMAT)  # get time from timestamp
        for key in self.__symbols.keys():  # for each symbol
            self.__symbols[key]._set_ask_bid(self.prices[key].i_close('M1', date, time))  # setting prices from close of prev minute


class SymbolPrices(object):
    """Defines functions for access to candles"""
    def __init__(self, currency):
        from pandas import read_csv
        self.data = 0
        self.__rates = {'M1': 1, 'M5': 5, 'M15': 15, 'M30': 30, 'H1': 60, 'H4': 240, 'D1': 1440, 'W1': 10080,
                        'm1': 43800}  # minutes in period
        try:
            self.data = read_csv('data/'+currency+'M1.csv')
        except FileNotFoundError:
            print('FileNotFoundError')

    def i_open(self, tf, date, time):
            try:
                return self.data.loc[(self.data['<DATE>'] == int(date)) & (self.data['<TIME>'] == int(time)), ['<OPEN>']]['<OPEN>'].tolist()[0]
            except AttributeError:
                print('AttributeError: you didnt initialized this time frame or data is empty!')
            except IndexError:
                print('AttributeError: you didnt initialized this time frame or data is empty!')

    def i_close(self, tf, date, time):
        try:
            _timestamp = mktime(strptime(str(date) + " " + str(time),
                                         DATE_FORMAT + " " + TIME_FORMAT))  # get timestamp from date and time for iter
            _timestamp += 60*self.__rates[tf]
            date = datetime.fromtimestamp(_timestamp).strftime(DATE_FORMAT)  # get date from timestamp
            time = datetime.fromtimestamp(_timestamp).strftime(TIME_FORMAT)  # get time from timestamp
            return self.data.loc[(self.data['<DATE>'] == int(date)) & (self.data['<TIME>'] == int(time)), ['<CLOSE>']]['<CLOSE>'].tolist()[0]
        except AttributeError:
            print('AttributeError: you didnt initialized this time frame or data is empty!')

    def i_high(self, tf, date, time):
        try:
            _timestamp = mktime(strptime(str(date)+" "+str(time), DATE_FORMAT+" "+TIME_FORMAT)) # get timestamp from date and time for iter
            high = self.data.loc[(self.data['<DATE>'] == int(date)) & (self.data['<TIME>'] == int(time)), ['<HIGH>']]
            if high.empty:
                return 0
            high = high['<HIGH>'].tolist()[0]
            for _ in range(1, self.__rates[tf], 1):  # iterating for make period's volume
                _timestamp += 60
                date = datetime.fromtimestamp(_timestamp).strftime(DATE_FORMAT)  # get date from timestamp
                time = datetime.fromtimestamp(_timestamp).strftime(TIME_FORMAT)  # get time from timestamp
                price = self.data.loc[(self.data['<DATE>'] == int(date)) & (self.data['<TIME>'] == int(time)), ['<HIGH>']]
                if price.empty:
                    continue
                price = price['<HIGH>'].tolist()[0]
                if price < high:
                    high = price
            return high
        except AttributeError:
            print('AttributeError: you didnt initialized this time frame or data is empty!')
        except ValueError:
            pass

    def i_low(self, tf, date, time):
        try:
            _timestamp = mktime(strptime(str(date)+" "+str(time), DATE_FORMAT+" "+TIME_FORMAT)) # get timestamp from date and time for iter
            low = self.data.loc[(self.data['<DATE>'] == int(date)) & (self.data['<TIME>'] == int(time)), ['<LOW>']]
            if low.empty:
                return 0
            low = low['<LOW>'].tolist()[0]
            for _ in range(1, self.__rates[tf], 1):  # iterating for make period's volume
                _timestamp += 60
                date = datetime.fromtimestamp(_timestamp).strftime(DATE_FORMAT)  # get date from timestamp
                time = datetime.fromtimestamp(_timestamp).strftime(TIME_FORMAT)  # get time from timestamp
                price = self.data.loc[(self.data['<DATE>'] == int(date)) & (self.data['<TIME>'] == int(time)), ['<LOW>']]
                if price.empty:
                    continue
                price = price['<LOW>'].tolist()[0]
                if price < low:
                    low = price
            return low
        except AttributeError:
            print('AttributeError: you didnt initialized this time frame or data is empty!')
        except ValueError:
            pass

    def i_volume(self, tf, date, time):
        try:
            _timestamp = mktime(strptime(str(date)+" "+str(time), DATE_FORMAT+" "+TIME_FORMAT)) # get timestamp from date and time for iter
            vol = 0
            for _ in range(0, self.__rates[tf]):  # iterating for make period's volume
                date = datetime.fromtimestamp(_timestamp).strftime(DATE_FORMAT)  # get date from timestamp
                time = datetime.fromtimestamp(_timestamp).strftime(TIME_FORMAT)  # get time from timestamp
                _timestamp += 60
                _vol = self.data.loc[(self.data['<DATE>'] == int(date)) & (self.data['<TIME>'] == int(time)), ['<VOL>']]
                if _vol.empty:
                    continue
                vol += _vol['<VOL>'].tolist()[0]
            return vol
        except AttributeError:
            print('AttributeError: you didnt initialized this time frame or data is empty!')


# sym = SymbolPrices('EURUSD', ['M15'])
#
#
# open1 = sym.i_open('M15', '1971.01.13', '00:00')
# pass
