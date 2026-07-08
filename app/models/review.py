"""Module defining the Review class

Classed:
    Review(BaseModel)
"""
from .baseclass import BaseModel
from .user import User
from .place import Place
from .. import db


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
    __tablename__ = "reviews"
    text = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # def __init__(self, text, rating, place, user):
    #     super().__init__()
    #     self.text = text
    #     self.rating = rating
    #     self.place = place
    #     self.user = user

    # # Getters and setters ---------------------------------

    # # text ------------------

    # @property
    # def text(self):
    #     return self.__text

    # @text.setter
    # def text(self, text):
    #     if type(text) is not str:
    #         raise TypeError("text must be a string")
    #     if not 0 < len(text):
    #         raise ValueError("text must not be empty")
    #     self.__text = text

    # # rating ----------------

    # @property
    # def rating(self):
    #     return self.__rating

    # @rating.setter
    # def rating(self, rating):
    #     if type(rating) is not int:
    #         raise TypeError("rating must be an integer")
    #     if not 0 < rating <= 5:
    #         raise ValueError("rating must be between 1 and 5")
    #     self.__rating = rating

    # # place -----------------

    # @property
    # def place(self):
    #     return self.__place

    # @place.setter
    # def place(self, place):
    #     if type(place) is not Place:
    #         raise TypeError("place must be a Place")
    #     self.__place = place

    # # user ------------------

    # @property
    # def user(self):
    #     return self.__user

    # @user.setter
    # def user(self, user):
    #     if type(user) is not User:
    #         raise TypeError("user must be a User")
    #     self.__user = user
