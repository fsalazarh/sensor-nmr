"""Module for database"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, Float, String, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool, StaticPool

from utils.singleton import SingletonMixin


class Database(SingletonMixin):
    """Represents a database instance using singleton pattern"""
    def __init__(self):
        super(Database, self).__init__()
        self.engine = create_engine(
            'sqlite:///local.db',
            connect_args={'check_same_thread': False, 'timeout':10},
            poolclass=QueuePool)
        self.engine_test = create_engine(
            'sqlite://',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool)
        self.Session = None
        self.Base = declarative_base()
        self.validators = {
            Integer: self.validate_int,
            Float: self.validate_float,
            String: self.validate_string,
            Boolean: self.validate_boolean,
            DateTime: self.validate_datetime,
        }

    def set_session(self, test_mode=False):
        """Sets the session to be used, must be called at the program startup"""
        if not test_mode: # pragma: no cover
            self.Session = scoped_session(sessionmaker(bind=self.engine))
            return
        self.Session = scoped_session(sessionmaker(bind=self.engine_test))


    def session(self):
        """Obtains the current scopped session to work on"""
        return self.Session()

    # Base validation for datatypes
    def validate_int(self, value):
        """Validates if the value is an integer instance"""
        if value is not None:
            if isinstance(value, str):
                value = int(value)
            else:
                assert isinstance(value, int)
        return value

    def validate_float(self, value):
        """Validates if the value is a float instance"""
        if value is not None:
            if isinstance(value, str):
                value = float(value)
            else:
                assert isinstance(value, (int,float))
        return value

    def validate_string(self, value):
        """Validates if the value is a string instance"""
        if value is not None:
            assert isinstance(value, str)
        return value


    def validate_boolean(self, value):
        """Validates if the value is a boolean instance"""
        if value is not None:
            assert isinstance(value, bool)
        return value


    def validate_datetime(self, value):
        """Validates if the value is a datetime instance"""
        if value is not None:
            assert isinstance(value, datetime)
        return value

@event.listens_for(Database.instance().Base, 'attribute_instrument')
def configure_listener(class_, key, inst): # pylint: disable=W0613
    """Configures a listener to validate automatically the types"""
    if not hasattr(inst.property, 'columns'):  # pragma: no cover
        return
    @event.listens_for(inst, "set", retval=True)
    def set_(instance, value, oldvalue, initiator): # pylint: disable=W0612, W0613
        """Sets the validators for each type"""
        validator = Database.instance().validators.get(inst.property.columns[0].type.__class__)
        if validator:
            return validator(value)
        return value  # pragma: no cover
