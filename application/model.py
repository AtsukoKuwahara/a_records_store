from application import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Document):
    user_id     =   db.IntField( unique=True )
    first_name  =   db.StringField( max_length=50 )
    last_name   =   db.StringField( max_length=50 )
    email       =   db.StringField( max_length=30, unique=True )
    password    =   db.StringField( )
    role        =   db.StringField(default='user')  # Field for user role

    def set_password(self, password):
        """
        Sets the password for the user by hashing it.
        :param password: Plain text password
        """
        self.password = generate_password_hash(password)

    def get_password(self, password):
        """
        Checks if the provided password matches the stored hashed password.
        :param password: Plain text password
        :return: Boolean indicating if the password matches
        """
        return check_password_hash(self.password, password) 

class Product(db.Document):
    product_id  =   db.IntField( unique=True )
    title       =   db.StringField( max_length=50 )
    artist      =   db.StringField( max_length=50 )
    label       =   db.StringField( max_length=50 )
    price       =   db.FloatField( )
    image_url   =   db.StringField(default='static/image/placeholder.png')  # Default image URL

    def save(self, *args, **kwargs):
        self.price = round(float(self.price), 2)
        return super(Product, self).save(*args, **kwargs)

class RecordOfTheWeek(db.Document):
    product_id  =   db.IntField()
    message     =   db.StringField( max_length=2000 )
    created_at  =   db.DateTimeField(default=datetime.datetime.utcnow)
    image_url   =   db.StringField()  # URL of the uploaded image

class Order(db.Document):
    user_id     = db.IntField()
    product_id  = db.IntField()
    quantity    = db.IntField()
    is_order    = db.BooleanField()

class TriviaArchive(db.Document):
    product_id  = db.IntField()
    title       = db.StringField(max_length=200)
    artist      = db.StringField(max_length=200)
    trivia      = db.StringField(max_length=2000)
    created_at  = db.DateTimeField(default=datetime.datetime.utcnow)
    message     = db.StringField(max_length=2000)  # Message from the record of the week