from model.models import User, Address
from dao.database_connect import session


def get_user(user_id):
    user = session.query(User).get(user_id)
    return user


def add_user(user_name):
    session.add(User(user_name))
