"Module for singleton"
from threading import Lock


class SingletonMixin(object):
    """Thread safe singleton mixin using double check pattern"""
    __singleton_lock = Lock()
    __singleton_instance = None

    def __init__(self):
        """Raised type error and warns that is a singleton"""
        if self.__singleton_instance:
            raise TypeError('Singletons must be accessed through `instance()`.')

    @classmethod
    def instance(cls):
        """Gets or instantiates the singleton"""
        if not cls.__singleton_instance:
            with cls.__singleton_lock: # # pylint: disable=E1129
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance
