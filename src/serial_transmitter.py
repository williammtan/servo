import serial
import time

class SerialTransmitter:
    def __init__(self,arduino_connect=True , move_threshold=1, verbose=False):
        self.arduino_connect = arduino_connect
        print(arduino_connect)
        if arduino_connect:
            self.arduino = serial.Serial(port='/dev/cu.usbmodem141301', baudrate=1000000, timeout=.1)
        self.prev_move = (90, 90)
        self.move_threshold = move_threshold
        self.verbose = verbose

    def move(self, move):
        x = move[0]
        y = move[1]
        # check if the move is too similar
        if ((abs(x-self.prev_move[0]) < self.move_threshold) and (abs(y-self.prev_move[1]) < self.move_threshold)):
            return
        print('to similar')
        if self.verbose:
            print(f'({x}, {y})')
        self.prev_move = (x,y)
        if self.arduino_connect:
            value = self.arduino.write(bytes(f'{x},{y}', 'utf-8'))
        self.prev_move = move
    
    def close(self):
        self.arduino.close()