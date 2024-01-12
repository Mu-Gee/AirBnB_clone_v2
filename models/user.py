#!/usr/bin/python3
"""This is the user class"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class User(BaseModel, Base):
    """This is the class for user
    Attributes:
        email: email address
        password: password for you login
        first_name: first name
        last_name: last name
        places: relationship between a user and places
    """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    places = relationship(
        'Place', backref='user', cascade='all, delete-orphan'
    )
    reviews = relationship(
        'Review', backref='user', cascade='all, delete-orphan'
    )
