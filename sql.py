"""
Run this to view the Users table of the Database

"""

import sqlalchemy as db
engine = db.create_engine('sqlite:///data.db') 
connection = engine.connect()
metadata = db.MetaData()
data = db.Table('users', metadata, autoload=True, autoload_with=engine)
query = db.select([data])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(len(ResultSet))
print(ResultSet)
