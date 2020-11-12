"""Module for thread manager"""
import logging
import time
from datetime import datetime
from threading import Thread

from utils.formatter import format_miliseconds
from utils.singleton import SingletonMixin


class ThreadManager(SingletonMixin):
    """A singleton class that manages all threads running the application,
    it has a pool of threads that can be safely-stopped at any time,
    the pool its not shared across threads
    """
    def __init__(self):
        super(ThreadManager, self).__init__()
        self.thread_pool = {}

    def add_thread(self, name, method, sleep_time=None):
        """Adds a new thread to the pool
        param :name: Name of the thread
        param :name: Method to tbe runned by the thread
        """
        if name in self.thread_pool:
            del self.thread_pool[name]
        self.thread_pool[name] = ThreadSafe(name, method, sleep_time)

    def start_thread(self, name):
        """
        Starts a thread from the pool
        param :name: Name of the thread
        """
        try:
            self.thread_pool[name].start()
        except Exception as error:
            logging.error('Unable to start service ' + name + ' the following error ocurred' +
                          str(error))
            print('Unable to start service ' + name + ' the following error ocurred' +
                  str(error))

    def stop_thread(self, name):
        """Stops a thread from the pool
        param :name: Name of the thread"""
        self.thread_pool[name].stop()

    def stop_all(self):
        """Stops all threads running"""
        for thread_name in self.thread_pool:
            self.stop_thread(thread_name)

    def thread_exist(self, name):
        """
        Verifies if there is a thread initiated with the given name
        param : name: Name of the thread
        """
        return name in self.thread_pool


    def is_thread_alive(self, name):
        """Verifies if the thread is running"""
        if name in self.thread_pool:
            return self.thread_pool[name].is_alive()
        return False

    def status(self):
        """Obtains a string detailing the status of all threads"""
        if not self.thread_pool:
            return 'The are currently no services running'
        status = ''
        for thread_name in self.thread_pool:
            status += self.thread_pool[thread_name].status() + '\n'
        return status

    def stopped_manually(self, name):
        """Verifies that the corresponding thread was stoppped manually"""
        if name in self.thread_pool:
            return self.thread_pool[name].stopped_manually()
        return False


    def exception(self, name):
        """Obtains the last exception thrown by the given thread"""
        if name in self.thread_pool:
            return self.thread_pool[name].exception
        return None


class ThreadSafe():
    """A Wrapper class that will run a thread indefinitly
    param :name: Name of the thread
    param :name: Method to te runned by the thread
    """
    def __init__(self, name, method, sleep_time):
        self.name = name
        self.method = method
        self.keep_running = True
        self.thread = Thread(target=self.run, name=name)
        self.sleep_time = sleep_time
        self.exception = None

    def start(self):
        """Starts the thread"""
        self.thread.start()

    def stop(self):
        """Stops the thread"""
        self.keep_running = False

    def is_alive(self):
        """Checks if the thread is alive"""
        return self.thread.isAlive()

    def stopped_manually(self):
        """Verify whether the thread was stopped manually or not"""
        return self.exception is None

    def status(self):
        """Obtain the status of the proccess"""
        status = ''
        if self.keep_running:
            status += ('Service ' + self.name + ' is running correctly with ' +
                       format_miliseconds(self.sleep_time))
        else:
            status += 'Service ' + self.name + ' is not running '
            if self.exception:
                status += 'it was stopped by the following error: ' + str(self.exception)
            else:
                status += 'it was stopped manually by an user'
        return status

    def run(self):
        """Wrapper for looping the thread until asked to stop"""
        while self.keep_running:
            try:
                self.method()
            except Exception as error:
                self.exception = error
                self.keep_running = False
                print('Service', self.name, 'stopped at ', str(datetime.utcnow()),
                      'by the following error:', str(error))
                logging.error('Service ' + self.name + ' error: ' + str(error))
            if self.sleep_time:
                time.sleep(self.sleep_time)
