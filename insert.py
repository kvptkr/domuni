import mysql.connector

mydb = mysql.connector.connect(
  host="domuni-db.c05r3wxvg4zn.us-east-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  passwd="password",
  database="domuni_db"
)

mycursor = mydb.cursor()

# sql = "DROP TABLE subletter;"
# sql = "DELETE FROM lessor WHERE lessor_id = 2;"
sql = "INSERT INTO subletter (dob,phone_num,email,first_name,last_name,password,last_login,num_rooms_available,num_rooms_total,ensuite,dist_to_wlu,dist_to_wloo,is_female,coed,min_price,max_price) VALUES ('19990618 12:00:00 AM','5192854578','jishaanminsariya@gmail.com','Jishaan','Minsariya','password','20200402 12:00:00 AM',1,5,TRUE,15,15,FALSE,'either',400,1000);"

mycursor.execute(sql)

mydb.commit()