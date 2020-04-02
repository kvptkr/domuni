import mysql.connector

mydb = mysql.connector.connect(
  host="domuni-db.c05r3wxvg4zn.us-east-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  passwd="password",
  database="domuni_db"
)

mycursor = mydb.cursor()

# sql = "DROP TABLE listing;"
# sql = "DELETE FROM lessor WHERE lessor_id = 2;"
sql = "INSERT INTO listing (street,city,postal_code,listing_type,lessor_id,num_rooms,ensuite,dist_to_wlu,dist_to_wloo,is_coed,price) VALUES ('181 Lester Street','Waterloo','N2L 0C2','Apartment',1,5,TRUE,7,7,TRUE,750);"

mycursor.execute(sql)

mydb.commit()