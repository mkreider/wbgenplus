class wide_high (object):
  ifname = 'ctrl'

  adrDict = {
  'first_rw'    : 0x0, # rw,  8 b, before
  'wide_rw_1'   : 0x4, # rw, 16 b, 48 bit, not a multiple of the bus width
  'wide_rw_0'   : 0x8, # rw, 32 b, 48 bit, not a multiple of the bus width
  'stat_get_1'  : 0xc, # ro, 32 b, 64 bit, driven
  'stat_get_0'  : 0x10, # ro, 32 b, 64 bit, driven
  }

  adrDict_reverse = {
  0x0   : 'first_rw', # rw,  8 b, before
  0x4   : 'wide_rw_1', # rw, 16 b, 48 bit, not a multiple of the bus width
  0x8   : 'wide_rw_0', # rw, 32 b, 48 bit, not a multiple of the bus width
  0xc   : 'stat_get_1', # ro, 32 b, 64 bit, driven
  0x10  : 'stat_get_0', # ro, 32 b, 64 bit, driven
  }

  flagDict = {
  'first' : 'rw', # before
  'wide'  : 'rw', # 48 bit, not a multiple of the bus width
  'stat'  : 'rd', # 64 bit, driven
  }

  valDict = {
  'first' : 0, # before
  'wide'  : 0, # 48 bit, not a multiple of the bus width
  'stat'  : 0, # 64 bit, driven
  }
