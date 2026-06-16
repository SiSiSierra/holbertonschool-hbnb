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
        + add_amenity(self, amenity): void
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title  # Up to 100 chars
        self.description = description
        
        # Initialize private backing attributes for our properties
        self._price = 0.0
        self._latitude = 0.0
        self._longitude = 0.0
        
        # Assigning via the properties below automatically triggers validation on init
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        
        self.owner = owner
        self.reviews = []
        self.amenities = []

    # --- PRICE PROPERTIES & VALIDATION ---
    @property
    def price(self):
        """Getter for price"""
        return self._price

    @price.setter
    def price(self, value):
        """Setter for price with validation rules (> 0)"""
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError("Price must be a valid number.")
        if val < 0:
            raise ValueError("Price must be a non-negative float.")
        self._price = val

    # --- LATITUDE PROPERTIES & VALIDATION ---
    @property
    def latitude(self):
        """Getter for latitude"""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Setter for latitude with validation rules (-90 to 90)"""
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a valid number.")
        if not (-90.0 <= val <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0 inclusive.")
        self._latitude = val

    # --- LONGITUDE PROPERTIES & VALIDATION ---
    @property
    def longitude(self):
        """Getter for longitude"""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Setter for longitude with validation rules (-180 to 180)"""
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a valid number.")
        if not (-180.0 <= val <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0 inclusive.")
        self._longitude = val

    # --- RELATIONSHIP MANAGEMENT INTERFACES ---
    def add_review(self, review):
        """Appends a new review instance to the place tracking log"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Appends a new amenity instance to the place configuration array"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
