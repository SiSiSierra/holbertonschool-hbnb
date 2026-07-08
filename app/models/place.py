"""Defines the Place class

Classes:
    Place(BaseModel)
"""
from .baseclass import BaseModel
from .user import User
from .amenity import Amenity
from .. import db
from sqlalchemy.orm import relationship
from .association_table import place_amenity


class Place(BaseModel):
    """ Represents a registered place in the app that can be rented

    Inherits:
        BaseModel

    Attributes:
        - id: string
        - title: string
        - description: string
        - price: float
        - latitude: float
        - longitude: float
        - owner: User
        - reviews: List(Review)
        - amenities: List(Amenity)
        - created_at: datetime
        - updated_at: datetime

    Functions:
        + add_review(self, review): void
        + add_amenity(self, amenity): void
    """
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    review_child = relationship('Review', backref='places', lazy=True)
    amenity_association = relationship('Amenity', secondary=place_amenity, lazy='subquery', backref=db.backref('places', lazy=True))


    # def __init__(self, title, description, price, latitude, longitude, owner):
    #     super().__init__()
    #     self.title = title  # Up to 100 chars
    #     self.description = description

    #     # Initialize private backing attributes for our properties
    #     self._price = 0.0
    #     self._latitude = 0.0
    #     self._longitude = 0.0

    #     # Assigning via the properties below automatically
    #     # triggers validation on init
    #     self.price = price
    #     self.latitude = latitude
    #     self.longitude = longitude

    #     self.owner = owner
    #     self.__reviews = []
    #     self.__amenities = []

    # # --- TITLE PROPERTIES & VALIDATION ---
    # @property
    # def title(self):
    #     return self.__title

    # @title.setter
    # def title(self, title):
    #     if type(title) is not str:
    #         raise TypeError("title must be a string")
    #     if not 0 < len(title) <= 100:
    #         raise ValueError("title must be between 1 and 100 characters long")
    #     self.__title = title

    # # --- DESCRIPTION PROPERTIES & VALIDATION ---
    # @property
    # def description(self):
    #     return self.__description

    # @description.setter
    # def description(self, description):
    #     if type(description) is not str:
    #         raise TypeError("description must be a string")
    #     self.__description = description

    # # --- PRICE PROPERTIES & VALIDATION ---
    # @property
    # def price(self):
    #     """Getter for price"""
    #     return self.__price

    # @price.setter
    # def price(self, value):
    #     """Setter for price with validation rules (> 0)"""
    #     try:
    #         val = float(value)
    #     except (TypeError, ValueError):
    #         raise ValueError("Price must be a valid number.")
    #     if val < 0:
    #         raise ValueError("Price must be a non-negative float.")
    #     self.__price = val

    # # --- LATITUDE PROPERTIES & VALIDATION ---
    # @property
    # def latitude(self):
    #     """Getter for latitude"""
    #     return self.__latitude

    # @latitude.setter
    # def latitude(self, value):
    #     """Setter for latitude with validation rules (-90 to 90)"""
    #     try:
    #         val = float(value)
    #     except (TypeError, ValueError):
    #         raise ValueError("Latitude must be a valid number.")
    #     if not (-90.0 <= val <= 90.0):
    #         raise ValueError(
    #                 "Latitude must be between -90.0 and 90.0 inclusive."
    #                 )
    #     self.__latitude = val

    # # --- LONGITUDE PROPERTIES & VALIDATION ---
    # @property
    # def longitude(self):
    #     """Getter for longitude"""
    #     return self.__longitude

    # @longitude.setter
    # def longitude(self, value):
    #     """Setter for longitude with validation rules (-180 to 180)"""
    #     try:
    #         val = float(value)
    #     except (TypeError, ValueError):
    #         raise ValueError("Longitude must be a valid number.")
    #     if not (-180.0 <= val <= 180.0):
    #         raise ValueError(
    #                 "Longitude must be between -180.0 and 180.0 inclusive."
    #                 )
    #     self.__longitude = val

    # # --- OWNER PROPERTIES AND VALIDATION ---
    # @property
    # def owner(self):
    #     return self.__owner

    # @owner.setter
    # def owner(self, owner):
    #     self.__owner = owner

    # # --- REVIEWS PROPERTIES ---
    # @property
    # def reviews(self):
    #     return self.__reviews

    # # --- AMENITIES PROPERTIES ---
    # @property
    # def amenities(self):
    #     return self.__amenities

    # # --- RELATIONSHIP MANAGEMENT INTERFACES ---
    # def add_review(self, review):
    #     """Appends a new review instance to the place tracking log"""
    #     self.reviews.append(review)

    # def add_amenity(self, amenity):
    #     """Appends a new amenity instance to the place configuration array"""
    #     if amenity not in self.amenities:
    #         self.amenities.append(amenity)
