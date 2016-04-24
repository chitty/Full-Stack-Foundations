from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Puppy

from datetime import date
from dateutil.relativedelta import relativedelta

engine = create_engine('sqlite:///puppyshelter.db')

DBSession = sessionmaker(bind=engine)

session = DBSession()


def get_puppies():
    """Query all of the puppies and return the results in ascending
       alphabetical order.
    """
    print "Puppies in ascending alphabetical order"
    puppies = session.query(Puppy).order_by(Puppy.name)
    for puppy in puppies:
        print puppy.name


def get_young_puppies():
    """Gets all of the puppies that are less than 6 months old organized by
       the youngest first.
    """
    print "Puppies 6 months old and younger"
    six_months_ago = date.today() + relativedelta(months=-6)
    puppies = session.query(Puppy).filter(Puppy.dateOfBirth >= six_months_ago).order_by(Puppy.dateOfBirth.desc())
    for puppy in puppies:
        print puppy.name+": "+str(puppy.dateOfBirth)


def get_puppies_weight():
    """Query all puppies by ascending weight"""
    print "Puppies in ascending weight"
    puppies = session.query(Puppy).order_by(Puppy.weight.asc())
    for puppy in puppies:
        print puppy.name+": "+str(puppy.weight)


def get_puppies_by_shelter():
    """Query all puppies and the shelter in which they are staying"""
    print "Puppies and the shelter they belong to"
    puppies = session.query(Puppy).order_by(Puppy.shelter_id)
    for puppy in puppies:
        print puppy.name+": "+str(puppy.shelter.name)


get_puppies()
get_young_puppies()
get_puppies_weight()
get_puppies_by_shelter()
