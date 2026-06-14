"""Defines the Place class

Classes:
    Place(BaseModel)
"""
from . import BaseModel


class Place(BaseModel):
    """ Represents a registered place in the app that can be rented

    Inherits:
        BaseModel

    Attributes:
        + id: string
        + title: string
        + description: string
        + price: float
        + latitude: float
        + longitude: float
        + owner: User
        + reviews: List(Review)
        + amenities: List(Amenity)
        + created_at: datetime
        + updated_at: datetime

    Functions:
        + add_review(self, review): void
        + add_amenity(self, review): void
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title # Up to 100 chars
        self.description = description
        self.price = price # > 0
        self.latitude = latitude # Between -90 and 90 inc.
        self.longitude = longitude # Between -180 and 180 inc.
        self.owner = owner # This MUST be validated!!!
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
