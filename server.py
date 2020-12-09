# Name: Paavo Hemmo, student ID: 014582750

import socket
from packethandling import client_id_packet, server_data_packet
import random
from player import Player
import time, threading

class Server(object):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    # Create a UDP socket (SOCK_DGRAM)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind((self.host, self.port))
    self.packetSize = 100
    self.client_endpoints = []
    self.players = []
    self.max_players = 33
    self.tick_rate = 60 # tick_rate times a second
    self.idle_times = []
    self.init_players_and_endpoints()
  
  def init_players_and_endpoints(self):
    for i in range(0, self.max_players):
      self.client_endpoints.append(None)
      self.players.append(None)
      self.idle_times.append(0)
  
  def listen(self):
    threading.Thread(target = self.send_game_state_to_clients).start()
    while True:
      # Receive a message from somewhere
      bytesAddressPair = self.sock.recvfrom(self.packetSize)
      message = bytesAddressPair[0]
      address = bytesAddressPair[1]

      if message[0] == 1:
        # join server packet
        if self.handle_join_server(address):
          print("successfully joined server")
      elif message[0] == 4:
        # user input packet
        client_id = message[1]
        self.idle_times[client_id] = 0
        self.handle_user_input(message)
      elif message[0] == 3:
        # client leaving server packet
        self.handle_client_leaving_server(message)
  
  def handle_user_input(self, message):
    client_id = message[1]
    key = message[2]

    player = self.players[client_id]
    player.changePosition(bytes([key]).decode('utf-8'))
  
  def handle_client_leaving_server(self, message):
    client_id = message[1]

    print("disconnecting client", client_id)

    self.client_endpoints[client_id] = None
    self.players[client_id] = None
    self.idle_times[client_id] = 0
  
  def send_game_state_to_clients(self):
    while True:
      filled_slots = []
      for p in self.players:
        if p:
          filled_slots.append(p)
          self.idle_times[p.client_id] += 1
          if self.idle_times[p.client_id] > (120 * self.tick_rate):
            self.handle_client_leaving_server((0, p.client_id))
            print("client has been idle for 120 seconds")
      data = server_data_packet(filled_slots)
      for c in self.client_endpoints:
        if c:
          self.sock.sendto(data, c)
      time.sleep(1 / self.tick_rate)

  
  def handle_join_server(self, address):
    # Go through all the clients, and see if same address already exists
    index_of_first_null = self.max_players
    same_address_found = False
    i = 0
    for c in self.client_endpoints:
      if c is None and index_of_first_null == self.max_players:
        index_of_first_null = i
      else:
        if c == address:
          same_address_found = True
      i += 1
    
    if index_of_first_null < self.max_players and not same_address_found:
      # ok to add
      client_id = index_of_first_null
      self.client_endpoints[client_id] = address
      self.add_player_to_server(client_id)
      self.send_client_id_to_client(client_id, address)
      return True
    return False
  
  def send_client_id_to_client(self, client_id, address):
    data = client_id_packet(client_id)
    self.sock.sendto(data, address)
  
  def add_player_to_server(self, client_id):
    positionX = 0
    positionY = 0
    while True:
      positionX = random.randint(0, 19)
      ositionY = random.randint(0, 19)
      samePositionFound = False
      # Check that no other player has the same position
      for p in self.players:
        if p and p.getPositionX() == positionX and p.getPositionY() == positionY:
          samePositionFound = True
      if not samePositionFound:
        break
    player = Player(client_id, positionX, positionY)
    self.players[client_id] = player
  
if __name__ == "__main__":
  port_num = 13445
  host = socket.gethostname()
  print("hostname: ", host)

  Server(host, port_num).listen()