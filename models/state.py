from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
import os
from models.city import City

class State(BaseModel, Base):
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", back_populates="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """FS mode: return all City objs with this state's id."""
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id
                    ]
