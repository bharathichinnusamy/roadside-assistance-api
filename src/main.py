"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db,User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['POST', 'GET'])
def handle_user():
    if request.method == 'POST':
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

        return "ok", 200
    
    elif request.method=="GET":
        user2=User.query.all()
        alluser=list(map(lambda x: x.serialize(),user2))
        return jsonify(alluser),200

    return "Invalid Method", 404


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
