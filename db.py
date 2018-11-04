# -*- coding: utf-8 -*-
import codecs
import sys

from mysql.connector import MySQLConnection, Error
from settings import MySQL

sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

def store_mentions(tag, count, price):
    query = "INSERT INTO Mentions(cashtag_name, count, bitcoin_price) " \
            "VALUES(%s,%s,%s)"
    args = (tag, count, price)

    return db_connect(args, query)


def store_sentiments(positive, negative, mentions_id):
    query = "INSERT INTO Sentiment(positive, negative, mentions_id) " \
            "VALUES(%s,%s,%s)"
    args = (positive, negative, mentions_id)

    return db_connect(args, query)


def get_database_data():
    query = """
        SELECT 
          table_schema , sum( data_length + index_length ) / 1024 / 1024 "Data Base Size in MB", 
          sum( data_free )/ 1024 / 1024 "Free Space in MB" 
        FROM information_schema.TABLES 
        GROUP BY table_schema
    """
    conn = MySQLConnection(**MySQL)
    cursor = conn.cursor()
    cursor.execute(query)

    lists = []
    for item in cursor.fetchall():
        lists.append({
            'name': item[0],
            'size': float(item[1]),
        })
    return lists


def new_database(name):
    query = "CREATE DATABASE IF NOT EXISTS %s" % name
    db_connect({}, query)

    return "%s Successfully Created" % name


def clear_cashtag_by_date(date):
    #   query = """
    #   ALTER TABLE `sentiment`
    # ADD CONSTRAINT `sentiment_fk_1`
    # FOREIGN KEY (`mentions_id`) REFERENCES `mentions` (`id`);
    #     """
    query = "DELETE from mentions WHERE DATE(created_time) = %s" % date
    db_connect({}, query)

    return "%s Successfully Cleared" % date


def clear_cashtag():
    query = "TRUNCATE TABLE sentiment"
    query2 = "DELETE from mentions"
    db_connect({}, query)
    db_connect({}, query2)

    return "Database Cleared Successfully"


def get_graph_data(tagname):
    query = """SELECT 
                    s.id, s.positive, s.negative, m.bitcoin_price, m.cashtag_name, m.created_time
                FROM
                    Sentiment s
                INNER JOIN 
                    Mentions m
                ON 
                    s.mentions_id = m.id
                WHERE m.cashtag_name =%s
                ORDER BY id DESC
                LIMIT 288""" % tagname
    # LIMIT 2016"""

    conn = MySQLConnection(**MySQL)
    cursor = conn.cursor()
    cursor.execute(query)
    lists = []
    for item in cursor.fetchall():
        lists.append({
            'id': item[0],
            'positive': item[1],
            'negative': item[2],
            'bitcoin_price': item[3],
            'cashtag_name': item[4],
            'timestamp': item[5].strftime('%Y-%m-%d %H:%M:%S'),
        })
    return lists


def db_connect(args, query):
    try:
        conn = MySQLConnection(**MySQL)
        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id:' + str(cursor.lastrowid))
        else:
            print('last insert id not found')

        conn.commit()
        return cursor.lastrowid
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
