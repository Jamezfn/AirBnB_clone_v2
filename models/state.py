#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import models
from models.city import City

class State(BaseModel):q
    """ State class """
    __tablename__ = 'states'


    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all, delete-orphan')
    @property
    def cities(self):
        """ Retrieves a list of City instances associated with this state.

        Returns:
            list: List of City instances related to this state.
        """
        if models.storage_type == "db":
            return [city for city in models.storage.all(City).values() if city.state_id == self.id]
        else:
            return [city for city in models.storagr.all(City).values() if city.state_id = self.id]
