"""Module defining the Review class

Classed:
    Review(BaseModel)
"""
from . import BaseModel
from .user import User
from .place import Place

class Review(BaseModel):
    """ Contains a review from a User about a Place

    Inherits:
        BaseModel

    Attributes:
        - id: string
        - text: string
        - rating: int
        - place: Place
        - user: User
        - created_at: datetime
        - updated_at: datetime

    Functions:
    """

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating # 1-5
        self.place = place # This MUST be validated!!
        self.user = user # This MUST be validated!!

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if type(text) is not str:
            raise TypeError("text must be a string")
        self.__text = text

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, rating):
        if type(rating) is not int:
            raise TypeError("rating must be an integer")
        if not 0 < rating <= 5:
            raise ValueError("rating must be between 1 and 5")
        self.__rating = rating

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, place):
        if type(place) is not Place:
            raise TypeError("place must be a Place")
        self.__place = place

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        if type(user) is not User:
            raise TypeError("user must be a User")
        self.__user = user
