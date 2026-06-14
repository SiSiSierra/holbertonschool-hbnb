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
        + id: string
        + text: string
        + rating: int
        + place: Place
        + user: User
        + created_at: datetime
        + updated_at: datetime

    Functions:
    """

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text # Up to 50 chars
        self.rating = rating # 1-5
        self.place = place # This MUST be validated!!
        self.user = user # This MUST be validated!!
