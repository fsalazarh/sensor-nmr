import logging
import time
import math
import numpy as np

from databases.database import Database
from models.peak import Peak
from models.noise import Noise

# import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta


class DataProcessor:
    """
    Handles information retrieving from microfone
    """
    def __init__(self, test_mode=False):
        self.test_mode = test_mode

    def process_data(self, check_time):
        peaks_last_min = Peak.find_last_min(check_time)
        if len(peaks_last_min) != 0:
            list = []
            for peak in peaks_last_min:
                list.insert(0,peak.peak_value)
            list.sort()
            return Noise(
                registered_at = check_time,
                peak = list[-1],
                var1 = sum(list[-(round(len(list)*0.01)+1):])/(round(len(list)*0.01)+1),
                var5 = sum(list[-(round(len(list)*0.05)+1):])/(round(len(list)*0.05)+1),
                var10 = sum(list[-(round(len(list)*0.1)+1):])/(round(len(list)*0.1)+1),
                avg = sum(list)/len(list)
            )
        else:
            return Noise()

    def process_data_peak(self, check_time):
        peaks_last_min = Peak.find_last_min(check_time)
        if len(peaks_last_min) != 0:
            list = []
            for peak in peaks_last_min:
                list.insert(0,peak.peak_value)
            peak_val = list[1]
            list.sort()
            return Noise(
                registered_at = check_time,
                peak = peak_val,
                var1 = sum(list[-(round(len(list)*0.01)+1):])/(round(len(list)*0.01)+1),
                var5 = sum(list[-(round(len(list)*0.05)+1):])/(round(len(list)*0.05)+1),
                var10 = sum(list[-(round(len(list)*0.1)+1):])/(round(len(list)*0.1)+1),
                avg = sum(list)/len(list)
            )
        else:
            return Noise()

    def convert_data(self):
        peaks = Peak.all()
        logging.info('Peaks saved: '+str(len(peaks)))
        if len(peaks) != 0:
            first_time = peaks[0].registered_at
            end_time = peaks[-1].registered_at
            time = first_time  - timedelta(minutes=-1+first_time.minute % 1,seconds=first_time.second,microseconds=first_time.microsecond)
            while time < end_time:
                noise = self.process_data(time)
                if noise.registered_at != None:
                    noise.save()
                time = time + timedelta(minutes=1)
            logging.info('ending converting')
        Peak.destroy_processed(time - timedelta(minutes=1))
