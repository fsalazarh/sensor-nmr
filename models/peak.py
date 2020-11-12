"""Module for measure"""
from sqlalchemy import Column, DateTime, Float, and_

from databases.database import Database
from models.mixins import CRUDMixin

from datetime import timedelta

class Peak(Database.instance().Base, CRUDMixin):
    """Model for measures table
    """
    __tablename__ = 'peaks'

    registered_at = Column(DateTime, primary_key=True) # este id es del smartcitizen no del sensor
    peak_value = Column(Float)

    @classmethod
    def find_last_min(cls,time):
        """Search setting by name"""
        session = Database.instance().session()
        return session.query(Peak).filter(and_(Peak.registered_at>time+timedelta(minutes=-1),Peak.registered_at<=time)).all()

    @classmethod
    def destroy_processed(cls,time):
        """Search setting by name"""
        session = Database.instance().session()
        session.query(Peak).filter(Peak.registered_at<=time+timedelta(minutes=-1)).delete()
        session.commit()
