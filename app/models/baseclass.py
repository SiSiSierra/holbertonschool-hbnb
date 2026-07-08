"""Module defining the Base class

Classes:
    BaseModel(db.Model)
"""
from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True # No table made in SQLAlchemy

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
