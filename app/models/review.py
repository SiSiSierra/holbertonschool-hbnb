"""Module defining the Review class

Classed:
    Review(BaseModel)
"""
from . import BaseModel


class Review(BaseModel):
    """ Contains a review from a User about a Place

    Inherits:
        BaseModel

    Attributes:
        - id: string
        - text: string
        - rating: int
        - place_id: UUID
        - user_id: UUID
        - created_at: datetime
        - updated_at: datetime

    Functions:
    """

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    # Getters and setters ---------------------------------

    # text ------------------

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if type(text) is not str:
            raise TypeError("text must be a string")
        if not 0 < len(text):
            raise ValueError("text must not be empty")
        self.__text = text

    # rating ----------------

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

    # place_id -----------------

    @property
    def place_id(self):
        return self.__place_id

    @place_id.setter
    def place_id(self, place_id):
        if type(place_id) is not str:
            raise TypeError("place_id must be an ID string")
        self.__place_id = place_id

    # user_id ------------------

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        if type(user_id) is not str:
            raise TypeError("user_id must be an ID string")
        self.__user_id = user_id
