# importing Modules
from os import name
import datetime
import telegram
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
        self.signup_time = signup_time
        self.lastseen = lastseen

    def __repr__(self):
        return "<User {} ({})>".format(self.user_id, self.username)
        

# User Tables
class Chats(BASE):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(UnicodeText)
    chat_id = Column(Integer)
    admins = Column(UnicodeText)
    signup_time = Column(UnicodeText)
    lastseen = Column(UnicodeText)

    def __init__(self, title, chat_id, admins, signup_time, lastseen):
        self.chat_id = chat_id
        self.title = title
        self.admins = admins
        self.signup_time = signup_time
        self.lastseen = lastseen



# Creating Tables
Users.__table__.create(checkfirst=True)
Chats.__table__.create(checkfirst=True)

# Defining Functions For DB
def DB_Updater(update, context):
    # Fetching Details with update
    if update.effective_chat.type == "private":
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
    else:
        f = str(update.effective_chat.title)
        c = int(update.effective_chat.id)
        a = get_admins(update, context)
        s = str(datetime.datetime.now())
        if is_regular_chat(c):
            chat_last_seen = get_last_seen_chat(c) 
            update_chat_data(f, c, a, s)
        else:
            insert_chat_data(f, c, a, s)

def insert_user_data(f, l, c, u, s):
    user_data = Users(first_name = f, last_name = l,user_id = c, username = u, signup_time = s, lastseen = s )
    SESSION.add(user_data)
    SESSION.commit()

def insert_chat_data(f, c, a, s):
    chat_data = Chats(title = f, chat_id = c, admins = a, signup_time = s, lastseen = s )
    SESSION.add(chat_data)
    SESSION.commit()

def update_chat_data(f, c, a, s):
    chat_data = SESSION.query(Chats).filter_by(chat_id= c).first()
    chat_data.title = f 
    chat_data.chat_id = c
    chat_data.admins = a
    chat_data.lastseen = s 
    SESSION.commit()


def is_regular_chat(c):
    chat_data = SESSION.query(Chats).filter_by(chat_id= c).first()
    print( '___',chat_data)
    if str(chat_data) == 'None':
        return False
    else:
        return True

def get_last_seen_chat(c):
    chat_data = SESSION.query(Chats).filter_by(chat_id= c).first()
    return chat_data.lastseen

def update_user_data(f, l, c, u, s):
    user_data = SESSION.query(Users).filter_by(user_id= c).first()
    user_data.first_name = f 
    user_data.last_name = l
    user_data.user_id = c
    user_data.username = u 
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

def get_members(update, context):
    members = update.effective_chat

def get_admins(update, context):
        administrators = context.bot.getChatAdministrators(update.effective_chat.id)
        text = "{\n"
        for admin in administrators:
            user = admin.user
            text += '"'+ str(user.id) + '",\n'
        text += "}"
        print (text)
        return text

def fetch_groups_allowed(update):
    user_id = update.effective_user.id
    groups = SESSION.query(Chats).filter(Chats.admins.like('%"'+ str(user_id) +'"%')).all()
    for group in groups:
        group.chat_id

SESSION.commit()
SESSION.close()

