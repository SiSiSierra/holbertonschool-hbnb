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
        + first_name: string
        + last_name: string
        + email: string
        + is_admin: boolean
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
