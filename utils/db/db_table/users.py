from sqlalchemy import Column, BigInteger, String

from utils.db.gino_shell_for_ORM_sqlalchemy import TimedBaseModel


class Users(TimedBaseModel):
    __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True)
    full_name = Column(String(128), nullable=False)
    user_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=True)
