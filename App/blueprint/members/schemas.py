#All schemas you work with is created here
from App.blueprint.models import Member
from App.blueprint.extensions import ma

#Creating the Schema
class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
    #using the SQLAlchemy model to create the fields used in serialization, deserialization, and validation
        model = Member #This schema validates the above member class
member_schema = MemberSchema() #allow you to serialize a single member object
members_schema = MemberSchema(many=True) #allow you to serialize a list of member object
login_schema = MemberSchema(exclude = ['name', 'DOB']) #This enable your login route not to required name of date of birth when logging in, instead they require the rest in our case password and email
