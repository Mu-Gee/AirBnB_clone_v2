#!/usr/bin/python3
"""This is the place class"""
import os

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel


place_amenity_table = Table(
    'place_amenity', Base.metadata,
    Column(
        'place_id', String(60), ForeignKey('places.id'),
        nullable=False, primary_key=True
    ),
    Column(
        'amenity_id', String(60), ForeignKey('amenities.id'),
        nullable=False, primary_key=True
    ),
)


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            'Review', backref='place', cascade='all, delete-orphan'
        )
        amenities = relationship(
            'Amenity', secondary=place_amenity_table, viewonly=False
        )
    else:
        @property
        def amenities(self):
            """Get a list of amenities associated with this place
            Return:
                return a list of all Amenity instances with a place_id matching
                the id of the current Place
            """
            keys = map('Amenity.{}'.format, self.amenity_ids)
            instances = models.storage.all(models.amenity.Amenity)
            return [instances[key] for key in keys]

        @amenities.setter
        def amenities(self, value):
            """Associate an amenity with this place
            """
            if type(value) is models.amenity.Amenity:
                self.amenity_ids.append(value.id)

        @property
        def reviews(self):
            """Get a list of reviews associated with this place
            Return:
                return a list of all Review instances with a place_id matching
                the id of the current Place
            """
            instances = models.storage.all(models.review.Review)
            return [review for review in instances.values()
                    if review.place_id == self.id]
