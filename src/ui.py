import pygame

class UI:
    def __init__(self, resolution):
        # Init pygame and screen
        self.resolution = resolution
        self.screen = self.init_screen()
    
    def init_screen(self):
        pygame.init()
        return pygame.display.set_mode([self.resolution[0], self.resolution[1]])

class UIFollow(UI):
    def __init__(self, resolution):
        # Inherit UI class
        super().__init__(resolution)
    
    def update(self, img):
        # Update and return mouse pos
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # Fill the background with img
        background_img = pygame.surfarray.make_surface(img)
        background_img = pygame.transform.rotate(background_img, -90)
        self.screen.blit(background_img, (0, 0))

        # Draw line to indicate x and y of mouse position
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        pos = (mouse_pos_x, (self.resolution[1] - mouse_pos_y))
        pygame.draw.line(self.screen, (255,0,0), (0, mouse_pos_y), (self.resolution[0], mouse_pos_y)) # x
        pygame.draw.line(self.screen, (0,255,0), (mouse_pos_x, 0), (mouse_pos_x, self.resolution[1])) # y

        pygame.draw.circle(self.screen, (0,0,255), (mouse_pos_x, mouse_pos_y), 5)

        pygame.display.flip()

        return pos

class UICallibrate(UI):
    def __init__(self, settings, resolution, move_factor=1):
        # Inherit UI class
        super().__init__(resolution)

        # set fonts
        pygame.font.init()
        self.font = pygame.font.SysFont('Lucida Grande', 20)

        # set key press move
        self.move_factor = move_factor
        self.settings = {
            'max': settings['max'],
            'x_flipped': settings['x_flipped'],
            'y_flipped': settings['y_flipped']
        }
    
    def update(self, img, servo_pos):
        self.servo_pos = servo_pos
        # Update and return mouse pos
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # Fill the background with img
        background_img = pygame.surfarray.make_surface(img)
        background_img = pygame.transform.rotate(background_img, -90)
        self.screen.blit(background_img, (0, 0))

        # Display x and y degree
        self.display_text((f'X Degree: {self.servo_pos[0]}'), (0,0))
        self.display_text((f'Y Degree: {self.servo_pos[1]}'), (0,20))

        change = self.move_pos()
        self.change_settings()

        pygame.display.flip()

        return change
    
    def change_settings(self):
        # get keys
        keys_pressed = pygame.key.get_pressed()

        right_arrow = keys_pressed[pygame.K_RIGHT]
        left_arrow = keys_pressed[pygame.K_LEFT]
        down_arrow = keys_pressed[pygame.K_DOWN]
        up_arrow = keys_pressed[pygame.K_UP]
        x_key = keys_pressed[pygame.K_x]
        y_key = keys_pressed[pygame.K_y]

        option_key = keys_pressed[pygame.K_LALT]

        # make func to validate commands
        def valid_command():
            # If more than one arrow is pressed
            arrow_list = [right_arrow, left_arrow, down_arrow, up_arrow, x_key, y_key]
            keys = [a for a in arrow_list if a == True]
            if len(keys) != 1:
                return False
            
            # else
            return True

            # TODO: Make double presses not possible
       
        if option_key and valid_command():
            # set max
            if right_arrow:
                print('set max right')
                self.settings['max']['right'] = self.servo_pos[0]
            elif left_arrow:
                print('set max left')
                self.settings['max']['left'] = self.servo_pos[0]
            elif up_arrow:
                print('set max up')
                self.settings['max']['top'] = self.servo_pos[1]
            elif down_arrow:
                print('set max down')
                self.settings['max']['bottom'] = self.servo_pos[1]

            # set flipped
            elif x_key:
                print('flip x')
                self.settings['x_flipped'] = not self.settings['x_flipped']
            elif y_key:
                print('flip y')
                self.settings['y_flipped'] = not self.settings['y_flipped']
            


    def display_text(self, string, location):
        text = self.font.render(string, False, (0, 0, 0))

        self.screen.blit(text, location)
    
    def move_pos(self):
        keys_pressed = pygame.key.get_pressed()
        fn_key = keys_pressed[pygame.K_LSHIFT]

        def binary_value(condition):
            if condition:
                if fn_key:
                    return 0.1
                return 1
            else: return 0
        right_arrow = binary_value(keys_pressed[pygame.K_RIGHT])
        left_arrow = binary_value(keys_pressed[pygame.K_LEFT])
        down_arrow = binary_value(keys_pressed[pygame.K_DOWN])
        up_arrow = binary_value(keys_pressed[pygame.K_UP])

        ctrl_key = keys_pressed[pygame.K_LCTRL]
        s_key = keys_pressed[pygame.K_s]

        # Check if ctrl and s key is pressed
        if ctrl_key and s_key:
            # Change save mode to true
            self.save = True
        else:
            # Change save mode to false
            self.save = False

        # Return addition to move
        x_change = (right_arrow - left_arrow)*self.move_factor
        y_change = (up_arrow - down_arrow)*self.move_factor

        return (x_change, y_change)
        