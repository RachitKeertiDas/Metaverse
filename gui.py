import pygame
import json
import threading
import textwrap as tr
from socket import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 900

FLOOR_DIM = (650,650)
CHAT_DIM = (350,600)
CHAT_START_DIM = (15,150)
TILE_COUNT = 10

BG_COLOR  = (24,44,97)
GREEN_COLOR = (0, 255,0)
BLUE_COLOR = (0,0,255)
RED_COLOR = (255,0,0)
COLORS = []

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


def send_chat(clientSocket, message : str):
    print(message)
    clientSocket.send(message.encode())
    return


def listen_chat(clientSocket, chatBox, metaverse,  my_username):
    # Listen From Server. If Server sends the message exit, we terminate"
    while True:
        message = clientSocket.recv(1024)
        # Do Whatever with the message here, pass it to the GUI for rendering
        msg = message.decode()
        if 1:
            msg_dict = json.loads(msg)
            if msg_dict['component'] == 'chat':
                if msg_dict['username'] == my_username:
                    continue
                chatBox.update_messages(msg)
            elif msg_dict['component'] == 'grid':
                if msg_dict['username'] == my_username:
                    continue
                metaverse.update_users(msg_dict["username"],msg_dict["xpos"], msg_dict["ypos"])
        else:
            print("Malformed Server Message")
            continue
        
        if msg == 'exit':
            clientSocket.close()
            return 
        print("Message Recieved From Server", msg)


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
            rect_start = (self.start_dim[0]+ user.y_pos*self.grid_size[0]+2, self.start_dim[1]+user.x_pos*self.grid_size[0]+2)
            pygame.draw.rect(Screen, user.color,pygame.Rect(rect_start,(self.grid_size[0]-4,self.grid_size[1]-4)))
            
    def update_users(self, username, x_pos, y_pos):

        if username not in self.users:
            # Add him
            new_user = User(BLUE_COLOR, username, x_pos, y_pos)
            self.add_user(new_user)

        current_x = self.users[username].x_pos
        current_y = self.users[username].y_pos
        print(f"Trying to Update {username} to position ({x_pos}, {y_pos})")
        self.update_user_deltas(username, delta_x =(x_pos-current_x), delta_y = (y_pos-current_y) )

        self.draw(self.screen)
        return 
    
    def update_user_deltas(self, username, delta_x=0, delta_y=0):
        print(username)
        if username not in self.users:
            print("User does not exist, continuing")
            # We should actually create a new user, drop at (0,0)
        else:
            self.users[username].update(delta_x, delta_y) 

        # Also convey to the server that we changed position if this is user recieved
        if username == my_username:
            print("Pinging Server")
            msg_dict = {"component":"grid", "username":username,"xpos":self.users[username].x_pos, "ypos":self.users[username].y_pos}
            send_chat(clientSocket, json.dumps(msg_dict))
         
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
        self.messages = [{"username":"FrostyNight", "text":"Hi, Welcome"},{"username":"Angad11121", "text":"Click on the text to get started"}]
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
    
    def update_messages(self, message: str):
        # Ignore message from myself
        try:
            msg_dict = json.loads(message)
            self.messages.append(msg_dict)
            self.draw(self.screen)
        except:
            print("Error occured: Malformed Server Message")

    def chat_input(self,event):
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_RETURN:
                # send_chat(username,self.text)
                msg_dict = {"component": "chat", "username": my_username, 'text': self.text}
                self.messages.append(msg_dict)
                send_chat(clientSocket, json.dumps(msg_dict))
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


my_username = input('Enter a Username:') 

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

## Create a Separate Listening Thread

# send_proc = threading.Thread(target=send_chat, args=[clientSocket])
listen_proc = threading.Thread(target=listen_chat, args=[clientSocket, chatBox, metaverse ,my_username])

#send_proc.start()
listen_proc.start()

# Just Inform everyone else of our position

metaverse.update_user_deltas(my_username, 0,0)
## Start Listening to Input Now


while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                send_chat(clientSocket, 'exit')
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

            clock.tick(60) # Cap the FPS

            pygame.display.flip()
    except KeyboardInterrupt:
        print("Shutting Down Gracefully")
        send_chat(clientSocket, 'exit')
        pygame.quit()
        break
        
#pygame.quit()
# clientSocket.close()

## FORMAT FOR SENDING MESSAGES TO THE SERVER

"""
json message
{
    "component": "chat"/"audio", "misc", "grid"
    "username" : username
    "text" : text
    "xpos" : xpos
    "ypos" : ypos
}
"""
