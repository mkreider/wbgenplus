class prio (object):
  ifname = 'ctrl'

  adrDict = {
  'reset_owr'         : 0x00000, # wo,          1 b, Resets the Priority Queue
  'mode_get'          : 0x00004, # ro,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  'mode_clr'          : 0x00008, # wo,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  'mode_set'          : 0x0000c, # wo,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  'clear_owr'         : 0x00010, # wo,          1 b, Clears counters and status
  'st_full_get'       : 0x00014, # ro, g_channels b, Channel Full flag (n..0) 
  'st_late_get'       : 0x00018, # ro,          1 b, Late message detected
  'ebm_adr_rw'        : 0x0001c, # rw,         32 b, Etherbone Master address
  'eca_adr_rw'        : 0x00020, # rw,         32 b, Event Condition Action Unit address
  'tx_max_msgs_rw'    : 0x00024, # rw,          8 b, Max msgs per packet
  'tx_max_wait_rw'    : 0x00028, # rw,         32 b, Max wait time for non empty packet
  'tx_rate_limit_rw'  : 0x0002c, # rw,         32 b, Max msgs per milliseconds
  'offs_late_rw_0'    : 0x00030, # rw,         32 b, Time offset before message is late
  'offs_late_rw_1'    : 0x00034, # rw,         32 b, Time offset before message is late
  'cnt_late_get'      : 0x00038, # ro,         32 b, Sum of all late messages
  'ts_late_get_0'     : 0x0003c, # ro,         32 b, First late Timestamp
  'ts_late_get_1'     : 0x00040, # ro,         32 b, First late Timestamp
  'cnt_out_all_get_0' : 0x00044, # ro,         32 b, Sum of all outgoing messages
  'cnt_out_all_get_1' : 0x00048, # ro,         32 b, Sum of all outgoing messages
  }

  adrDict_reverse = {
  0x00000 : 'reset_owr', # wo,          1 b, Resets the Priority Queue
  0x00004 : 'mode_get', # ro,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  0x00008 : 'mode_clr', # wo,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  0x0000c : 'mode_set', # wo,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  0x00010 : 'clear_owr', # wo,          1 b, Clears counters and status
  0x00014 : 'st_full_get', # ro, g_channels b, Channel Full flag (n..0) 
  0x00018 : 'st_late_get', # ro,          1 b, Late message detected
  0x0001c : 'ebm_adr_rw', # rw,         32 b, Etherbone Master address
  0x00020 : 'eca_adr_rw', # rw,         32 b, Event Condition Action Unit address
  0x00024 : 'tx_max_msgs_rw', # rw,          8 b, Max msgs per packet
  0x00028 : 'tx_max_wait_rw', # rw,         32 b, Max wait time for non empty packet
  0x0002c : 'tx_rate_limit_rw', # rw,         32 b, Max msgs per milliseconds
  0x00030 : 'offs_late_rw_0', # rw,         32 b, Time offset before message is late
  0x00034 : 'offs_late_rw_1', # rw,         32 b, Time offset before message is late
  0x00038 : 'cnt_late_get', # ro,         32 b, Sum of all late messages
  0x0003c : 'ts_late_get_0', # ro,         32 b, First late Timestamp
  0x00040 : 'ts_late_get_1', # ro,         32 b, First late Timestamp
  0x00044 : 'cnt_out_all_get_0', # ro,         32 b, Sum of all outgoing messages
  0x00048 : 'cnt_out_all_get_1', # ro,         32 b, Sum of all outgoing messages
  }

  flagDict = {
  'reset'         : 'wp', # Resets the Priority Queue
  'mode'          : 'rwa', # b2: Time limit, b1: Msg limit, b0 enable
  'clear'         : 'wp', # Clears counters and status
  'st_full'       : 'rd', # Channel Full flag (n..0) 
  'st_late'       : 'rd', # Late message detected
  'ebm_adr'       : 'rw', # Etherbone Master address
  'eca_adr'       : 'rw', # Event Condition Action Unit address
  'tx_max_msgs'   : 'rw', # Max msgs per packet
  'tx_max_wait'   : 'rw', # Max wait time for non empty packet
  'tx_rate_limit' : 'rw', # Max msgs per milliseconds
  'offs_late'     : 'rw', # Time offset before message is late
  'cnt_late'      : 'rd', # Sum of all late messages
  'ts_late'       : 'rd', # First late Timestamp
  'cnt_out_all'   : 'rd', # Sum of all outgoing messages
  }

  valDict = {
  'reset'         : 0, # Resets the Priority Queue
  'mode'          : 0, # b2: Time limit, b1: Msg limit, b0 enable
  'clear'         : 0, # Clears counters and status
  'st_full'       : 0, # Channel Full flag (n..0) 
  'st_late'       : 0, # Late message detected
  'ebm_adr'       : 0, # Etherbone Master address
  'eca_adr'       : 0, # Event Condition Action Unit address
  'tx_max_msgs'   : 0, # Max msgs per packet
  'tx_max_wait'   : 0, # Max wait time for non empty packet
  'tx_rate_limit' : 0, # Max msgs per milliseconds
  'offs_late'     : 0, # Time offset before message is late
  'cnt_late'      : 0, # Sum of all late messages
  'ts_late'       : 0, # First late Timestamp
  'cnt_out_all'   : 0, # Sum of all outgoing messages
  }
