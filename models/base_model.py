#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models

class BaseModel:
    """A base class for all hbnb models"""
    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if kwargs:
            valid_keys = {'id', 'created_at', 'updated_at', '__class__'}
            for key, value in kwargs.items():
                if key not in valid_keys:
                    raise KeyError(f"Invalid key: {key}")
                if key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != '__class__':
                    setattr(self, key, value)
            self.id = getattr(self, 'id', str(uuid.uuid4()))
            self.created_at = getattr(self, 'created_at', datetime.now())
            self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        models.storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({})'.format(cls, self.id)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
