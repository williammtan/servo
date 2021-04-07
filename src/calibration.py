import cv2
import pygame
import time
import json
import os
import sys

from ui import UICallibrate
from face_detection import FaceDetection
from serial_transmitter import SerialTransmitter
from _json import Json

class Calibration:
    def __init__(self, mode=None):
        self.servo_pos = (90, 90)
        self.allow_save = True
        
        self.json = Json('settings.json')
        self.settings = self.json.get_json()

        if mode == 'debug': self.serial_transmitter = SerialTransmitter(arduino_connect=False)
        else: self.serial_transmitter = SerialTransmitter(arduino_connect=True, move_threshold=0.05)
        self.ui = UICallibrate(self.settings, (640, 480), move_factor=0.5)
        self.face_detection = FaceDetection()

        self.calibrate()

    def calibrate(self):
        running = True
        while running:
            img = self.face_detection.get_img()
            change = self.ui.update(img, self.servo_pos)
            self.change_servo_pos(change)
            self.update_settings()

            # Allow save will ensure they can only save after they let go of the save button
            if self.ui.save and self.allow_save:
                # Write to json *and* set allow save to false
                self.write_json()
                self.allow_save = False
            else:
                # set allow save to true
                self.allow_save = True
                

            self.serial_transmitter.move(self.servo_pos)
            self.log()
            time.sleep(0.01)
    
    def log(self):
        # delete and rewrite all setting and pos data
        os.system('clear')
        log_text = f"""
        Pos: {self.servo_pos}
        Settings: {self.settings}
        """
        print(log_text)
    
    def change_servo_pos(self, change):
        # Convert change and change servo pos
        if self.settings['x_flipped']:
            change = (-change[0], change[1])
        if self.settings['y_flipped']:
            change = (change[0], -change[1])
        new_servo_pos = (self.servo_pos[0]+change[0], self.servo_pos[1]+change[1])

        # if new_servo_pos is valid
        if not ((new_servo_pos[0] > 180 or new_servo_pos[0] < 0) or (new_servo_pos[1] > 180 or new_servo_pos[1] < 0)):
            # update servo_pos
            self.servo_pos = (self.servo_pos[0] + change[0], self.servo_pos[1] + change[1])
        else:
            # do nothing
            pass
    
    def update_settings(self):
        self.settings['camera_fov']['y'] = self.ui.settings['max']['top'] - self.ui.settings['max']['bottom']
        self.settings['camera_fov']['x'] = self.ui.settings['max']['right'] - self.ui.settings['max']['left']

        self.settings['x_flipped'] = self.ui.settings['x_flipped']
        self.settings['y_flipped'] = self.ui.settings['y_flipped']


    def write_json(self):
        self.json(self.settings)

if __name__ == '__main__':
    try: mode = sys.argv[1]
    except IndexError: mode = None
    calibration = Calibration(mode=mode)