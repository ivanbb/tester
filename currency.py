class Symbol:
    def __init__(self, name, base, digits, point, contract_size, tick_size, spread, margin):
        self.__name = name
        self.__base = base
        self.__digits = digits
        self.__point = point
        self.__contract_size = contract_size
        self.__tick_size = tick_size
        self.__spread = spread
        self.__ask = 0
        self.__bid = 0
        self.__margin = margin

    def symbol_info(self, var):
        variables = {'SYMBOL_TRADE_TICK_SIZE': self.__tick_size,
                     'SYMBOL_POINT': self.__point,
                     'SYMBOL_TRADE_CONTRACT_SIZE': self.__contract_size,
                     'SYMBOL_CURRENCY_BASE': self.__base,
                     'SYMBOL_DIGITS': self.__digits,
                     'SYMBOL_SPREAD': self.__spread,
                     'SYMBOL_ASK': self.__ask,
                     'SYMBOL_BID': self.__bid,
                     'SYMBOL_MARGIN': self.__margin
                     }
        try:
            return variables[var]
        except KeyError as e:
            print(e)
            return -1

    def _set_ask_bid(self, ask):
        self.__ask = ask
        self.__bid = ask+self.__spread


