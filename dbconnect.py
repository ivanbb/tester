from mysql.connector import MySQLConnection, Error
from datetime import datetime
from configparser import ConfigParser


def read_db_config(filename='db_config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def insert_trade(trade, ticket):
    query = "INSERT INTO trades(time,ticket,symbol,type,volume,price) VALUES(%s, %s, %s, %s, %s, %s)"
    date_time = datetime.fromtimestamp(trade['time']).strftime('%Y-%m-%d %H:%M:%S')
    args = (date_time, ticket, trade['symbol'], trade['type'], trade['volume'], trade['price'])

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def insert_balance(time, balance, equity):
    query = "INSERT INTO balance(time,balance,equity) VALUES(%s, %s, %s)"
    date_time = datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    args = (date_time, balance, equity)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def query_with_fetchall(name):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM symbols WHERE name = %(name)s", {'name': name})
        rows = cursor.fetchall()

        return rows

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# query_with_fetchall("SBER")