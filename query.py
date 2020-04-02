import pandas as pd
import pymysql

host = "domuni-db.c05r3wxvg4zn.us-east-1.rds.amazonaws.com"
port = 3306
dbname = 'domuni_db'
user = "admin"
password = "password"

conn = pymysql.connect(host, user = user, port = port, passwd = password, db=dbname)

# response = pd.read_sql("",con=conn)

# response = pd.read_sql(sql,con=conn)

# Query to see all tables
response = pd.read_sql("SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema = 'domuni_db'",con=conn)

print(response)