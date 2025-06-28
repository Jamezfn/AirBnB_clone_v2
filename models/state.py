#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City

class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        """Getter attribute for cities in FileStorage"""
        city_list = []
        all_city = models.storage.all(City)
        for city in all_city.values:
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
