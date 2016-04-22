from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_restaurants():
    """Query all the restaurants and return the results in ascending
       alphabetical order.
    """
    return session.query(Restaurant).order_by(Restaurant.name)


def get_restaurant(id):
    """Gets a restaurant by its id.
    """
    return session.query(Restaurant).filter_by(id=id).one()


def insert_restaurant(name):
    """Inserts a restaurant into the database with the passed name.
    """
    session.add(Restaurant(name=name))
    session.commit()


def update_restaurant(id, name):
    """Update restaurant with the passed id to have the passed name.
    """
    restaurant = get_restaurant(id)
    restaurant.name = name
    session.add(restaurant)
    session.commit()


def delete_restaurant(id):
    """Delete restaurant with the passed id.
    """
    restaurant = get_restaurant(id)
    session.delete(restaurant)
    session.commit()
