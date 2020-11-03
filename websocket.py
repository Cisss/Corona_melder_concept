
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import random
import json

clients = []
roles = {}
rooms = {}
players = {}
class SimpleChat(WebSocket):

    def handleMessage(self):
        message = json.loads(self.data)
        # Handle simple return request
        if 'request' in message:
            # Handle room request
            if message['request'] == 'room':
                room = self.random_room()
                self.sendMessage("room:" + str(room))
            elif message['request'] == 'question':
                self.random_player().sendMessage("random question")               
        # Add player to room
        elif 'join' in message:
            room = message['join']
            if room in rooms:
                datad = {self}
                rooms[room] += datad
                players[room] = rooms[room].copy()
            else:
                print('invalid number')

    # Create room for host
    def random_room(self):
        room = str(random.choice(range(1000, 9000)))
        if room in rooms:
            self.random_room()
        else:
            rooms[room] = [self]
            return room

    # choose a random user
    def random_player(self):
        print("rooms", rooms)
        # if there are one or more rooms
        if rooms != []:
            # select room that the current user is in
            for room in rooms:
                print(rooms[room])
                if self in rooms[room]:
                    # choose random player
                    num = len(players[room])
                    print("number", num)
                    index = random.choice(range(num))
                    active_player = players[room][index]
                    # Remove player from players
                    players[room].pop(index)
                    # if there is only one player left reset players
                    if(num == 1):
                        print(players[room])
                        print(rooms[room])
                        players[room] = rooms[room]
                        print(players[room])
                    # return choosen user
                    return active_player
                        
        
    def handleConnected(self):
        print(self.address, 'connected')
        for client in clients:
            client.sendMessage(self.address[0] + u' - connected')
        clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')

server = SimpleWebSocketServer('', 8000, SimpleChat)
server.serveforever()
