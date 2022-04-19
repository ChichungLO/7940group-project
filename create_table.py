import psycopg2

conn = psycopg2.connect(host="ec2-44-194-4-127.compute-1.amazonaws.com", user="kouyhyskzsssia", dbname="d9meetj91bb2ms",
                        password="f21744c8bfe917ea276c6b044fcf0362e50920f32143a927489d076b6d44493a", sslmode='require')
print(conn)

cur = conn.cursor()
# cur.execute('''CREATE TABLE COOK
#         (ID INT PRIMARY KEY NOT NULL,
#         NAME TEXT NOT NULL,
#         TIMES INT NOT NULL);''')
# conn.commit()
# print("create table sucessfully")

# cur.execute("INSERT INTO COOK (ID, NAME, TIMES) VALUES (1, 'tomato', 0)")
# cur.execute("INSERT INTO COOK (ID, NAME, TIMES) VALUES (2, 'tofu', 0)")
# cur.execute("INSERT INTO COOK (ID, NAME, TIMES) VALUES (3, 'chips', 0)")
# cur.execute("INSERT INTO COOK (ID, NAME, TIMES) VALUES (4, 'burger', 0)")
# conn.commit()

# cur.execute("""SELECT table_schema, table_name FROM information_schema.tables
#     WHERE table_schema = 'public' ORDER BY table_schema, table_name;""")
# for table in cur.fetchall():
#     print(table)

cur.execute("SELECT ID, NAME, TIMES FROM COOK ORDER BY ID")
rows = cur.fetchall()
for row in rows:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("TIMES = ", row[2], "\n")



# 关闭连接
conn.close()
