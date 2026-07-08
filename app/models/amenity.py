"""Module defining the Amenity class

Classes:
    Amenity(BaseModel)
"""
from .baseclass import BaseModel
from .. import db
from sqlalchemy.orm import relationship
from .association_table import place_amenity


class Amenity(BaseModel):
    """Pre-defined items that can be added to Places

    Inherits:
        BaseModel

    Attributes:
        + id: string
        + name: string
        + created_at: datetime
        + updated_at: datetime

    Functions:
    """
    __tablename__ = "amenities"
    name = db.Column(db.String(128), nullable=False)
    place_association = relationship('Place', secondary=place_amenity, lazy='subquery', backref=db.backref('amenities', lazy=True))

    # def __init__(self, name):
    #     super().__init__()
    #     self.name = name

    # @property
    # def name(self):
    #     return self.__name

    # @name.setter
    # def name(self, name):
    #     if type(name) is not str:
    #         raise TypeError("name must be a string")
    #     if len(name) > 50:
    #         raise ValueError("name cannot be longer than 50 characters")
    #     self.__name = name
