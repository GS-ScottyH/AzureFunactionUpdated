import psycopg2
import pandas as pd
import pymssql

class Database_op:
    def __init__(self):        
        self.database="DB_NAME"
        self.user = "USER_NAME"
        self.password = "#######"
        self.host = "HOST_URL"
        self.port = "5432"
        self.sslmode = "require"
        self.connection_string = "postgresql://" + self.user + ":" + self.password + "@" + self.host + ":" + self.port + "/" + self.database # Make database connection string.
        self.conn = psycopg2.connect(database = self.database, user = self.user , password = self.password, host = self.host, port = self.port)
        self.cursor = self.conn.cursor()  
        
        # self.server="HOST/SERVER_NAME"
        # self.database="DB_NAME"
        # self.user="USER"
        # self.password="#######"  
        # self.con = pymssql.connect(self.server, self.user, self.password, self.database)
        # self.cursor = self.con.cursor()        
        
    def verify_api_key(self,Api_key):
        self.cursor.execute("SELECT * FROM salesforce.apitoken WHERE accesstoken = '{}';".format(Api_key))
        data = self.cursor.fetchall()
        return len(data)
       

        