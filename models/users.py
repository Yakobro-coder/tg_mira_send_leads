

from sqlalchemy import Column, Integer, Table
from sqlalchemy.orm import declarative_base
from data_base import get_metadata
Base = declarative_base()
metadata = get_metadata()


class Users(Base):
    # __tablename__ = 'bot_mira_users'
    # id = db.Column(db.Integer, primary_key=True)
    # telegram_id = db.Column(db.Integer, unique=True, nullable=False)
    # crm_id = db.Column(db.Integer, unique=True, nullable=False)
    # username = db.Column(db.String)
    # first_name = db.Column(db.String)
    # last_name = db.Column(db.String)
    # email = db.Column(db.String)
    __table__ = Table('bot_mira_users', metadata, Column("id", Integer, primary_key=True), autoload=True)

    def __json__(self):
        return dict(
            id=self.id,
            telegram_id=self.telegram_id,
            crm_id=self.crm_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email
        )
