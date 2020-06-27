from model.models import User, Address
from dao.database_connect import session


def get_user(u_id):
    user = session.query(User).get(u_id)
    return user


def add_user(u_id, first_name, last_name):
    session.add(User(u_id, first_name, last_name))
    session.commit()
