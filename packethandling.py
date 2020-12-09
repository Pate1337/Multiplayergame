# Name: Paavo Hemmo, student ID: 014582750

import struct

def join_server_packet():
  value = bytes([1])
  packer = struct.Struct('c')
  packed_data = packer.pack(value)

  return packed_data

def client_id_packet(client_id):
  values = (bytes([2]), bytes([client_id]))
  packer = struct.Struct('c c')
  packed_data = packer.pack(*values)

  return packed_data

def server_data_packet(players):
  data_part = "c "
  values = []
  values.append(bytes([5]))
  for p in players:
    values.append(bytes([p.getClientID()]))
    values.append(bytes([p.getPositionX()]))
    values.append(bytes([p.getPositionY()]))
    data_part += "c c c "
  
  packer = struct.Struct(data_part)
  packed_data = packer.pack(*values)

  return packed_data

def user_input_packet(client_id, key):
  values = (bytes([4]), bytes([client_id]), key.encode())
  packer = struct.Struct('c c c')
  packed_data = packer.pack(*values)

  return packed_data

def client_leaving_server_packet(client_id):
  values = (bytes([3]), bytes([client_id]))
  packer = struct.Struct('c c')
  packed_data = packer.pack(*values)

  return packed_data
