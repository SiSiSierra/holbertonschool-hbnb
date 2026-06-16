"""Module defining User class

Classes:
    User(BaseModel)
"""
from . import BaseModel


class User(BaseModel):
    """A User represents a person's account on the app, and can create\
            reviews and places
    
    Inherits:
        BaseModel
    
    Attributes:
        + id: string
        - first_name: string
        - last_name: string
        - email: string
        - is_admin: boolean
        + created_at: datetime
        + updated_at: datetime

    Functions:
"""
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        if type(first_name) is not str:
            raise TypeError("first_name must be a string")
        if len(first_name) > 50:
            raise ValueError("first_name cannot exceed 50 characters")
        self.__first_name = first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        if type(last_name) is not str:
            raise TypeError("last_name must be a string")
        if len(last_name) > 50:
            raise ValueError("last_name cannot exceed 50 characters")
        self.__last_name = last_name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if type(email) is not str:
            raise TypeError("email must be a string")
        self.__email = email

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        if type(is_admin) is not bool:
            raise TypeError("is_admin must be a boolean")
        self.__is_admin = is_admin
