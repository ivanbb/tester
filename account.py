class Account:
    __balance = 0

    def __init__(self, balance, currency, leverage):
        self.__balance = balance
        self.__equity = balance
        self.__free_margin = balance
        self.__margin = 0
        self.__currency = currency
        self.__leverage = leverage
        self.__assets = {currency: balance}  # активы
        self.__profit = 0
        self.positions = {}
        self.orders = []

    def account_info(self, var):
        variables = {'ACCOUNT_BALANCE': self.__balance,
                     'ACCOUNT_PROFIT': self.__profit,
                     'ACCOUNT_EQUITY': self.__equity,
                     'ACCOUNT_MARGIN_FREE': self.__free_margin,
                     'ACCOUNT_MARGIN': self.__free_margin,
                     'ACCOUNT_CURRENCY': self.__currency,
                     'ACCOUNT_LEVERAGE': self.__leverage,
                     'ACCOUNT_ASSETS': self.__assets,
                     }
        return variables[var]

    def set_balance(self, var):
        self.__balance += var
        self.__assets[self.__currency] += var

    def set_equity(self, var):
        self.__equity += var

    def set_margin(self, var):
        self.__margin += var

    def set_assets(self, assets):
        try:
            self.__assets[assets[0]] += assets[1]  # change asset's amount
        except KeyError:
            self.__assets[assets[0]] = assets[1]  # change asset's amount
        if self.__assets[assets[0]] == 0:  # if amount == 0, remove is from dict
            self.__assets.pop(assets[0])

    def check_positions(self, symbol):
        """checking positions with the same asset"""
        keys = []
        for key in self.positions.keys():
            if self.positions[key]['symbol'] == symbol:
                keys.append(key)
        return keys

    def calc(self):
        """Function for calculating free margin, profit and equity"""
        from objects import symbols

        for position in self.positions:
            position = self.positions[position]
            if position['type'] == 'BUY':
                bid = symbols[position['symbol']].symbol_info("PRICE_BID")
                tick = symbols[position['symbol']].symbol_info("SYMBOL_POINT")
                contract = symbols[position['symbol']].symbol_info("SYMBOL_TRADE_CONTRACT_SIZE")
                pos_profit = (bid - position['price'])*position['volume']*tick*contract  # calculating position's profit
                self.set_equity(pos_profit)  # and changing equity

            elif position['type'] == 'SELL':
                ask = symbols[position['symbol']].symbol_info("PRICE_ASK")
                tick = symbols[position['symbol']].symbol_info("SYMBOL_POINT")
                contract = symbols[position['symbol']].symbol_info("SYMBOL_TRADE_CONTRACT_SIZE")
                pos_profit = (position['price']-ask)*position['volume']*tick*contract
                self.set_equity(pos_profit)

        self.__profit = self.__equity-self.__balance

        print('equity={0}, profit={1}'.format(self.__equity, self.__profit))

