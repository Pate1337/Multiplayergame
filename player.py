# Name: Paavo Hemmo, student ID: 014582750

class Player(object):
  def __init__(self, client_id, positionX, positionY):
    self.client_id = client_id
    self.positionX = positionX
    self.positionY = positionY
  
  def getPositionX(self):
    return self.positionX
  
  def getPositionY(self):
    return self.positionY
  
  def getClientID(self):
    return self.client_id
  
  def setPositionX(self, positionX):
    self.positionX = positionX
  
  def setPositionY(self, positionY):
    self.positionY = positionY
  
  def getColor(self):
    return self.color
  
  def draw(self, surface, width, rows, pygame):
    dis = width // rows
    i = self.positionX
    j = self.positionY

    pygame.draw.rect(surface, (255,0,0), (i*dis+1,j*dis+1, dis-2, dis-2))
  
  def move(self, pygame):
    pressed = ""
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return "quit"
      keys = pygame.key.get_pressed()
      for key in keys:
        if keys[pygame.K_a]:
          pressed = "a"
        elif keys[pygame.K_d]:
          pressed = "d"
        elif keys[pygame.K_w]:
          pressed = "w"
        elif keys[pygame.K_s]:
          pressed = "s"
    return pressed
  
  def changePosition(self, key):
    if key == "a" and self.positionX != 0:
      self.positionX -= 1
    elif key == "w" and self.positionY != 0:
      self.positionY -= 1
    elif key == "d" and self.positionX != 19:
      self.positionX += 1
    elif key == "s" and self.positionY != 19:
      self.positionY += 1