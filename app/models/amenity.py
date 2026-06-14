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
