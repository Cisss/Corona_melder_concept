
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import random
import json

clients = []
roles = {}
rooms = {}
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
                print('request for a message')
                if rooms != {}:
                    print('room is not empty')
                    for room in rooms:
                        print('foreach room')
                        print(room)
                        print(rooms[room])
                        if self in rooms[room]:
                            for client in clients:
                                if client in rooms[room]:
                                    client.sendMessage("random question")
                            

        # Add player to room
        elif 'join' in message:
            room_number = message['join']
            if room_number in rooms:
                print("in hereee")
                datad = {self}
                rooms[room_number].update(datad)
                print('did just that')
                print(rooms)
            else:
                print('invalid number')

    # Create room for host
    def random_room(self):
        room = str(random.choice(range(1000, 9000)))
        if room in rooms:
            self.random_room()
        else:
            rooms[room] = {self}
            print(rooms)
            return room

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






#  if roles[self]:
#     if roles[self] == 'host':
#         for client in clients:
#             if client == self:
#                 room = json.loads(self.data)['room']
#                 rooms[room] = self
#                 print(rooms)
#                 client.sendMessage(True, room)
# else:
#     client.sendMessage(False, "Kies eerst een role")



# from flask import Flask, render_template
# from flask_socketio import SocketIO, send, emit, join_room, leave_room
    
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return 'hooi'

# @socketio.on('connect')
# def test_message():
#    print("this works")
#    emit('my response', {'data': 'Connected'})
   

# @socketio.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + ' has entered the room.', room=room)

# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', room=room)

# @socketio.on_error_default
# def default_error_handler(e):
#     print(request.event["message"]) # "my error event"
#     print(request.event["args"])    # (data,)

# if __name__ == '__main__':
#     socketio.run(app)

