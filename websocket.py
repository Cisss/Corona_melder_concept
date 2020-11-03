
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import random
import json

clients = []
roles = {}
rooms = {}
players = {}
json_questions = {}
questions = {}
class SimpleChat(WebSocket):
    # handel messages
    def handleMessage(self):
        message = json.loads(self.data)
        # Handle simple return request
        if 'request' in message:
            # Handle room request
            if message['request'] == 'room':
                # get questions
                self.get_questions()
                room = self.random_room()
                self.sendMessage("room:" + str(room))
            elif message['request'] == 'question':
                self.random_player().sendMessage(self.random_question())               
        # Add player to room
        elif 'join' in message:
            room = message['join']
            if room in rooms:
                player = {self}
                rooms[room] += player
                players[room] = rooms[room].copy()
            else:
                print('invalid number')
        # delete room
        elif 'delete' in message:
            room = message['delete']
            print(rooms)
            print(room)
            rooms.pop(room)
            print(room)
            for client in clients:
                client.sendMessage("deleted room:" + room)

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
        # if there are one or more rooms
        if rooms != []:
            # select room that the current user is in
            for room in rooms:
                if self in rooms[room]:
                    # choose random player
                    num = len(players[room])
                    index = random.choice(range(num))
                    active_player = players[room][index]
                    # Remove player from players
                    players[room].pop(index)
                    # if there is only one player left reset players
                    if(num == 1):
                        players[room] = rooms[room].copy()
                    # return choosen user
                    return active_player

    #  get questions
    def get_questions(self):
        with open('questions.json') as json_file:
            data = json.load(json_file)
            # create questions
            json_questions["questions"] = data["questions"].copy()
            questions['questions'] = json_questions["questions"].copy()

    # choose a random question
    def random_question(self):
        # if questions is empty reset
        if questions['questions'] == []:
            questions['questions'] = json_questions["questions"].copy()
        # choose random question
        num = len(questions["questions"])
        index = random.choice(range(num))
        random_question = questions["questions"][index]
        # delete choosen question
        questions['questions'].pop(index)
        # return choosen question
        return(random_question)

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
