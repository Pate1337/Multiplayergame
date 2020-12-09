# Name: Paavo Hemmo, student ID: 014582750

import pygame
from player import Player

class Game(object):
  def __init__(self, client):
    self.players = []
    self.init_players()
    self.client_id = None
    self.player = None
    self.client = client
    self.player_count = 0
  
  def init_players(self):
    for i in range(0, 33):
      self.players.append(None)
  
  def getPlayers(self):
    return self.players
  
  def getPlayerCount(self):
    return self.player_count
  
  def removePlayer(self, client_id):
    self.players[client_id] = None
    self.player_count -= 1
  
  def updatePlayerPosition(self, client_id, positionX, positionY):
    self.players[client_id].setPositionX(positionX)
    self.players[client_id].setPositionY(positionY)
  
  def addPlayer(self, client_id, positionX, positionY):
    self.players[client_id] = Player(client_id, positionX, positionY)
    self.player = self.players[self.client_id]
    self.player_count += 1

  def drawGrid(self, w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
      x = x + sizeBtwn
      y = y + sizeBtwn

      pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
      pygame.draw.line(surface, (255,255,255), (0,y),(w,y))

  def redrawWindow(self, surface):
    global rows, width
    surface.fill((0, 0, 0))
    for p in self.players:
        if p:
          p.draw(surface, width, rows, pygame)
    self.drawGrid(width,rows, surface)
    pygame.display.update()
  
  def setClient(self, client_id):
    self.client_id = client_id

  def start(self):
    global rows, width
    pygame.init()
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    clock = pygame.time.Clock()
    key = ""

    while key != "quit":
      if self.player:
        key = self.player.move(pygame)
      self.redrawWindow(win)
      clock.tick(60)
      if key != "" and key != "quit":
        self.client.send_user_input(self.client_id, key)
    self.client.disconnect_from_server(self.client_id)
    pygame.quit()