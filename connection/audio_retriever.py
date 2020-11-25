import logging
import pyaudio
import wave
import time
import math
import numpy as np

from scipy.signal import butter,filtfilt
import RPi.GPIO as gpio

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
        self.format = pyaudio.paInt16
        self.channels = 1 # mono
        self.sample_rate = 44100 # Hz
        self.frames = 2**12 # samples per buffer
        self.audio = None
        self.stream = None
        self.recording = None
        self.decoded_recording = None
        self.filtered_recording = None
        self.b,self.a = self.design_filter(20,20000)
        gpio.setmode(gpio.BOARD)
        gpio.setup(11, gpio.OUT) # R
        gpio.setup(13, gpio.OUT) # G
        gpio.setup(15, gpio.OUT) # V
        gpio.setup(16, gpio.OUT) # ON/OFF

    def is_recorder_device_ready(self):
        self.audio = pyaudio.PyAudio()
        for device in range(self.audio.get_device_count()):
            if ('mems-mic' in self.audio.get_device_info_by_index(device).get('name') or
                'Input' in self.audio.get_device_info_by_index(device).get('name')):
                self.recorder_device = device
                self.stream = stream = self.audio.open(format = self.format,rate = self.sample_rate, \
                channels = self.channels, input_device_index = self.recorder_device, \
                input = True, frames_per_buffer=self.frames)
                return True
        return False

    def noise_peak(self, sound_buffer):
        '''
        Peak value (but its a short rms in reality)
        '''
        peak = 0
        length = len(sound_buffer)
        for value in sound_buffer:
            peak += (value/(2**16/2))**2
        return 20*math.log10((peak/length)**(1/2))

    def design_filter(self, lowcut, highcut, order=3):
        nyq = 0.5*self.sample_rate
        low = lowcut/nyq
        high = highcut/nyq
        b,a = butter(order, [low,high], btype='band')
        return b,a

    def retrieve_audio(self):
        """
        Function that streams audio and store noise data
        """
        recording = self.stream.read(self.frames, exception_on_overflow = False)
        self.decoded_recording = np.fromstring(recording, dtype=np.int16)
        self.filtered_recording = filtfilt(self.b, self.a, self.decoded_recording)
        peak = Peak(
            registered_at=datetime.utcnow(),
            peak_value=self.noise_peak(self.filtered_recording)+105
        )
        peak.save()

    def stop_audio(self):
        self.stream.stop_stream()
        while not self.stream.is_stopped():
            self.stream.close()
