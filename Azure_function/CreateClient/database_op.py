import psycopg2
import pandas as pd
import pymssql

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
        
    # def start_connection(self):
    #     # self.conn = psycopg2.connect(database = self.database, user = self.user , password = self.password, host = self.host, port = self.port) #Get connection object by initializing connection to database. 
    #     # self.cursor = self.conn.cursor()  
    #     self.con = pymssql.connect(self.server, self.user, self.password, self.database)
    #     self.cursor = self.conn.cursor()  
    #     return self.conn, self.cursor
    
    # def close_connection(self):
    #     self.con.commit()
    #     self.cursor.close()
    #     self.con.close()
        
    def insert_data(self, accountnumber, name, account_id,lastmodifieddate):
        # _,cursor = self.start_connection()
        print("Connection established")        
        self.cursor.execute("INSERT INTO salesforce.account (accountnumber, name, accountid, Lastmodifieddate) VALUES (%s, %s, %s, %s);", (accountnumber, name, account_id, lastmodifieddate))
        print("Row inserted")  
        self.con.commit()
        # self.cursor.close()
        # self.con.close()  
        # self.close_connection()                    
        return "Data inserted successfully"

    def get_data(self):
        # _,cursor = self.start_connection()
        query = "SELECT * FROM salesforce.account;"
        df = pd.read_sql_query(query, con=self.con)
        print(df.head())
        self.con.commit()
        # self.cursor.close()
        # self.con.close()  
        # self.close_connection()
        return df
    
    # def get_accname_accnumber(self,accountnumber,accountname):
    #     _,cursor = self.start_connection()
    #     try:
    #         query = "SELECT name FROM salesforce.account WHERE accountnumber = {} AND accountname={};".format(accountnumber,accountname)
    #         df = pd.read_sql_query(query, con=self.conn)
    #         self.close_connection()
    #         return 1
    #     except:        
    #         return 0
                
    def check_accnumber(self,accountnumber):
        # _,cursor = self.start_connection()
        query = "select * from salesforce.account where accountnumber = '{}';".format(str(accountnumber))
        print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        self.con.commit()
        # self.cursor.close()
        # self.con.close()  
        # self.close_connection()
        return result
    
    def update_record(self,accountnumber, name):
        # _,cursor = self.start_connection()
        query = "UPDATE salesforce.account SET name = '{}' WHERE accountnumber = '{}';".format(name,accountnumber)
        self.cursor.execute(query)
        self.con.commit()
        # self.cursor.close()
        # self.con.close()  
        # self.close_connection()
        return "Account updated successfully"
    
# cls_obj = Database_op()    
# res = cls_obj.check_accnumber("123456")
# if res==None:
#     print("No record found")
# else:
#     cls_obj.update_record("123456","Vedity")
        