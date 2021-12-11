import pygame
import json

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 900

FLOOR_DIM = (650,650)
CHAT_DIM = (350,600)
CHAT_START_DIM = (15,150)
TILE_COUNT = 10

BG_COLOR  = (7,54,120)
GREEN_COLOR = (0, 255,0)
BLUE_COLOR = (0,0,255)
RED_COLOR = (255,0,0)
COLORS = []

class User():
    max_x = TILE_COUNT -1
    max_y = TILE_COUNT -1
    def __init__(self, color, username, x_pos=0, y_pos=0):
        self.color = color
        self.x_pos = min(x_pos,self.max_x)
        self.y_pos = min(y_pos,self.max_y)
        self.name = username
    
    def update(self, delta_x = 0, delta_y = 0):
        self.x_pos = min(self.x_pos + delta_x, self.max_x)
        self.x_pos = max(0, self.x_pos)

        self.y_pos = min(self.y_pos + delta_y, self.max_y)
        self.y_pos = max(0, self.y_pos)

    

class Floor():
    def __init__(self, tile_count, floor_dim, start_dim, screen):
        # Floor consists of a set of tiles, each of size TILE_COUNT
        self.tile_count = tile_count
        self.floor_dim = floor_dim
        self.grid_size = (floor_dim[0]/tile_count, floor_dim[1]/tile_count)
        self.start_dim = start_dim
        self.screen = screen
        # Display The users as tiles on the Floor
        self.users = {}

    def add_user(self,user):
        username = user.name
        print(type(user))
        if username in self.users:
            print("Warning, Duplicate Users Found, Will Replace Current User.")
            self.users[username] = user
        else:
            self.users[username] = user
        print(type(self.users[username].x_pos))

        self.draw(self.screen) 

    def draw(self,Screen):
        start_dim = self.start_dim
        floor_dim = self.floor_dim
        pygame.draw.rect(Screen, (255,255,255), pygame.Rect((start_dim),(floor_dim)) )

        for y in range(0,int(self.floor_dim[0]), int(self.grid_size[0])):
            # Print Vertical Lines for the grid
            pygame.draw.line(Screen,(0,0,0), start_pos=(start_dim[0]+y,start_dim[1]),end_pos=(start_dim[0]+y,start_dim[1]+floor_dim[1]),width=3)
        
        for x in range(0,int(self.floor_dim[1]), int(self.grid_size[1])):
            # Print Horizontal Lines for the Grid.
            pygame.draw.line(Screen,(0,0,0), start_pos=(start_dim[0],start_dim[1]+x),end_pos=(start_dim[0] + floor_dim[0],start_dim[1]+x),width=3)
        
        for username, user in self.users.items():
            print(username)
            rect_start = (self.start_dim[0]+ user.y_pos*self.grid_size[0], self.start_dim[1]+user.x_pos*self.grid_size[0])
            pygame.draw.rect(Screen, user.color,pygame.Rect(rect_start,self.grid_size))
            
    def update_users(self, username):
        print(username)
        self.draw(self.screen)
        return 
    
    def update_user_deltas(self, username, delta_x=0, delta_y=0):
        print(username)
        if username not in self.users:
            print("User does not exist, continuing")
            # We should actually create a new user, drop at (0,0)
        else:
            self.users[username].update(delta_x, delta_y) 
        
        self.draw(self.screen)
            
        

class Chat():

    def __init__(self, Screen, start_dim):
        self.num_messages = 8
        self.start_dim = start_dim
        self.chat_dim = CHAT_DIM
        self.input_rect = pygame.Rect((15,start_dim[1]+CHAT_DIM[1]),(350,50))
        self.text = ''
        self.font  = pygame.font.SysFont("Ubuntu", 18)
        self.screen = Screen
        self.messages = [{"username":"FrostyNight", "text":"Finish this sem"},{"username":"Angad11121", "text":"Finish this sem"}]
        # self.messages = [{"username":"FrostyNigh#t", "text":"1"},{"username":"2", "text":"2"}]
        pygame.draw.rect(Screen, (220,220,220), self.input_rect)
        self.draw(self.screen)
    
    def draw(self, Screen):
        msgs = self.messages
        start_dim = self.start_dim
        chat_dim = self.chat_dim 
        pygame.draw.rect(Screen, (30,30,30), pygame.Rect((start_dim),(chat_dim)))
        index = 1
        for msg in reversed(msgs[-self.num_messages:]):
            print(msg)
            text_msg = msg["username"] + ": " + msg["text"]
            chat_msgs = self.font.render(text_msg, True, (255,255,255))
            w, h =chat_msgs.get_size()
            self.screen.blit(chat_msgs,(16,self.start_dim[1]+CHAT_DIM[1] +25 -h/2 -index*50))
            index +=1

    def chat_input(self,event):
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_RETURN:
                # send_chat(username,self.text)
                self.messages.append({'username':my_username, 'text':self.text})
                self.text = ''
                self.draw(self.screen)
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            chat_label = self.font.render(self.text, True, (0,0,0))
            w,h = chat_label.get_size()
            pygame.draw.rect(self.screen, (220,220,220), self.input_rect)
            self.screen.blit(chat_label, (16,self.start_dim[1]+CHAT_DIM[1] +25 -h/2),(max(w-348,0), 0, 348, h))

            
            
my_username = 'Rachit'

current_focus = "grid"
pygame.init()
clock = pygame.time.Clock()
pygame.font.init()

canvas = pygame.display.set_mode(size=[WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption('Metaverse')
canvas.fill(BG_COLOR)

display_font  = pygame.font.SysFont("Ubuntu", 30)
label = display_font.render(f'Hello, {my_username}!, Welcome to the metaverse', True,(255,255,255))

canvas.blit(label, ((WINDOW_WIDTH)*0.30,50))

# Create our user
# Drop him at 0,0 for now
myuser = User(color=GREEN_COLOR, username=my_username, x_pos=0, y_pos=0)
print(myuser)

# Initialize the Floor 
metaverse = Floor(tile_count=TILE_COUNT, floor_dim =FLOOR_DIM, start_dim=(400, 150), screen=canvas)
metaverse.draw(canvas)
metaverse.add_user(myuser)

# Init chat
chatBox = Chat(canvas, start_dim = CHAT_START_DIM)
chatBox.draw(canvas)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if chatBox.input_rect.collidepoint(event.pos):
                current_focus = "chat"
            else:
                current_focus = "grid"    
            continue
        
        if current_focus == "grid":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    current_focus = "chat"
        
        if current_focus == "chat":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_focus = "grid"

        if current_focus == "grid":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    print("DOWN")
                    metaverse.update_user_deltas(my_username,delta_x=1)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    print("UP")
                    metaverse.update_user_deltas(my_username,delta_x=-1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    print("LEFT")
                    # metaverse.update_users(my_username)
                    metaverse.update_user_deltas(my_username,delta_y=-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    print("RIGHT")
                    metaverse.update_user_deltas(my_username,delta_y=1)
                    # Insert Socket Call here Send a message to server saying we've updated the position
        else:
            chatBox.chat_input(event)


        clock.tick(60)

        pygame.display.flip()

pygame.quit()
