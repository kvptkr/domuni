import mysql.connector

mydb = mysql.connector.connect(
  host="domuni-db.c05r3wxvg4zn.us-east-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  passwd="password",
  database="domuni_db"
)

mycursor = mydb.cursor()

# sql = "DROP TABLE lessor;"
# sql = "DELETE FROM lessor WHERE lessor_id = 2;"

sql = "INSERT INTO listing (street,city,postal_code,listing_type,lessor_id,num_rooms_available,ensuite,dist_to_wlu,dist_to_wloo,coed,price,num_rooms_total) VALUES ('181 Lester Street', 'Waterloo','N2L 0C2','Sublet',1, 2,TRUE,7,7,'either',700,5);"

mycursor.execute(sql)

mydb.commit()