class simple_demo (object):
  ifname = 'slave'

  adrDict = {
  'status_get'  : 0x00, # ro, g_statusbits b, Shows if the devices are rdy/busy
  'mode_get'    : 0x04, # ro,            8 b, Mode
  'mode_clr'    : 0x08, # wo,            8 b, Mode
  'mode_set'    : 0x0c, # wo,            8 b, Mode
  'scpad_rw_1'  : 0x10, # rw,           32 b, Scratchpad. Can be modified from Bus or outer entity
  'scpad_rw_0'  : 0x14, # rw,           32 b, Scratchpad. Can be modified from Bus or outer entity
  'count_get'   : 0x18, # ro,           16 b, Shows Data Input Counter
  }

  adrDict_reverse = {
  0x00  : 'status_get', # ro, g_statusbits b, Shows if the devices are rdy/busy
  0x04  : 'mode_get', # ro,            8 b, Mode
  0x08  : 'mode_clr', # wo,            8 b, Mode
  0x0c  : 'mode_set', # wo,            8 b, Mode
  0x10  : 'scpad_rw_1', # rw,           32 b, Scratchpad. Can be modified from Bus or outer entity
  0x14  : 'scpad_rw_0', # rw,           32 b, Scratchpad. Can be modified from Bus or outer entity
  0x18  : 'count_get', # ro,           16 b, Shows Data Input Counter
  }

  flagDict = {
  'status'  : 'rd', # Shows if the devices are rdy/busy
  'mode'    : 'rwaf', # Mode
  'scpad'   : 'rwdf', # Scratchpad. Can be modified from Bus or outer entity
  'count'   : 'rd', # Shows Data Input Counter
  }

  valDict = {
  'status'  : 0, # Shows if the devices are rdy/busy
  'mode'    : 0xff, # Mode
  'scpad'   : 0, # Scratchpad. Can be modified from Bus or outer entity
  'count'   : 0, # Shows Data Input Counter
  }
