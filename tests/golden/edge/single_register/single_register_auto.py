class single_register (object):
  ifname = 'ctrl'

  adrDict = {
  'value_rw'  : 0x0, # rw, 8 b, only register
  }

  adrDict_reverse = {
  0x0 : 'value_rw', # rw, 8 b, only register
  }

  flagDict = {
  'value' : 'rw', # only register
  }

  valDict = {
  'value' : 0, # only register
  }
