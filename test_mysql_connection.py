import mysql.connector
 
mydb = mysql.connector.connect(
  host="106.52.171.168",       # 数据库主机地址
  user="comp7940gp13",    # 数据库用户名
  passwd="comp7940gp13"   # 数据库密码
)
 
print(mydb)