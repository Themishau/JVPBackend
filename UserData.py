from app import Logindb
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import cryptography
import pymysql
import pandas as pd
from enum import Enum
import string
import random


def generate_uique_id():
    length = 25

    while True:
        id = ''.join(random.choices(string.ascii_letters, k=length))
        # if objects.filter(code=id).count() == 0:
        #     return code

class TABLENAMES(Enum):
    EMAIL              = 'email'
    PASSWORD              = 'password'


class User(Logindb.Model):
    __tablename__='User'
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_0900_ai_ci'}
    id=Logindb.Column('idUser', Logindb.Integer, primary_key=True)
    email=Logindb.Column('email', Logindb.String(100))
    password=Logindb.Column('password', Logindb.String(100))

    def __init__(self, email, password):
        print(f'user: {email} pass: {password}')
        self.email=email
        self.password=password

    def __repr__(self):
        return self.email


class SQL_Writer():
    def __init__(self, db_connection=None, user_name=None):
        self.db_connection = self.create_connection_pymysql()
        self.user_name = 'UserWriterReader'
        self.cursor = self.db_connection.cursor()

    def testConnection(self):
        sqlEngine = create_engine("mysql+pymysql://UserWriterReader:UserTest123@127.0.0.1:9556/UserData")
        dbConnection = sqlEngine.connect()
        frame = pd.read_sql("select * from User", dbConnection)
        pd.set_option('display.expand_frame_repr', False)
        dbConnection.close()
        if frame is not None:
            print(frame)
            return True
        else:
            return False

    def reconnect_to_Database(self):
        self.close_connection()
        self.db_connection = self.create_connection_pymysql()
        self.cursor = self.db_connection.cursor()

    def create_connection(self):
        sqlEngine = create_engine("mysql+pymysql://UserWriterReader:UserTest123@127.0.0.1:9556/UserData")
        dbConnection = sqlEngine.connect()
        return dbConnection

    def select_statement_to_conncection(self, sql_statement, dbConnection):
        frame = pd.read_sql("select * from QR_Code", dbConnection)
        pd.set_option('display.expand_frame_repr', False)
        print(frame)

    def select_user(self):
        sql = "SELECT * FROM `UserData`"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print('Result: ')
        print(pd.DataFrame(list(result), columns=["Id", "Benefit", "Timestamp"]))


    def create_connection_pymysql(self):
        connection = pymysql.connect(host='127.0.0.1',    # change host-ip if needed
                                     port=9556,           # change port if needed
                                     user='UserWriterReader',
                                     password='UserTest123',
                                     db='UserData')
        print('success')
        return connection

    def close_connection(self):
        self.db_connection.close()