# Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker 
from sqlalchemy import create_engine, Column, Text, Integer, Date, Boolean, \
ForeignKey, case, func, join, text, extract
from datetime import datetime as dt
import numpy as np
import pandas as pd

# Init DB
engine = create_engine('sqlite:///database.db')
engine.connect() 
Base = declarative_base()

# Define Tables
class House(Base):
	__tablename__ = 'Houses'
	id = Column(Integer, primary_key = True)
	address = Column(Text)
	office_id = Column(Integer, ForeignKey('Offices.id'))
	agent_id = Column(Integer, ForeignKey('Agents.id'))
	seller_id = Column(Integer, ForeignKey('Customers.id'))    
	no_bedrooms = Column(Integer, nullable=False)
	no_bathrooms = Column(Integer, nullable=False)
	list_price = Column(Integer, nullable=False)
	zipcode = Column(Integer)
	list_date = Column(Date)
	sold = Column(Boolean)

class Customer(Base):
	__tablename__ = 'Customers'
	id = Column(Integer, primary_key = True)
	name = Column(Text)

class Office(Base):
	__tablename__ = 'Offices'
	id = Column(Integer, primary_key = True)
	address = Column(Text)

class Agent(Base):
	__tablename__ = 'Agents'
	id = Column(Integer, primary_key = True)
	name = Column(Text)
	handel = Column(Text)

class Sale(Base):
	__tablename__ = 'Sales'
	id = Column(Integer, primary_key = True)
	house_id = Column(Integer, ForeignKey('Houses.id'), index=True)
	buyer_id = Column(Integer, ForeignKey('Customers.id'), index=True)
	sale_price = Column(Integer, nullable=False, index = True)
	sale_date = Column(Date, index=True)
	sale_commission = Column(Integer)

# Create tables
Base.metadata.create_all(bind=engine)

# Add Sale
def sell_house(house, buyer, date):

	# Open Session
	Session = sessionmaker(bind=engine)
	session = Session()

	# Mark Sold
	house_row = session.query(House).filter(House.id == house)
	house_row.update({House.sold: True})

	# Calculate price and comission
	price = session.query(House.list_price).filter(House.id == house).first()[0]
	commission = session.query(House.list_price*case([
		(House.list_price < 100000, 0.01),
		(House.list_price < 200000, 0.075),
		(House.list_price < 500000, 0.06),
		(House.list_price < 1000000, 0.05),
		(House.list_price > 1000000, 0.04),])
	).filter(House.id == house).first()[0]

	# Add Sale
	session.add(Sale( 
		house_id = house,
		buyer_id = buyer,
		sale_price = price,
		sale_date = date,
		sale_commission = commission))

	# Commit Change and close session
	session.commit()
	session.close()

# Add Seed Data

# Open Session
Session = sessionmaker(bind=engine)
session = Session()

k_house = [column.key for column in House.__table__.c][1:]
v_house = [
['Giza', 1, 1, 1, 11, 1, 4500000, 14143, dt(2019, 4, 9),False],
['Rhodes', 2, 2, 2, 4, 2, 200003, 10001, dt(2019, 4, 3),False],
['Babylon', 3, 3, 2, 2, 3, 2220000, 20331, dt(2019, 3, 3),False],
['Alexandria', 4, 4, 3, 4, 2, 624000, 14143, dt(2018, 10, 5),False],
['Halicarnassus', 5, 4, 3, 5, 6, 35000, 94102, dt(2018, 3, 9),False],
['Olympia', 2, 5, 5, 1, 5, 1000, 10001, dt(101, 10, 1),False]]

k_customer = [column.key for column in Customer.__table__.c][1:]
v_customer = [['King Mansa Musa'], ['Jeff Bazos'], ['King Midas'],
['John D. Rockefeller'], ['Bill Gates'], ['Baron Rothschild']]

k_office = [column.key for column in Office.__table__.c][1:]
v_office = [['1600 Pennsylvania Avenue'],['10 Downing Street'],['350 Fifth Avenue'],
{'221 B Baker Street'},['30 Rockefeller Plaza'], ['5 Avenue Anatole']]

k_agent = [column.key for column in Agent.__table__.c][1:]
v_agent = [['James Bond','@007'],['Natasha Romanoff','@b_widow'],['Austin Powers','@groovybb'],
['Clarice Starling','@QuidFoSho'],['Fourty Seven','@hitman_official'],['Smith','@redpill']]

classes = [House,Customer,Office,Agent]
keys = [k_house, k_customer, k_office, k_agent]
values = [v_house, v_customer, v_office, v_agent]

for i in range(len(classes)):
	bundles = []
	for item in values[i]:
		items = dict(zip(keys[i], item))
		bundles.append(items)

		for bundle in bundles:
			session.add(classes[i](**bundle))


			session.commit()
			session.close()

			sell_house(1, 5, dt(2019, 4, 9))
			sell_house(2, 4, dt(2019, 4, 8))
			sell_house(3, 4, dt(2019, 4, 1))
			sell_house(4, 6, dt(2019, 2, 5))
			sell_house(5, 6, dt(2019, 1, 10))
			sell_house(6, 6, dt(207, 1, 1))