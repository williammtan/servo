import pygame
import time
import cv2

from serial_transmitter import SerialTransmitter
from ui import UIFollow
from face_detection import FaceDetection
from _json import Json

class Turret:
    def __init__(self):
        self.serial_transmitter = SerialTransmitter()
        self.face_detection = FaceDetection()
        self.json = Json()

        self.settings = self.json.get_json()
        self.camera_fov = camera_fov
        self.resolution = self.face_detection.resolution
        self.pos = ()

    def move(self, move):
        # Send move (in degrees) to serial transmitter class
        self.serial_transmitter.move(move)
    
    def convert(self, move):
        # Convert pos in video to degree
        x = move[0]
        y = move[1]

        x_ratio = x/640
        y_ratio = y/480
        
        if self.settings['x_flipped']:
            servo_x = round((180-self.settings['right'])/2 + (self.camera_fov*(1-x_ratio)), 1)
        else:
            servo_x = round((self.settings['left'])/2 + (self.camera_fov*(x_ratio)), 1)
        if self.settings['y_flipped']:
            servo_y = round((180-self.settings['top'])/2 + (self.camera_fov*(1-y_ratio)), 1)
        else:
            servo_y = round((self.settings['bottom'])/2 + (self.camera_fov*(y_ratio)), 1)

        return (servo_x, servo_y)

class TurretCommand(Turret):
    def __init__(self):
        # Inherit parent Turret class
        super().__init__()
        
        self.ui = UIFollow((640, 480))
        self.start()

    def start(self):
        # Run loop
        running = True
        while running:
            img = self.face_detection.get_img()
            self.pos = self.ui.update(img)
            self.servo_pos = self.convert(self.pos)
            self.serial_transmitter.move(self.servo_pos)
            time.sleep(0.01)

            

class TurretFollow:
    def __init__(self):
        pass

class OldTurret:
    def __init__(self, camera_fov=65.563, mode='command', x_flipped=False, y_flipped=False):
        self.serial_transmitter = SerialTransmitter()
        self.x_flipped = x_flipped
        self.y_flipped = y_flipped
        self.camera_fov = camera_fov

        if mode == 'command':
            self.resolution = 500
            self.command()
        elif mode == 'follow':
            self.follow()
        else:
            raise Exception('Not available mode!')

    def command(self):
        # Start pygame module to control turret

        pygame.init()
        screen = pygame.display.set_mode([self.resolution, self.resolution])

        # Create font
        font = pygame.font.SysFont('Lucida Grande', 20)

        # running loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the background with black
            screen.fill((0, 0, 0))

            # Draw line to indicate x and y of mouse position
            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255,0,0), (0, mouse_pos_y), (self.resolution, mouse_pos_y)) # x
            pygame.draw.line(screen, (0,255,0), (mouse_pos_x, 0), (mouse_pos_x, self.resolution)) # y

            pygame.draw.circle(screen, (0,0,255), (mouse_pos_x, mouse_pos_y), 5)
            
            # Display x and y of mouse position
            text_x = font.render(f'X: {mouse_pos_x}\n', True, (255, 255, 255))
            text_y = font.render(f'Y: {self.resolution - mouse_pos_y}', True, (255, 255, 255))
            screen.blit(text_x, (0,0))
            screen.blit(text_y, (0,30))

            # Move turret
            if mouse_pos_x == None or mouse_pos_y == None:
                continue
            degree_x, degree_y = self.convert_command(mouse_pos_x, mouse_pos_y)
            self.serial_transmitter.move((degree_x, degree_y))
            time.sleep(0.01)

            pygame.display.flip()
        pygame.quit()
    
    def display():
        pass

    
    def convert_command(self, x, y):
        x_ratio = x/self.resolution
        y_ratio = y/self.resolution
        if self.x_flipped:
            degree_x = 180-(180*x_ratio)
        else:
            degree_x = 180*x_ratio
        if self.y_flipped:
            degree_y = 180-(180*y_ratio)
        else:
            degree_y = 180*y_ratio
        return degree_x, degree_y

    def convert(self, x, y):
        x_ratio = x/640
        y_ratio = y/480
        camera_fov = self.camera_fov
        degree_x = (180-camera_fov)/2 + (camera_fov*(1-x_ratio))
        degree_y = (180-camera_fov)/2 + (camera_fov*y_ratio)
        return degree_x, degree_y

    def follow(self):
        pass


