"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for,redirect
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS,cross_origin
from utils import APIException, generate_sitemap, send_sms
from models import db,User,Hero,Incident,Service
from twilio.twiml.messaging_response import MessagingResponse
import requests
from flask_jwt_simple import create_jwt,JWTManager,decode_jwt,jwt_required


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")  # Change this!
jwt = JWTManager(app)

# validation with JWT
# @app.before_request
# def checkjwt():
#     not_protected=["/hero/login","/user/login"]
#     token=request.cookies.get("token")
#     if request.path not in not_protected and token is not None:
#         decoded=decode_jwt(token)
#         return get_jwt_identity()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.after_request
def after_request(response):
    header=response.headers
    header['Access-Control-Allow-Origin']="*"
    return response
# post and get methods for User
@app.route('/user', methods=['POST','GET'])
@cross_origin()
def handle_createread():
    if request.method=='POST':
        body = request.get_json()

        if body is None:
            raise APIException ("You need to specify the request body as a json object ", status_code=400)
        if "first_name" not in body:
            raise APIException ("You need to specify first name", status_code=400)
        if "last_name" not in body:
            raise APIException ("You need to specify last name", status_code=400)
        if "email" not in body:
            raise APIException ("You need to specify email", status_code=400)
        if "password" not in body:
            raise APIException ("You need to specify password", status_code=400)
        if "phone" not in body:
            raise APIException ("You need to specify phone number", status_code=400)
        if "share_phone" not in body:
            raise APIException ("You need to specify share_phone", status_code=400)

        user1=User(first_name=body["first_name"],last_name=body["last_name"],email=body["email"],password=body["password"],phone=body["phone"],share_phone=body["share_phone"])
        db.session.add(user1)
        db.session.commit()
        return "created successfully", 200

    else:
        user2=User.query.all()
        alluser=list(map(lambda x: x.serialize(),user2))
        return jsonify(alluser),200

# put and delete methods for User
@app.route('/user/<id>',methods=['PUT','DELETE'])
@cross_origin()
# @jwt_required
def handle_updatedelete(id):
    if request.method=='PUT':
        obj1=User.query.get(id)
        newobj=request.get_json()
        if "first_name" in newobj:
            obj1.first_name=newobj["first_name"]
        if "last_name" in newobj:
            obj1.last_name=newobj["last_name"]
        if "email" in newobj:
            obj1.email=newobj["email"]
        if "password" in newobj:
            obj1.password=newobj["password"]
        if "phone" in newobj:
            obj1.phone=newobj["phone"]
        if "share_phone" in newobj:
            obj1.share_phone=newobj["share_phone"]
    
        db.session.merge(obj1)
        db.session.commit()
        return "updated successfully",200

    else:
        deleteone=User.query.get(id)
        db.session.delete(deleteone)
        db.session.commit()
        return "deleted successfully",200

# Login end point for User      
@app.route('/user/login',methods=['POST'])
@cross_origin()
def handle_userlogin():
    item=request.get_json()

    if item is None:
        raise APIException ("You need to specify the request body as a json object ", status_code=400)
    if "email" not in item:
        raise APIException ("You need to specify email", status_code=400)
    if "password" not in item:
        raise APIException ("You need to specify password", status_code=400)

    allitems=User.query.filter(User.email==item["email"],User.password==item["password"]).first()

    if allitems is None:
        return "your email or password is incorrect",401
    else:
        usertoken=create_jwt(identity=allitems.email)
        usertoken1={"key":usertoken}
        usertoken2=jsonify(usertoken1)
        # usertoken2.set_cookie("usertoken",usertoken,secure=True)
        return usertoken2,200

# post and get methods for Hero
@app.route('/hero',methods=['POST','GET'])
@cross_origin()
def createandread():
    if request.method=='POST':
        herodata1=request.get_json()

        if herodata1 is None:
            raise APIException ("You need to specify the request body as a json object ", status_code=400)
        if "first_name" not in herodata1:
            raise APIException ("You need to specify first name", status_code=400)
        if "last_name" not in herodata1:
            raise APIException ("You need to specify last name", status_code=400)
        if "email" not in herodata1:
            raise APIException ("You need to specify email", status_code=400)
        if "password" not in herodata1:
            raise APIException ("You need to specify password", status_code=400)
        if "zip_code" not in herodata1:
            raise APIException ("You need to specify zipcode", status_code=400)    
        if "phone" not in herodata1:
            raise APIException ("You need to specify phone number", status_code=400)
        if "share_phone" not in herodata1:
            raise APIException ("You need to specify share_phone", status_code=400)

        herodata2=Hero(first_name=herodata1["first_name"],last_name=herodata1["last_name"],email=herodata1["email"],password=herodata1["password"],zip_code=herodata1["zip_code"],phone=herodata1["phone"],share_phone=herodata1["share_phone"])
        db.session.add(herodata2)
        db.session.commit()
        return "posted it",200

    else:
        herodata3=Hero.query.all()
        herodata4=list(map(lambda x: x.serialize(),herodata3))
        print(herodata4)
        return jsonify(herodata4),200

