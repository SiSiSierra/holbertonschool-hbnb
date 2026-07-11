"""Module defining User class

Classes:
    User(BaseModel)
"""
from .baseclass import BaseModel
import re
from .. import bcrypt, db
import uuid
from sqlalchemy.orm import relationship, validates



class User(BaseModel):
    """A User represents a person's account on the app, and can create\
reviews and places

    Inherits:
        * BaseModel

    Attributes:
        - id: string
        - first_name: string
        - last_name: string
        - email: string
        - password:
        - is_admin: boolean
        - created_at: datetime
        - updated_at: datetime

    Functions:
        + hash_password(self, password)
        + verify_password(self, password)
"""
    # Setup SQLAlchemy Table -----------------------
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    place_child = relationship('Place', backref='owner', lazy=True)
    review_child = relationship('Review', backref='user', lazy=True)

    # Validators -----------------------------
    @validates("first_name")
    def validate_first_name(self, key, name):
        if not 0 < len(name) <= 50:
            raise ValueError(
                "first_name must be between 1 and 50 characters long"
            )
        return name
        
    @validates("last_name")
    def validate_last_name(self, key, name):
        if not 0 < len(name) <= 50:
            raise ValueError(
                "last_name must be between 1 and 50 characters long"
            )
        return name

    # Password hashing and comparison ---------------------

    def hash_password(self, password):
        """Hash the password using Bcrypt before storing"""
        self.password = \
            bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Compare provided password with stored password by hashing"""
        return bcrypt.check_password_hash(self.password, password)


    # def __init__(self, first_name, last_name, email, password, is_admin=False):
    #     super().__init__()
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.password = password
    #     self.is_admin = is_admin

    # # Getters and setters ---------------------------------

    # # first_name ------------

    # @property
    # def first_name(self):
    #     return self.__first_name

    # @first_name.setter
    # def first_name(self, first_name):
    #     if type(first_name) is not str:
    #         raise TypeError("first_name must be a string")
    #     if not 0 < len(first_name) <= 50:
    #         raise ValueError(
    #                 "first_name must be between 1 and 50 characters long"
    #                 )
    #     self.__first_name = first_name

    # # last_name -------------

    # @property
    # def last_name(self):
    #     return self.__last_name

    # @last_name.setter
    # def last_name(self, last_name):
    #     if type(last_name) is not str:
    #         raise TypeError("last_name must be a string")
    #     if not 0 < len(last_name) <= 50:
    #         raise ValueError(
    #                 "last_name must be between 1 and 50 characters long"
    #                 )
#        self.__last_name = last_name

    # email -----------------

#    @property
#    def email(self):
#        return self.__email

#    @email.setter
#    def email(self, email):
#        if type(email) is not str:
#            raise TypeError("email must be a string")
#        if not 0 < len(email):
#            raise ValueError("email must not be empty")
#        # Validate e-mail format
#        valid_email_regex = \
#            '^(\\w|\\.|\\_|\\-)+[@](\\w|\\_|\\-|\\.)+[.]\\w{2,3}$'
#        if not re.search(valid_email_regex, email):
#            raise ValueError("email must be in a valid e-mail format")
#        self.__email = email

    # is_admin --------------

#    @property
#    def is_admin(self):
#        return self.__is_admin

#    @is_admin.setter
#    def is_admin(self, is_admin):
#        if type(is_admin) is not bool:
#            raise TypeError("is_admin must be a boolean")
#        self.__is_admin = is_admin

    # password --------------

#    @property
#    def password(self):
#        return self.__password

#    @password.setter
#    def password(self, password):
#        self.hash_password(password)
