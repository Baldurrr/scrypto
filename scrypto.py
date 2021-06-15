#!/usr/bin/python3

from pycoingecko import CoinGeckoAPI
import mysql.connector
from mysql.connector import errors
import json
from environs import Env
import os
import time
from datetime import datetime
import itertools

def data_analyzer(nb_devise,devise1,devise2,api_response,sql_user,sql_password,sql_host,sql_db,sql_port):
    try:
        conn = mysql.connector.connect(
        user=sql_user,
        password=sql_password,
        host=sql_host,
        database=sql_db, 
        port=sql_port,auth_plugin='mysql_native_password')

        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Connected to database")
        cur = conn.cursor()

        for crypto in crypto_list:
            if crypto == "bitcoin":
                print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | BITCOIN SELECTED ")
                btc_response=api_response['bitcoin']

                if int(nb_devise) == 1:
                    btc_value_1=btc_response[devise1]
                    btc_value_date=btc_response['last_updated_at']
                    converted_ts=datetime.fromtimestamp(btc_value_date)
                    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Sending to bitcoin table")
                    field_devise1="value_"+str(devise1)
                    try:
                        cur.execute("INSERT into bitcoin (time,metric,"+field_devise1+") VALUES ,'"+str(converted_ts)+"','btc_curve',"+str(btc_value_1)+")")
                        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query successfull")
                        conn.commit()

                    except mysql.connector.Error as e:
                        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query failed !!")
                        print(e)

                elif int(nb_devise) ==2:
                    btc_value_1=btc_response[devise1]
                    btc_value_2=btc_response[devise2]
                    btc_value_date=btc_response['last_updated_at']
                    converted_ts=datetime.fromtimestamp(btc_value_date)
                    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Sending to bitcoin table")
                    field_devise1="value_"+str(devise1)
                    field_devise2="value_"+str(devise2)
                    try:
                        cur.execute("INSERT into bitcoin (time,metric,"+field_devise1+","+field_devise2+") VALUES ('"+str(converted_ts)+"','btc_curve',"+str(btc_value_1)+","+str(btc_value_2)+")")
                        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query successfull")
                        conn.commit()

                    except mysql.connector.Error as e:
                        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query failed !!")
                        print(e)
                        
                else:
                    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Number of currency not correct")

            elif crypto =="ethereum":
                print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | ETHEREUM SELECTED")
                eth_response=api_response['ethereum']

                if int(nb_devise) == 1:
                    eth_value_1=eth_response[devise1]
                    eth_value_date=eth_response['last_updated_at']
                    converted_ts=datetime.fromtimestamp(eth_value_date)
                    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Sending to ethereum table")
                    field_devise1="value_"+str(devise1)
                    try:
                        cur.execute("INSERT into ethereum (time,metric,"+field_devise1+") VALUES ('"+str(converted_ts)+"','eth_curve',"+str(eth_value_1)+")")
                        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query successfull")
                        conn.commit()

                    except mysql.connector.Error as e:
                        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query failed !!")
                        print(e)

                elif int(nb_devise) == 2:
                    eth_value_1=eth_response[devise1]
                    eth_value_2=eth_response[devise2]
                    eth_value_date=eth_response['last_updated_at']
                    converted_ts=datetime.fromtimestamp(eth_value_date)
                    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Sending to ethereum table")
                    field_devise1="value_"+str(devise1)
                    field_devise2="value_"+str(devise2)
                    try:
                        cur.execute("INSERT into ethereum (time,metric,"+field_devise1+","+field_devise2+") VALUES ('"+str(converted_ts)+"','eth_curve',"+str(eth_value_1)+","+str(eth_value_2)+")")
                        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query successfull")
                        conn.commit()

                    except mysql.connector.Error as e:
                        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query failed !!")
                        print(e)

                else:
                    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Number of currency out of range")

            else:
                print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Not a valid currency")
        conn.close()    
        
    except mysql.connector.Error as e:
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Connection to database failed")
        print(e)


def devise_checking(devise1,devise2,cryptomoney,sql_user,sql_password,sql_host,sql_db,sql_port):
    nb_devise=""
    if devise1 != "" and devise2 == "":
        api_response=api_connector.get_price(ids=cryptomoney, vs_currencies=[devise1],include_last_updated_at=True)
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | API response: "+str(api_response))
        nb_devise="1"
        data_analyzer(nb_devise,devise1,devise2,api_response,sql_user,sql_password,sql_host,sql_db,sql_port)

    elif devise1 != "" and devise2 != "":
        api_response=api_connector.get_price(ids=cryptomoney, vs_currencies=[devise1,devise2],include_last_updated_at=True)
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | API response: "+str(api_response))
        nb_devise="2"
        data_analyzer(nb_devise,devise1,devise2,api_response,sql_user,sql_password,sql_host,sql_db,sql_port)

    else:
        print("Number of currency not correct")


if __name__ == '__main__':

    print("                            _        ")
    print("                           | |       ")
    print("  ___  ___ _ __ _   _ _ __ | |_ ___  ")
    print(" / __|/ __| '__| | | | '_ \| __/ _ \ ")
    print(" \__ \ (__| |  | |_| | |_) | || (_) |")
    print(" |___/\___|_|   \__, | .__/ \__\___/ ")
    print("                 __/ | |             ")
    print("                |___/|_|             ")
    
    while True:
        api_connector = CoinGeckoAPI()

        env = Env()
        env.read_env()

        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Getting var env")
        try:
            crypto_var= str(os.environ.get('CRYPTO_LIST'))
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | CRYPTO_LIST: "+crypto_var)
        except:
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Mutliple currency must be separated by a ','")
            break

        devise1=str(os.environ.get('DEVISE_1'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | DEVISE_1: "+devise1)

        try:
            devise2=str(os.environ.get('DEVISE_2'))
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | DEVISE_2: "+devise2)
        except:
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | DEVISE_2 not specified")
            break

        try: 
            scrape_time=int(os.environ.get('SCRAPE_TIME'))
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SCRAPE_TIME: "+str(scrape_time))
        except:
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | A scrape interval must be set (time in second, ex: 300 = 5min)")
            break

        sql_user= str(os.environ.get('SQL_USER'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_USER: "+sql_user)

        sql_password= str(os.environ.get('SQL_PASSWORD'))
        if sql_password == "":
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_PASSWORD is empty")
            break

        else:
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_PASSWORD: *********")

        sql_host= str(os.environ.get('SQL_HOST'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_HOST: "+sql_host)
        sql_db= str(os.environ.get('SQL_DB'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_DB: "+sql_db)
        sql_port= int(os.environ.get('SQL_PORT'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_PORT: "+str(sql_port))

        crypto_list=crypto_var.split(',')
        if len(crypto_list)>2:
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Number of currency > 2")
            break

        if len(crypto_list)==1:
            cryptomoney=crypto_list[0]
            devise_checking(devise1,devise2,cryptomoney,sql_user,sql_password,sql_host,sql_db,sql_port)

        elif len(crypto_list)>1:
            temp_str=""
            for crypto in crypto_list:
                temp_str=temp_str+','+str(crypto)

            cryptomoney=temp_str[1:]
            devise_checking(devise1, devise2, cryptomoney,sql_user,sql_password,sql_host,sql_db,sql_port)

        time.sleep(scrape_time)
