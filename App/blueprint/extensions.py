from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
#from .models import New_app

ma = Marshmallow()
#Creating an instance of Limiter
limiter = Limiter(key_func=get_remote_address)#this use to get the address of whoever keeps sending request to the server
cache = Cache()
