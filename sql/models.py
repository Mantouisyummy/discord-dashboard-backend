from sqlalchemy import Column, Integer, String

from .database import Base


class WelcomeMessage(Base):
    __tablename__ = "welcome_messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)
    channel = Column(Integer)
