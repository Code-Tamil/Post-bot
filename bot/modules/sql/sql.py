# importing Modules
from os import name
import datetime
from sqlalchemy.sql.functions import user
from bot import dispatcher
from bot.modules.sql import BASE, SESSION
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
    UniqueConstraint,
    func
)

# Defining Tables
# User Tables
class Users(BASE):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(UnicodeText)
    last_name = Column(UnicodeText)
    user_id = Column(Integer)
    username = Column(UnicodeText)
    signup_time = Column(UnicodeText)
    lastseen = Column(UnicodeText)

    def __init__(self, first_name, last_name, user_id, username, signup_time, lastseen):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.username = username
        self.signup_time = signup_time
        self.lastseen = lastseen

    def __repr__(self):
        return "<User {} ({})>".format(self.user_id, self.username)
        

# Creating Tables
Users.__table__.create(checkfirst=True)


# Defining Functions For DB
def DB_Updater(update):
    # Fetching Details with update
    f = str(update.effective_user.first_name)
    l = str(update.effective_user.last_name)
    c = int(update.effective_user.id)
    s = str(datetime.datetime.now())
    u = str(update.effective_user.username)

    if is_regular_user(c):
        user_last_seen = get_last_seen(c)
        update_user_data(f, l, c, u, s)
        return 'Welcome you Again\nLast Seen you by <pre>' + user_last_seen + '</pre>'
    else:
        insert_user_data(f, l, c, u, s)
        return ''

def insert_user_data(f, l, c, u, s):
    user_data = Users(first_name = f, last_name = l,user_id = c, username = u, signup_time = s, lastseen = s )
    SESSION.add(user_data)
    SESSION.commit()

def update_user_data(f, l, c, u, s):
    user_data = SESSION.query(Users).filter_by(user_id= c).first()
    user_data.first_name = f 
    user_data.last_name = l
    user_data.user_id = c
    user_data.username = u 
    user_data.signup_time = s
    user_data.lastseen = s 
    SESSION.commit()

def get_last_seen(c):
    user_data = SESSION.query(Users).filter_by(user_id= c).first()
    return user_data.lastseen

def is_regular_user(c):
    user_data = SESSION.query(Users).filter_by(user_id= c).first()
    print( '___',user_data)
    if str(user_data) == 'None':
        return False
    else:
        return True

SESSION.commit()
SESSION.close()

