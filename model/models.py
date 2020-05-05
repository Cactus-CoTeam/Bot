from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from database_connect import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    addresses = relationship("Address", backref=backref("address", cascade="all,delete"))

    def __init__(self, name):
        self.name = name


class Address(Base):
    __tablename__ = 'address'

    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    city = Column(String)
    street = Column(String)
    home = Column(String)

    def __init__(self, user_id, city, street, home):
        self.user_id = user_id
        self.city = city
        self.street = street
        self.home = home
