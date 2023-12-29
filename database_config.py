import pymysql
import configparser


def get_db_connection():
    config = configparser.ConfigParser()
    config.read('config.conf')

    db_host = config['DATABASE']['host']
    db_user = config['DATABASE']['user']
    db_pass = config['DATABASE']['password']
    db_name = config['DATABASE']['dbname']

    return pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name)
