"""Module for measure"""
from sqlalchemy import Column, DateTime, Float

from databases.database import Database
from models.mixins import CRUDMixin


class Noise(Database.instance().Base, CRUDMixin):
    """Model for measures table
    """
    __tablename__ = 'noises'

    registered_at = Column(DateTime, primary_key=True) # este id es del smartcitizen no del sensor
    peak = Column(Float)
    var1 = Column(Float)
    var5 = Column(Float)
    var10 = Column(Float)
    avg = Column(Float)
    synchronized_at = Column(DateTime)

    @classmethod
    def find_unsynchronized(cls):
        """Search setting by name"""
        session = Database.instance().session()
        return session.query(Noise).filter(Noise.synchronized_at==None)

    @classmethod
    def find_synchronized(cls):
        """Search setting by name"""
        session = Database.instance().session()
        return session.query(Noise).filter(Noise.synchronized_at!=None)

    @classmethod
    def destroy_synchronized(cls):
        """Search setting by name"""
        session = Database.instance().session()
        session.query(Noise).filter(Noise.synchronized_at!=None).delete()
        session.commit()
