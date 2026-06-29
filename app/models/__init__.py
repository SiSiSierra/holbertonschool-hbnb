""" Module defining abstract BaseModel for other models
to inherit

Classes:
    BaseModel(ABC)
"""
import uuid
from datetime import datetime
from abc import ABC


class BaseModel(ABC):
    """ Abstract Class BaseModel

    Attributes:
        - id: String
        - created_at: datetime
        - updated_at: datetime

    Functions:
        + save(self): void
        + update(self, data): void
    """

    def __init__(self):
        self.__id = str(uuid.uuid4())
        self.__created_at = datetime.now()
        self.__updated_at = datetime.now()

    @property
    def id(self):
        return self.__id

    @property
    def created_at(self):
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    # ---------------------------------

    def save(self):
        """Set updated_at to current time after self is modified"""
        self.__updated_at = datetime.now()

    def update(self, data):
        """Set self's attributes to given new values

        Params:
            data: Dictionary of attribute: value pairs
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
