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
        
    # def get_acc_id(self,client_id):
    #     self.cursor.execute("SELECT accountid FROM salesforce.account WHERE infoxchange_id = '{}';".format(client_id))
    #     data = self.cursor.fetchall()
    #     print(data[0][0])
    #     if data[0][0]!="None":
    #         return data[0][0]
    #     else:
    #         return None
    
    def update_varified_status(self, Account_id, status):                
        self.cursor.execute("UPDATE salesforce.account SET IsVerified = '{}' WHERE accountid = '{}';".format(status, Account_id))
        print("Insertion done")  
        self.con.commit()                        
        return "Data inserted successfully"
            
    
# cls_obj = Database_op()    
# res = cls_obj.get_acc_id("22774")
# print(res)
# if res==None:
#     print("No record found")
# else:
#     cls_obj.update_record("123456","Vedity")
        