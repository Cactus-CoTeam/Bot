from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from dao.database_connect import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    addresses = relationship("Address", backref=backref("addresses", cascade="all,delete"))

    def __init__(self, u_id, first_name, last_name):
        self.id = u_id
        self.first_name = first_name
        self.last_name = last_name


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    city = Column(String)
    street = Column(String)
    home = Column(String)

    def __init__(self, user_id, city, street, home):
        self.user_id = user_id
        self.city = city
        self.street = street
        self.home = home
