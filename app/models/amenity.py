"""Module defining the Amenity class

Classes:
    Amenity(BaseModel)
"""
from . import BaseModel


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

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) is not str:
            raise TypeError("name must be a string")
        if len(name) > 50:
            raise ValueError("name cannot be longer than 50 characters")
        self.__name = name
