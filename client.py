# Name: Paavo Hemmo, student ID: 014582750

import socket
from packethandling import join_server_packet, user_input_packet, client_leaving_server_packet
from player import Player
import threading
from game import Game

class Client(object):
  def __init__(self, host, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.serverAddress = (host, port)
    self.packetSize = 100
    self.game = Game(self)
    self.client_id = None
  
  def send_user_input(self, client_id, key):
    data = user_input_packet(client_id, key)
    self.sock.sendto(data, self.serverAddress)

  def listen_to_server(self):
    while True:
      bytesAddressPair = self.sock.recvfrom(self.packetSize)
      message = bytesAddressPair[0]
      address = bytesAddressPair[1]

      if message[0] == 2:
        # clientID packet
        self.client_id = message[1]
        self.game.setClient(self.client_id)
      elif message[0] == 5:
        self.handle_game_state_from_server(message)

  def join_server(self):
    data = join_server_packet()
    self.sock.sendto(data, self.serverAddress)
  
  def start_game(self):
    self.game.start()
  
  def disconnect_from_server(self, client_id):
    data = client_leaving_server_packet(client_id)
    print(data)
    self.sock.sendto(data, self.serverAddress)

  def handle_game_state_from_server(self, message):
    i = 1
    client_id = None
    positionX = None
    positionY = None
    clients_on_server = []
    players = self.game.getPlayers()
    for b in message[1:len(message)]:
      if i % 3 == 1:
        # client_id
        client_id = b
        clients_on_server.append(client_id)
      elif i % 3 == 2:
        # positionX
        positionX = b
      else:
        positionY = b
        if players[client_id]:
          self.game.updatePlayerPosition(client_id, positionX, positionY)
        else:
          self.game.addPlayer(client_id, positionX, positionY)
      i += 1
    if self.game.getPlayerCount() != len(clients_on_server):
      for p in players:
        if p.client_id not in clients_on_server:
          self.game.removePlayer(p.client_id)
          break

  
if __name__ == "__main__":
  host = "Paavo-Air"
  port = 13445
  c = Client(host, port)
  c.join_server()
  server_listener = threading.Thread(target = c.listen_to_server)
  server_listener.start()
  c.start_game()