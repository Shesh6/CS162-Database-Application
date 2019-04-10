# CS162 Assignment 2 - Database Application

###Run Guide:
**setup.py** contains the database initialization, table specification and seed data insertion.
**run.py** contains the queries required for the assignment, and prints them.
```
python3.6 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt

python3 setup.py
python3 run.py
```
### Highlights

Transactions are used in the seed data insertion, even though it's expected to run once, on a single system, with little risk of complication.
In a professional environments, any changes to the tables should be wrapped inside sessions, so that if clashes arise the system can roll back to resolve issues. I implemented a function to register a sale, which inserts and updates information in several tables and is bound to be used often, in order to abstract the operation for users of the system. That function has a built in commit command, to enforce the use of transactions.

The database is normalized according to the third normal form:
- **1NF**: Atomic, domain-relevant, unique, order-independent
- **2NF**: No partial dependency: No attribute can be determined without entire primary key
- **3NF**: No transitive dependency: No attribute depends on any other but the primary key

Queries are made primarily on primary key ID numbers set to autoincrement with additions, to reduce the need for indices.
Other queries often rely on attirbutes of sales, such as date and price, which follow a sequential structure that's likely to be used for comparisons. These therefore are indexed, to reduce search complexity.