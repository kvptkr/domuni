from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import numpy as np
import json
from datetime import datetime

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
    num_rooms_available = db.Column(db.Integer)
    num_rooms_total = db.Column(db.Integer)
    ensuite = db.Column(db.Boolean)
    dist_to_wlu = db.Column(db.Integer)
    dist_to_wloo = db.Column(db.Integer)
    coed = db.Column(db.String(100))
    price = db.Column(db.Integer)
    lessor_id = db.Column(db.Integer, db.ForeignKey('lessor.lessor_id'),nullable=False)
    favourite_listings = db.relationship('Favourite_listing', backref='listing',lazy=True)
    photos = db.relationship('Photo', backref='listing',lazy=True)


    def __init__(self,street,city,postal_code,listing_type,lessor_id, num_rooms_available,ensuite,dist_to_wlu, dist_to_wloo,coed,price,num_rooms_total):
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.listing_type = listing_type
        self.lessor_id = lessor_id
        self.num_rooms_available = num_rooms_available
        self.ensuite = ensuite
        self.dist_to_wlu = dist_to_wlu
        self.dist_to_wloo = dist_to_wloo
        self.coed = coed
        self.price = price
        self.num_rooms_total = num_rooms_total
  
# Listing Schema - for marshmallow
class ListingSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('listing_id','street','city','postal_code','listing_type','lessor_id','num_rooms_available','ensuite','dist_to_wlu','dist_to_wloo','coed','price', 'num_rooms_total')

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
    dob = db.Column(db.DateTime)
    phone_num = db.Column(db.String(20))
    email = db.Column(db.String(100),unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    last_login = db.Column(db.DateTime)
    listings = db.relationship('Listing', backref='lessor',lazy=True)
    messages = db.relationship('Message', backref='lessor',lazy=True)

    def __init__(self,dob,phone_num,email,first_name,last_name,password,last_login):
        self.dob = dob
        self.phone_num = phone_num
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.last_login = last_login
  
# Lessor Schema - for marshmallow
class LessorSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('lessor_id','dob','phone_num','email','first_name','last_name','password','last_login')

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
    dob = db.Column(db.DateTime)
    phone_num = db.Column(db.String(20))
    email = db.Column(db.String(100),unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    last_login = db.Column(db.DateTime)
    num_rooms_available = db.Column(db.Integer)
    num_rooms_total = db.Column(db.Integer)
    ensuite = db.Column(db.Boolean)
    dist_to_wlu = db.Column(db.Integer)
    dist_to_wloo = db.Column(db.Integer)
    is_female = db.Column(db.Boolean)
    coed = db.Column(db.String(100))
    min_price = db.Column(db.Integer)
    max_price = db.Column(db.Integer)
    favourite_listings = db.relationship('Favourite_listing', backref='subletter',lazy=True)
    messages = db.relationship('Message', backref='subletter',lazy=True)

    def __init__(self,dob,phone_num,email,first_name,last_name,password,last_login,num_rooms_available,ensuite,dist_to_wlu,dist_to_wloo,is_female,coed,min_price,max_price,num_rooms_total):
        self.dob = dob
        self.phone_num = phone_num
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.last_login = last_login
        self.num_rooms_available = num_rooms_available
        self.ensuite = ensuite
        self.dist_to_wlu = dist_to_wlu
        self.dist_to_wloo = dist_to_wloo
        self.is_female = is_female
        self.coed = coed
        self.num_rooms_total = num_rooms_total
        self.min_price = min_price
        self.max_price = max_price
  
# Subletter Schema - for marshmallow
class SubletterSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('subletter_id','dob','phone_num','email','first_name','last_name','password','last_login','num_rooms_available','ensuite','dist_to_wlu','dist_to_wloo','is_female','coed','min_price','max_price','num_rooms_total')

# Initiate Subletter Schema
subletter_schema = SubletterSchema()
subletters_schema = SubletterSchema(many=True)

################################################################################################

# ENDPOINT - Create lessor account
@application.route('/create-lessor',methods=['PUT'])
def create_lessor():
    dob = request.json['dob']
    phone_num = request.json['phone_num']
    email = request.json['email']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    password = request.json['password']
    
    new_lessor = Lessor(dob,phone_num,email,first_name,last_name,password,datetime.now())

    db.session.add(new_lessor)
    db.session.commit()

    lessor_id = Lessor.query.filter_by(email = email).first().lessor_id
    response = {'response':lessor_id}

    return jsonify(response)
    
# ENDPOINT - Create subletter account
@application.route('/create-subletter',methods=['PUT'])
def create_subletter():
    dob = request.json['dob']
    phone_num = request.json['phone_num']
    email = request.json['email']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    password = request.json['password']
    last_login = request.json['last_login']
    num_rooms_available = request.json['num_rooms_available']
    ensuite = request.json['ensuite']
    dist_to_wlu = request.json['dist_to_wlu']
    dist_to_wloo = request.json['dist_to_wloo']
    is_female = request.json['is_female']
    coed = request.json['coed']
    num_rooms_total = request.json['num_rooms_total']
    min_price = request.json['min_price']
    max_price = request.json['max_price']
    
    new_subletter = Subletter(dob,phone_num,email,first_name,last_name,password,datetime.now(),num_rooms_available,ensuite,dist_to_wlu,dist_to_wloo,is_female,coed,min_price,max_price,num_rooms_total)

    db.session.add(new_subletter)
    db.session.commit()

    subletter_id = Subletter.query.filter_by(email = email).first().subletter_id
    response = {'response':subletter_id}

    return jsonify(response)
   
# ENDPOINT - Get all students
@application.route('/lessors-all',methods=['GET'])
def get_students():
    all_lessors = Lessor.query.all()
    result = lessors_schema.dump(all_lessors)
    return jsonify(result)

@application.route('/listings-all',methods=['GET'])
def get_listings():
    all_listings = Listing.query.all()
    result = listings_schema.dump(all_listings)
    return jsonify(result)

# ENDPOINT - LoginSubletter
@application.route('/loginSubletter', methods=['POST'])
def check_sub_login_creds():
    email = request.json['email']
    password = request.json['password']

    subletter = Subletter.query.filter_by(email=email, password=password).first()
    response = {"response":""}

    if bool(subletter) == True:
        response["response"] = str(subletter.subletter_id)
    else:
        response["response"] = "Invalid credentials."

    return jsonify(response)

# ENDPOINT - LoginLessor
@application.route('/loginLessor', methods=['POST'])
def check_les_login_creds():
    email = request.json['email']
    password = request.json['password']

    lessor = Lessor.query.filter_by(email=email, password=password).first()
    response = {"response":""}

    if bool(lessor) == True:
        response["response"] = str(lessor.subletter_id)
    else:
        response["response"] = "Invalid credentials."

    return jsonify(response)

#ENDPOINT - filter listings based on lessor's requirements
@application.route('/filter-listings', methods = ['GET'])
def filter_listing():
    listarray = np.array([])

    subletter = Subletter.query.get(1)
    listing = Listing.query.filter_by(ensuite=subletter.ensuite).all()
    for l in listing:
        if l.num_rooms_available >= subletter.num_rooms_available:
            if l.num_rooms_total == subletter.num_rooms_total:
                if l.dist_to_wloo <= subletter.dist_to_wloo:
                    if l.dist_to_wlu <= subletter.dist_to_wlu:
                        if l.price <= subletter.max_price:
                            if l.price >= subletter.min_price:
                                if subletter.coed == "either":
                                    if subletter.is_female == True:
                                        if l.coed != "men":
                                            listarray = np.append(listarray,[l.listing_id],axis=0)
                                            #listarray = np.append(listarray,[[l.street,l.city,l.postal_code,l.listing_type,l.num_rooms_available,l.num_rooms_total,l.ensuite,l.dist_to_wlu,l.dist_to_wloo,l.coed,l.price]], axis=0)
                                    else:
                                        if l.coed != "female":
                                            listarray = np.append(listarray,[l.listing_id],axis=0)
                                            #listarray = np.append(listarray,[[l.street,l.city,l.postal_code,l.listing_type,l.num_rooms_available,l.num_rooms_total,l.ensuite,l.dist_to_wlu,l.dist_to_wloo,l.coed,l.price]], axis=0)
                                if subletter.coed == "male":
                                    if l.coed == subletter.coed:
                                        listarray = np.append(listarray,[l.listing_id],axis=0)
                                        #listarray = np.append(listarray,[[l.street,l.city,l.postal_code,l.listing_type,l.num_rooms_available,l.num_rooms_total,l.ensuite,l.dist_to_wlu,l.dist_to_wloo,l.coed,l.price]], axis=0)
                                if subletter.coed == "female":
                                    if l.coed == subletter.coed:
                                        listarray = np.append(listarray,[l.listing_id],axis=0)
                                        #listarray = np.append(listarray,[[l.street,l.city,l.postal_code,l.listing_type,l.num_rooms_available,l.num_rooms_total,l.ensuite,l.dist_to_wlu,l.dist_to_wloo,l.coed,l.price]], axis=0)                
    #print(listarray)
    outlist = [[[[[[[[[[[]]]]]]]]]]]
    for i in range(len(listarray)):
        Final_listing = Listing.query.get(listarray[i-1])
        outlist.append([Final_listing.street,Final_listing.city,Final_listing.postal_code,Final_listing.listing_type,Final_listing.num_rooms_available,Final_listing.num_rooms_total,Final_listing.ensuite,Final_listing.dist_to_wlu,Final_listing.dist_to_wloo,Final_listing.coed,Final_listing.price])
    #lists = listarray.tolist()
    #json_str = json.dumps(lists)
    return jsonify(outlist)


#ENDPOINT - Create a listing
@application.route('/listing-create/<lessor_id>', methods=['POST'])
def add_listing(lessor_id):
    #create the listing with all the info that the lessor puts in
    #listing_id = request.json['listing_id'] #not included bc primary key
    street = request.json['street']
    city = request.json['city']
    postal_code = request.json['postal_code']
    listing_type = request.json['listing_type']
    lessor_id = lessor_id #request.json['lessor_id']
    #favourite_listings = request.json['favourite_listings']
    #photos = request.json['photo'] ### I think we should create a separate method that will take in photos at a later time/as a separate operation
    
    new_listing = Listing(street, city, postal_code, listing_type, lessor_id)

    db.session.add(new_listing)
    db.session.commit()

    return listing_schema.jsonify(new_listing)

#ENDPOINT - View Lessor's listings
@application.route('/<lessor_id>/listings', methods=['GET']) #this seems to work right now but need more data to test
def my_listing(lessor_id):
    #returns all the listings that belong to 1 lessor
    all_my_listings = Listing.query.filter_by(lessor_id = lessor_id)
    
    result = listings_schema.dump(all_my_listings)
    return jsonify(result)

#ENDPOINT - Display individual listing info
@application.route('/listings/<listing_id>', methods=['GET']) #this seems to work right now too but more data would help test this
def view_ind_listing(listing_id):
    listing = Listing.query.get(listing_id)
    #returns all the attributes of the selected listing id 
    return listing_schema.jsonify(listing)

# ENDPOINT - Get all messages between two users
@application.route('/get-messages',methods=['POST'])
def get_messages():
    subletter_id = request.json['subletter_id']
    lessor_id = request.json['lessor_id']
    all_messages = Message.query.filter_by(subletter_id=subletter_id, lessor_id=lessor_id).all()
    msgs = messages_schema.dump(all_messages)
    
    return jsonify(msgs)

# ENDPOINT- create and send a message
@application.route('/message-create', methods=['PUT'])
def add_message():
    subletter_id = request.json['subletter_id']
    lessor_id = request.json['lessor_id']
    text = request.json['text']
    lessor_sent = request.json['lessor_sent']
    now = datetime.utcnow()
    
 
    new_message = Message(lessor_id, subletter_id, text, str(now), lessor_sent)

    db.session.add(new_message)
    db.session.commit()

    return "your message was successfully sent"


# Run server
if __name__ == '__main__':
    # application.run(host='0.0.0.0')
    application.run(debug=True)