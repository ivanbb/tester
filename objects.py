from time import strptime, mktime
DATE_FORMAT = '%Y%m%d'
TIME_FORMAT = '%H%M%S'
start = (20170103, 101700)
end = (20170103, 181800)
start = int(mktime(strptime(str(start[0])+" "+str(start[1]), DATE_FORMAT+" "+TIME_FORMAT)))
end = int(mktime(strptime(str(end[0])+" "+str(end[1]), DATE_FORMAT+" "+TIME_FORMAT)))
time_frame = 'M5'
balance = 100
currency = 'USD'
symbols_list = [['SBER', 'RUR', 4, 0.01, 1, 0.01, 8, 0]]  # name, base, digits, point, contract_size, tick_size, spread, margin
symbols = {}  # symbols parameters, include ASK and BID prices
candles = {}  # prices of candles (exclude ASK and BID)
leverage = 10
market = 0
datetime = start  # time of 0 candle during testing
