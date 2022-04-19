import mysql.connector
 
mydb = mysql.connector.connect(
  host="comp7940gp13.database.windows.net:1433",       # 数据库主机地址
  user="comp7940gp13",    # 数据库用户名
  passwd="comp7940_gp13"   # 数据库密码
)
 
print(mydb)