"""Mixins for models module"""
from databases.database import Database


class CRUDMixin():
    """Mixing for CRUD operations"""

    @classmethod
    def all(cls):
        """Return all records"""
        session = Database.instance().session()
        return session.query(cls).all()

    @classmethod
    def find(cls, _id):
        """Find the record by id"""
        if _id is None:
            return None
        return Database.instance().session().query(cls).get(_id)

    def save(self):
        """Saves the new element on the database"""
        session = Database.instance().session()
        if self.find(self.registered_at) is None:
            session.add(self)
        session.commit()

    @classmethod
    def destroy(cls):
        """Destroys the elements from the database"""
        session = Database.instance().session()
        session.query(cls).delete()
        session.commit()
