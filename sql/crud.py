from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert

from . import models
from .database import create_session


def get_welcome(guild_id: int) -> models.WelcomeMessage:
    seesion = create_session()
    return seesion.query(models.WelcomeMessage).filter(models.WelcomeMessage.id == guild_id).first()

def upsert_welcome_message(guild_id: int, message: str = "", channel: int = 0):
    session = create_session()
    session.add(models.WelcomeMessage(id=guild_id, message=message, channel=channel))
    session.commit()

    return 'Success'

def update_welcome_message(guild_id: int, message: str, channel: str):
    payload = {
        "message": message,
        "channel": channel
    }

    session = create_session()

    session.query(models.WelcomeMessage).filter(models.WelcomeMessage.id == guild_id).update(payload, synchronize_session=False)

    session.commit()

    return payload
