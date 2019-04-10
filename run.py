# Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker 
from sqlalchemy import create_engine, Column, Text, Integer, Date, Boolean, \
                       ForeignKey, case, func, join, text, extract
from datetime import datetime as dt
import numpy as np
import pandas as pd

# Query 1
print("Find the top 5 offices with the most sales for that month:")
sales_count = func.count(House.office_id).label("Sales")
q1 = session.query(
	House.office_id,
	Office.address,
	sales_count
	).join(Office).filter(House.sold == True)\
	.group_by(House.office_id)\
	.order_by(sales_count.desc())\
	.limit(5)

print(pd.read_sql(q1.statement, session.bind))

# Query 2
print("Find the top 5 estate agents who have sold the most:")
agent_sale_count = func.count(House.agent_id).label('Sales')
q2 = session.query(
	Agent.id,
	Agent.name,
	Agent.handel,
	agent_sale_count
	).join(House).filter(House.sold == True)\
	.group_by(Agent.id)\
	.order_by(agent_sale_count.desc()).\
	limit(5)

print(pd.read_sql(q2.statement, session.bind))

# Query 3
print("Calculate the commission that each estate agent must receive:")
total_coms = func.sum(Sale.sale_commission).label('Commission')
q3 = session.query(
	Agent.name,
	total_coms
	).join(House,House.agent_id == Agent.id)\
	.join(Sale, Sale.house_id == House.id)\
	.group_by(Agent.id)

print(pd.read_sql(q3.statement, session.bind))

# Query 4
print("For all houses that were sold that month, calculate the average number of days that the house was on the market:")
# Used raw input due to limited datetime functionality in SQLAlchemy
q4 = text("""SELECT Houses.address, 
	Houses.list_date, 
	Sales.sale_date, 
	julianday(Sales.sale_date)- julianday(Houses.list_date)
	AS "Days on Market"
	FROM Houses 
	JOIN Sales ON Houses.id == Sales.house_id
	WHERE strftime('%m', Sales.sale_date)==strftime('%m',CURRENT_TIMESTAMP)""")

print(pd.read_sql(q4, session.bind))

# Query 5
print("For all houses that were sold that month, calculate the average selling price:")
avg_price = func.avg(Sale.sale_price).label('Average Price')
q5 = session.query(
	avg_price)\
	.filter(extract('month', Sale.sale_date) == dt.today().month)

print(pd.read_sql(q5.statement, session.bind))

# Query 6
print("Find the zip codes with the top 5 average sales prices:")
avg_price = func.avg(Sale.sale_price).label('Average Price')
q6=session.query(
	House.zipcode,
	avg_price
	).join(Sale). \
filter(House.sold == True)\
.group_by(House.zipcode)\
.order_by(avg_price.desc()).limit(5)

print(pd.read_sql(q6.statement, session.bind))