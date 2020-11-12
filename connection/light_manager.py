import logging
import time
import math
import numpy as np

import RPi.GPIO as gpio

from databases.database import Database
from connection.data_processor import DataProcessor
from models.noise import Noise

# import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time


class LightManager:
    """
    Handles information retrieving from microfone
    """
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.begin_hour = time(7,30)
        self.end_hour = time(16,0)
        self.led_status = ""
        gpio.setmode(gpio.BOARD)
        gpio.setup(11, gpio.OUT) # B
        gpio.setup(13, gpio.OUT) # R
        gpio.setup(15, gpio.OUT) # G

    def rgb_set(self):
        school_time = datetime.utcnow()
        check_time = school_time + timedelta(hours=-4)
        if (check_time.time() >= self.begin_hour and check_time.time() <= self.end_hour):
            noise = DataProcessor().process_data_peak(school_time)
            if self.led_status != "on":
                self.led_status = "on"
                logging.info('LED: on')
            if noise.registered_at != None:
                if noise.peak >= 80:
                    #red
                    gpio.output(11, False)
                    gpio.output(13, True)
                    gpio.output(15, False)
                else:
                    if noise.avg < 55:
                        #green
                        gpio.output(11, False)
                        gpio.output(13, False)
                        gpio.output(15, True)
                    elif noise.avg < 80:
                        #yellow, R+G
                        gpio.output(11, False)
                        gpio.output(13, True)
                        gpio.output(15, True)

        else:
            if self.led_status != "off":
                self.led_status = "off"
                logging.info('LED: off')
            # OFF
            gpio.output(11, False)
            gpio.output(13, False)
            gpio.output(15, False)
