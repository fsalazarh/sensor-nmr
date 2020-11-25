"""Module for synchronizers"""
import logging
from pathlib import Path

from models.peak import Peak
from synchronization.request_handler import RequestHandler

class BaseSynchronizer():
    """Base sync class"""
    def __init__(self):
        self.request_handler = RequestHandler()
        self._is_authenticated = False

    def authenticate(self):
        self._is_authenticated = self.request_handler.authenticate()

class DriveSynchronizer(BaseSynchronizer):
    """Synchronizer for peak values to drive
    """
    def synchronize(self):
        """Check for unsynchronized peak values on the database an gives them to Google Drive"""
        self.request_handler.post_peak()


class BigQuerySynchronizer(BaseSynchronizer):
    def synchronize(self):
        self.request_handler.post_peak_big_query()