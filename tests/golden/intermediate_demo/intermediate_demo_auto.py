class intermediate_demo (object):
  ifname = 'slave'

  adrDict = {
  'status_get'      : 0x000, # ro, g_channels b, 'timestamps pending' bit per channel
  'ch_qty_get'      : 0x004, # ro,          5 b, Individually controllable flag bits
  'ch_sel_rw'       : 0x020, # rw,          8 b, Channel select register
  'clear_fifo_owr'  : 0x100, # wo,          1 b, Clears Fifo
  'ts_out_get_0'    : 0x104, # ro,         32 b, Timestamp fifos in. Use RD flag to pop
  'ts_out_get_1'    : 0x108, # ro,         32 b, Timestamp fifos in. Use RD flag to pop
  'ts_cnt_get'      : 0x10c, # ro,         16 b, Shows channel timestamp count
  'ts_flags_rw'     : 0x110, # rw,    g_flags b, timestamp channel flagbits
  }

  adrDict_reverse = {
  0x000 : 'status_get', # ro, g_channels b, 'timestamps pending' bit per channel
  0x004 : 'ch_qty_get', # ro,          5 b, Individually controllable flag bits
  0x020 : 'ch_sel_rw', # rw,          8 b, Channel select register
  0x100 : 'clear_fifo_owr', # wo,          1 b, Clears Fifo
  0x104 : 'ts_out_get_0', # ro,         32 b, Timestamp fifos in. Use RD flag to pop
  0x108 : 'ts_out_get_1', # ro,         32 b, Timestamp fifos in. Use RD flag to pop
  0x10c : 'ts_cnt_get', # ro,         16 b, Shows channel timestamp count
  0x110 : 'ts_flags_rw', # rw,    g_flags b, timestamp channel flagbits
  }

  flagDict = {
  'status'      : 'rd', # 'timestamps pending' bit per channel
  'ch_qty'      : 'r', # Individually controllable flag bits
  'ch_sel'      : 'rw', # Channel select register
  'clear_fifo'  : 'wmsp', # Clears Fifo
  'ts_out'      : 'rdmf', # Timestamp fifos in. Use RD flag to pop
  'ts_cnt'      : 'rdm', # Shows channel timestamp count
  'ts_flags'    : 'rwm', # timestamp channel flagbits
  }

  valDict = {
  'status'      : 0, # 'timestamps pending' bit per channel
  'ch_qty'      : channels, # Individually controllable flag bits
  'ch_sel'      : 0, # Channel select register
  'clear_fifo'  : 0, # Clears Fifo
  'ts_out'      : 0, # Timestamp fifos in. Use RD flag to pop
  'ts_cnt'      : 0, # Shows channel timestamp count
  'ts_flags'    : 0, # timestamp channel flagbits
  }
