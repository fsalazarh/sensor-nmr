import logging
import time
import math
import numpy as np


from databases.database import Database
from models.peak import Peak

# import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta


class AudioRetriever:
    """
    Handles information retrieving from microfone
    """
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.recorder_device = None
        self.channels = 1 # mono
        self.sample_rate = 44100 # Hz
        self.frames = 2**12 # samples per buffer
        self.audio = None
        self.stream = None
        self.recording = None
        self.decoded_recording = None
        self.filtered_recording = None

    def is_recorder_device_ready(self):
        return True

    def noise_peak(self):
        '''
        Peak value (but its a short rms in reality)
        '''
        time.sleep(self.frames/self.sample_rate)
        return np.random.randint(1,120)

    def retrieve_audio(self):
        """
        Function that streams audio and store noise data
        """
        peak = Peak(
            registered_at=datetime.utcnow(),
            peak_value=self.noise_peak()
        )
        peak.save()

    def stop_audio(self):
        self.stream = None
