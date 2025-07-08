#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
import models
from models.review import Review
from models.amenity import Amenity
from os import getenv

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(128))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", back_populates="place", cascade="all, delete")
        user = relationship("User", back_populates="places")
        amenities = relationship("Amenity", secondary=place_amenity, back_populates="place_amenities", viewonly=False)
    else:
        amenity_ids = []

        @property
        def reviews(self):
            """Getter attribute for reviews in FileStorage"""
            review_list = []
            review_objs = models.storage.all(Review)
            for review in review_objs.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Getter for amenities in FileStorage"""
            amenity_objs = models.storage.all(Amenity)
            return [amenity for amenity in amenity_objs.values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter attribute for amenities in FileStorage"""
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)

    def __init__(self, *args, **kwargs):
        """Initialize Place instance with default values for required fields"""
        super().__init__(*args, **kwargs)
        if 'max_guest' not in kwargs or kwargs['max_guest'] is None:
            self.max_guest = 0

        if 'price_by_night' not in kwargs or kwargs['price_by_night'] is None:
            self.price_by_night = 0
        if 'number_rooms' not in kwargs or kwargs['number_rooms'] is None:
            self.number_rooms = 0
        if 'number_bathrooms' not in kwargs or kwargs['number_bathrooms'] is None:
            self.number_bathrooms = 0
