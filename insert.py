import mysql.connector

mydb = mysql.connector.connect(
  host="domuni-db.c05r3wxvg4zn.us-east-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  passwd="password",
  dbname="domuni_db"
)

mycursor = mydb.cursor()

# sql = "DROP TABLE student;"

sql = "INSERT INTO lessor (dob,phone_num,email,first_name,last_name,password,last_login,num_rooms_available,num_rooms_total,ensuite,dist_to_wlu,dist_to_wloo,is_female,coed,min_price,max_price) VALUES ('19990718 12:00:00 AM','0192854578','test2@gmail.com','John','Smith','password','20200402 12:00:00 AM',1,5,TRUE,15,15,FALSE,'either',400,1000);"
# Read more: https://javarevisited.blogspot.com/2012/10/sql-query-to-find-all-table-on-database-mysql-sqlserver.html#ixzz6IOV0DuyR"

mycursor.execute(sql)

mydb.commit()
# import sqlalchemy

# url = 'mysql://%s:%s@%s' % ('admin', 'password', 'domuni-db.c05r3wxvg4zn.us-east-1.rds.amazonaws.com:3306')
# engine = sqlalchemy.create_engine(url)  # connect to server

# create_str = "CREATE DATABASE IF NOT EXISTS %s ;" % ('domuni')
# engine.execute(create_str)
# engine.execute("USE location;")

# # db.create_all()
# # db.session.commit()