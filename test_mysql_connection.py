<<<<<<< Updated upstream
import mysql.connector
 
mydb = mysql.connector.connect(
  host="106.52.171.168",       # 数据库主机地址
  user="comp7940gp13",    # 数据库用户名
  passwd="comp7940gp13"   # 数据库密码
)
 
print(mydb)
=======
import pyodbc
server = 'comp7940gp13.database.windows.net'
database = 'comp7940gp13'
username = 'comp7940gp13'
password = '{comp7940_gp13}'   
driver= '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()
>>>>>>> Stashed changes
