from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initiate application
application = Flask(__name__)

# Database
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@domuni-db.c05r3wxvg4zn.us-east-1.rds.amazonaws.com:3306/domuni_db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To prevent any complaints in console

# Initialize db
db = SQLAlchemy(application)

# Initiate marshmallow
ma = Marshmallow(application)

# Favourite_listing Model/Class - SQLAlchemy
class Favourite_listing(db.Model):
    subletter_id = db.Column(db.Integer, db.ForeignKey('subletter.subletter_id'),primary_key=True )
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.listing_id'),primary_key=True)

    def __init__(self,subletter_id,listing_id):
        self.subletter_id = subletter_id
        self.listing_id = listing_id
  
# Favourite_listing Schema - for marshmallow
class Favourite_listingSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('subletter_id','listing_id')

# Initiate Favourite_listing Schema
favourite_listing_schema = Favourite_listingSchema()
favourite_listings_schema = Favourite_listingSchema(many=True)

################################################################################################

# Listing Model/Class - SQLAlchemy
class Listing(db.Model):
    listing_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(7))
    listing_type = db.Column(db.String(100))
    lessor_id = db.Column(db.Integer, db.ForeignKey('lessor.lessor_id'),nullable=False)
    favourite_listings = db.relationship('Favourite_listing', backref='listing',lazy=True)
    photos = db.relationship('Photo', backref='listing',lazy=True)


    def __init__(self,street,city,postal_code,listing_type,lessor_id):
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.listing_type = listing_type
        self.lessor_id = lessor_id
  
# Listing Schema - for marshmallow
class ListingSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('listing_id','street','city','postal_code','listing_type','lessor_id')

# Initiate Listing Schema
listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)

################################################################################################

# Photo Model/Class - SQLAlchemy
class Photo(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(500))
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.listing_id'),nullable=False)

    def __init__(self,image_path,listing_id):
        self.image_path = image_path
        self.listing_id = listing_id
  
# Photo Schema - for marshmallow
class PhotoSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('image_id','image_path','listing_id')

# Initiate Photo Schema
photo_schema = PhotoSchema()
photos_schema = PhotoSchema(many=True)

################################################################################################

# Lessor Model/Class - SQLAlchemy
class Lessor(db.Model):
    lessor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    listings = db.relationship('Listing', backref='lessor',lazy=True)
    messages = db.relationship('Message', backref='lessor',lazy=True)

    def __init__(self,user_id):
        self.user_id = user_id
  
# Lessor Schema - for marshmallow
class LessorSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('user_id','lessor_id')

# Initiate Lessor Schema
lessor_schema = LessorSchema()
lessors_schema = LessorSchema(many=True)

################################################################################################

# Message Model/Class - SQLAlchemy
class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    lessor_id = db.Column(db.Integer,db.ForeignKey('lessor.lessor_id'))
    subletter_id = db.Column(db.Integer,db.ForeignKey('subletter.subletter_id'))
    text = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime)
    lessor_sent = db.Column(db.Boolean)

    def __init__(self,lessor_id,subletter_id,text,timestamp,lessor_sent):
        self.lessor_id = lessor_id
        self.subletter_id = subletter_id
        self.text = text
        self.timestamp = timestamp
        self.lessor_sent = lessor_sent
  
# Message Schema - for marshmallow
class MessageSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('message_id','lessor_id','subletter_id','text','timestamp','lessor_sent')

# Initiate Message Schema
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

################################################################################################

# Subletter Model/Class - SQLAlchemy
class Subletter(db.Model):
    subletter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    num_rooms = db.Column(db.Integer)
    ensuite = db.Column(db.Boolean)
    dist_to_wlu = db.Column(db.Integer)
    dist_to_wloo = db.Column(db.Integer)
    is_female = db.Column(db.Boolean)
    min_price = db.Column(db.Integer)
    max_price = db.Column(db.Integer)
    favourite_listings = db.relationship('Favourite_listing', backref='subletter',lazy=True)
    messages = db.relationship('Message', backref='subletter',lazy=True)

    def __init__(self,user_id,num_rooms,ensuite,dist_to_wlu,dist_to_wloo,is_female,min_price,max_price):
        self.user_id = user_id
        self.num_rooms = num_rooms
        self.ensuite = ensuite
        self.dist_to_wlu = dist_to_wlu
        self.dist_to_wloo = dist_to_wloo
        self.is_female = is_female
        self.min_price = min_price
        self.max_price = max_price
  
# Subletter Schema - for marshmallow
class SubletterSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('subletter_id','user_id','num_rooms','ensuite','dist_to_wlu','dist_to_wloo','is_female','min_price','max_price')

# Initiate Subletter Schema
subletter_schema = SubletterSchema()
subletters_schema = SubletterSchema(many=True)

################################################################################################

# User Model/Class - SQLAlchemy
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    subletter = db.relationship('Subletter', backref='user',uselist=False)
    lessor = db.relationship('Lessor', backref='user',uselist=False)
    dob = db.Column(db.DateTime)
    phone_num = db.Column(db.String(20))
    email = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    last_login = db.Column(db.DateTime)

    def __init__(self,dob,phone_num,email,first_name,last_name,password,last_login):
        self.dob = dob
        self.phone_num = phone_num
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.last_login = last_login
  
# User Schema - for marshmallow
class UserSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('user_id','subletter_id','lessor_id','dob','phone_num','email','first_name','last_name','password','last_login')

# Initiate User Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

################################################################################################

# ENDPOINT - Get all students
@application.route('/students-all',methods=['GET'])
def get_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result)


# Run server
if __name__ == '__main__':
    # application.run(host='0.0.0.0')
    application.run(debug=True)