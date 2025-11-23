#This holds the route for the CRUD information
from App.blueprint.members import members_bp
from App.blueprint.members.schemas import member_schema, members_schema, login_schema
from App.blueprint.models import Member, db
from sqlalchemy import select
from marshmallow import ValidationError 
from App.blueprint.extensions import limiter, cache
from App.utils.util import encode_token, token_required
from flask import request, jsonify

#Creating Login session
@members_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json) #This is requesting the email and password from the user and adding it to credentials   
        email = credentials['email'] #gets the email that was passed to the credentials
        password = credentials['password'] #get the password that was passed to credentials earlier
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Member).where(Member.email==email) #checking if the save email in your db is the same as the one given by the user
    member = db.session.execute(query).scalars().first()

    if member and member.password==password: #if you have a valid user that is associated to a password and you have said password stored in your database
        token = encode_token(member.id) #then assign a token to them. The user is a member that is save in your database

        #Then give the user a response
        response = {
            "status": "Success",
            "Message": "Successfully Logged In",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"Message": "Invalid email or password"})


#Create a member
@members_bp.route("/", methods=['POST'])
@limiter.limit("5 per day")
def create_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Member).where(Member.email == member_data['email']) #Checking our db for a member with this email
    existing_member = db.session.execute(query).scalars().all()
    if existing_member:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201

#Retrieving all Users
@members_bp.route("/", methods=['GET'])
#@limiter.limit("3 per hour") #A client can only attempt to make 3 users per hour
@cache.cached(timeout=30)
def get_members():
    query = select(Member)
    members = db.session.execute(query).scalars().all()

    return members_schema.jsonify(members)

#Retrieving a specific User
@members_bp.route("/<int:member_id>", methods=['GET'])
def get_member(member_id):#pass a parameter here which is the id for a specific member
    member = db.session.get(Member, member_id)#you already have the id as a param so just get it directly with both the member and its path param

    if member:
        return member_schema.jsonify(member), 200
    return jsonify({"error": "Member not found."}), 404

#Update a member infor ie: Member(PUT)
@members_bp.route("/<int:member_id>", methods=['PUT'])
@limiter.limit("5 per month") #You are only allow to update your account 5 per month
def update_member(member_id):
    member = db.session.get(Member, member_id) #path parameter to get the data

    #check if said member exist
    if not member:
        return jsonify({"error": "Member not found."})
    
    #Validate the data before updating
    try:
        member_data = member_schema.load(request.json)
    except ValueError as e:
        return jsonify(e.message), 400
    
    for key, value in member_data.items():
        setattr(member, key, value)

    db.session.commit()#use this becuase an edit is being added to a database
    return member_schema.jsonify(member), 200


#Delete a Specific Member
@members_bp.route("/", methods=['DELETE'])
@limiter.limit("5 per day") #YOu can only limit 5 members per day
@token_required
def delete_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error": "Member not found"}), 404
    
    db.session.delete(member)
    db.session.commit()
    return jsonify({"Message": f'Member id: {member_id}, successfully deleted.'}), 200
