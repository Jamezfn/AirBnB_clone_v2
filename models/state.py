from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.city import City

class State(BaseModel, Base):
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="state", cascade="all, delete")

    @property
    def cities_list(self):
        city_list = []
        for city in models.storage.all("City").values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
