from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'usuarios_douglas'

    index = Column(Integer, primary_key=True)
    login = Column(String(100), unique=True)
    senha = Column(String(100))
    email = Column(String(100))
    UID = Column(Text)
    totp_secret = Column(String(32)) 
    
    def get_id(self):
        return str(self.index)