# put and delete methods for Hero
@app.route('/hero/<id>',methods=['PUT','DELETE'])
@cross_origin()
# @jwt_required
def updateanddelete(id):
    if request.method=='PUT':
        herodata5=Hero.query.get(id)
        herodata6=request.get_json()

        if "first_name" in herodata6:
            herodata5.first_name=herodata6["first_name"]
        if "last_name" in herodata6:
            herodata5.last_name=herodata6["last_name"]
        if "email" in herodata6:
            herodata5.email=herodata6["email"]
        if "password" in herodata6:
            herodata5.password=herodata6["password"]
        if "zip_code" in herodata6:
            herodata5.zip_code=herodata6["zip_code"]
        if "phone" in herodata6:
            herodata5.phone=herodata6["phone"]
        if "share_phone" in herodata6:
            herodata5.share_phone=herodata6["share_phone"]

        db.session.merge(herodata5)
        db.session.commit()
        return "modified it",200

    else:
        herodata7=Hero.query.get(id)
        db.session.delete(herodata7)
        db.session.commit()
        return "deleted it",200

# Login end point for Hero
@app.route('/hero/login',methods=['POST'])
@cross_origin()
def handle_heroplogin():
    herobody=request.get_json() 

    if herobody is None:
        raise APIException ("You need to specify the request body as a json object ", status_code=400)
    if "email" not in herobody:
        raise APIException ("You need to specify email", status_code=400)
    if "password" not in herobody:
        raise APIException ("You need to specify password", status_code=400)

    heroobj=Hero.query.filter(Hero.email==herobody["email"],Hero.password==herobody["password"]).first()

    if heroobj is None:
        return "your email or password is incorrect"
    else:
        token=create_jwt(identity=heroobj.email)
        tokendata={'key':token}
        jsontoken=jsonify(tokendata)
        # jsontoken.set_cookie("token",token,secure=True)
        return jsontoken,200

# post method for Service
@app.route('/service',methods=['POST'])
@cross_origin()
# @jwt_required
def handle_service():
    service1=request.get_json()

    if service1 is None:
        raise APIException ("You need to specify the request body as a json object ", status_code=400)
    if "servicetype_name" not in service1:
        raise APIException ("You need to specify servicetype_name", status_code=400)

    sercice2=Service(servicetype_name=service1["servicetype_name"])
    db.session.add(sercice2)
    db.session.commit()
    return "services created successfully"

# post method for Incident 
@app.route('/incident',methods=['POST','OPTIONS'])
# @jwt_required
def handle_incident():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    firststep=request.get_json()
    print(firststep)
    print(firststep["email"])
    secondstep=User.query.filter(User.email==firststep["email"]).first()
    thridstep=Service.query.filter(Service.servicetype_name==firststep["servicetype_name"]).first()
    fourthstep=Incident(user_id=secondstep.user_id,servicetype_id=thridstep.servicetype_id,latitude=firststep["latitude"],longitude=firststep["longitude"])
    db.session.add(fourthstep)
    db.session.commit()
# getting a User's zipcode by using latitude & longitude
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json",params={'latlng':firststep["latitude"]+','+firststep["longitude"],'key':'AIzaSyDnPdnUPzUc0NaVzp4hS6Y_dhPSE8rvK1s'})
    response1=response.json()
    list1=response1["results"][0]["address_components"]
    postal_code = None
    for obj in list1:
        if obj["types"][0]=="postal_code":
            postal_code = obj["long_name"]
    print(postal_code)
    if postal_code is not None:
        # its time to send the sms to everyone at this postal code
        heros_nearby = Hero.query.filter(Hero.zip_code==postal_code)
        for _hero in heros_nearby:
            print(_hero)
            send_sms("Hello "+_hero.first_name+", someone needs your help! please reply with "+str(fourthstep.incident_id)+" if you are willing to help", _hero.phone)
            return "success"
            
@app.route('/incident/response',methods=['POST'])
def receive_test_sms(): 
    incoming_message_content = request.values.get('Body', None)
    incoming_number = request.values.get('From', None)
    print(incoming_number)
    print(incoming_message_content)
    gettingheroobj=Hero.query.filter(Hero.phone==incoming_number).first()
    print(gettingheroobj.hero_id)
    newone=Incident.query.filter(Incident.incident_id==int(incoming_message_content)).first()
    print(newone.hero_id)
    newone.hero_id=gettingheroobj.hero_id
    db.session.merge(newone)
    db.session.commit()
    resp=MessagingResponse()
    userdetail=User.query.filter(User.user_id==newone.user_id).first()
    resp.message("Thank you,here's a user's details..\nFirst Name:"+userdetail.first_name+"\nPhone No:"+userdetail.phone+"\nhttp://maps.google.com/?q="+str(newone.latitude)+','+str(newone.longitude))
    return str(resp),200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
