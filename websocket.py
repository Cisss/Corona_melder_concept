
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import random
import json

clients = []
roles = {}
rooms = {}
players = {}
json_questions = {}
questions = {}
class question_game(WebSocket):
    # handel messages
    def handleMessage(self):
        message = json.loads(self.data)
        # Handle simple return request
        if 'request' in message:
            # Handle room request
            if message['request'] == 'room':
                # create room
                print('int request room')
                room = self.random_room()
                print('room is requested')
                # get questions
                self.get_questions()
                # Send room number
                self.sendMessage('''{"room":''' + room + "}")
                # senf random question to random person
            elif message['request'] == 'question':
                self.random_player().sendMessage('''{"question":"''' + self.random_question() + '''"}''')               
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
            rooms.pop(room)
            for client in clients:
                client.sendMessage('''{"deleted_room":''' + room + "}")

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
            room = self.get_room()
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

    # get room number
    def get_room(self):
        for room in rooms:
                if self in rooms[room]:
                    return room

    #  get questions
    def get_questions(self):
        # get room
        room = self.get_room()
        print('over here')
        # get json from file
        with open('questions.json') as json_file:
            print('in file')
            data = json.load(json_file)
            # create list of questions
            json_questions["questions"] = data["questions"].copy()
            print(json_questions['questions'])
            # create questions list for room
            questions[room] = json_questions["questions"].copy()
            print(questions)

    # choose a random question
    def random_question(self):
        print("in function")
        # get room
        room = self.get_room()
        # if questions is empty reset
        if questions[room] == [] or room not in questions:
            print('in if statement')
            questions[room] = json_questions["questions"].copy()
        # choose random question
        num = len(questions[room])
        index = random.choice(range(num))
        random_question = questions[room][index]
        # delete choosen question
        questions[room].pop(index)
        # return choosen question
        return(random_question)

    def handleConnected(self):
        clients.append(self)

    def handleClose(self):
       clients.remove(self)

server = SimpleWebSocketServer('', 8000, question_game)
server.serveforever()
