from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "a super secret, secret key" #This key will only be valid for things in your web alone and nobody else will have it

def encode_token(member_id): #we use user id because it is unique and will make our tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta (days=0, hours=1), #This sets the expiration time to an hour past now
        'iat': datetime.now(timezone.utc), #This is when it was issued
        'sub': str(member_id) #Always make sure that this is a string 
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f) #The donuts sprinkler
    def decorated(*args, **kwargs):
        token = None

        #Make sure your route is in an Authorized header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1] #The server normally returns beares and tokens but we are only after our token, hence the split function
            if not token:
                return jsonify({"Message": "Missing token"}) #returns error message if token is not given
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print(data)
                member_id = data['sub']
            except ExpiredSignatureError as e:
                return jsonify({"Message": "Token Expired"}), 400
            except JWTError as e:
                return jsonify({"Message": "Invalid Token"}), 400
            return f(member_id, *args, **kwargs)
        else:
            return jsonify({"Message": "You must be logged in to access this"})
    return decorated