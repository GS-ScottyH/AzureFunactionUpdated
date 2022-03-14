import psycopg2
import pandas as pd
import pymssql
from sqlalchemy import null

class Database_op:
    def __init__(self):
        # Update connection string information
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
        
        
    def insert_data(self, name, first_name, last_name, infoxchange_id):                
        self.cursor.execute("UPDATE salesforce.account SET first_name = '{}', last_name= '{}', infoxchange_id = '{}' WHERE accountnumber = '{}';".format(first_name,last_name,infoxchange_id,name))
        print("Insertion done")  
        self.con.commit()                        
        return "Data inserted successfully"

    def check_infoxcangeid(self, name):
        self.cursor.execute("SELECT infoxchange_id FROM salesforce.account WHERE name = '{}';".format(name))
        data = self.cursor.fetchall()
        print(data[0][0])
        if data[0][0]!="None":
            return True
        else:
            return False

    def update_data(self, name, first_name, last_name):
        self.cursor.execute("UPDATE salesforce.account SET first_name = '{}', last_name= '{}' WHERE accountnumber = '{}';".format(first_name,last_name,name))
        print("Updation done")  
        self.con.commit()                        
        return "Data updated successfully"
    
# database_obj = Database_op()
# msg = database_obj.check_infoxcangeid("infosys34")
# msg = database_obj.update_data("infosys33","vish","bar")
# print(msg)