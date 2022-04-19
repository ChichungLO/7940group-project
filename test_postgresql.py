import psycopg2

# 连接数据库
# conn = psycopg2.connect(dbname="d9meetj91bb2ms", user="kouyhyskzsssia",
#                        password="f21744c8bfe917ea276c6b044fcf0362e50920f32143a927489d076b6d44493a", host="ec2-44-194-4-127.compute-1.amazonaws.com", port="5432")

conn = psycopg2.connect(host="ec2-44-194-4-127.compute-1.amazonaws.com", user="kouyhyskzsssia", dbname="d9meetj91bb2ms",
                        password="f21744c8bfe917ea276c6b044fcf0362e50920f32143a927489d076b6d44493a", sslmode='require')
                        


print(conn)

# 关闭连接
conn.close()
