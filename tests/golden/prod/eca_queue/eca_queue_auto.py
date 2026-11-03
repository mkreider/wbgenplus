class eca_queue (object):
  ifname = 'slave'

  adrDict = {
  'queue_id_get'    : 0x0000000000000000000000000, # ro,  8 b, The index of a_channel_o from the ECA to which this queue is connected (set channel_select=queue_id+1)
  'pop_owr'         : 0x0000000000000000000000004, # wo,  1 b, Pop action from the channel's queue
  'flags_get'       : 0x0000000000000000000000008, # ro,  5 b, Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  'num_get'         : 0x000000000000000000000000c, # ro,  8 b, Subchannel target
  'event_id_hi_get' : 0x0000000000000000000000010, # ro, 32 b, Event ID (high word)
  'event_id_lo_get' : 0x0000000000000000000000014, # ro, 32 b, Event ID (low word)
  'param_hi_get'    : 0x0000000000000000000000018, # ro, 32 b, Parameter (high word)
  'param_lo_get'    : 0x000000000000000000000001c, # ro, 32 b, Parameter (low word)
  'tag_get'         : 0x0000000000000000000000020, # ro, 32 b, Tag from the condition
  'tef_get'         : 0x0000000000000000000000024, # ro, 32 b, Timing extension field
  'deadline_hi_get' : 0x0000000000000000000000028, # ro, 32 b, Deadline (high word)
  'deadline_lo_get' : 0x000000000000000000000002c, # ro, 32 b, Deadline (low word)
  'executed_hi_get' : 0x0000000000000000000000030, # ro, 32 b, Actual execution time (high word)
  'executed_lo_get' : 0x0000000000000000000000034, # ro, 32 b, Actual execution time (low word)
  }

  adrDict_reverse = {
  0x0000000000000000000000000 : 'queue_id_get', # ro,  8 b, The index of a_channel_o from the ECA to which this queue is connected (set channel_select=queue_id+1)
  0x0000000000000000000000004 : 'pop_owr', # wo,  1 b, Pop action from the channel's queue
  0x0000000000000000000000008 : 'flags_get', # ro,  5 b, Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  0x000000000000000000000000c : 'num_get', # ro,  8 b, Subchannel target
  0x0000000000000000000000010 : 'event_id_hi_get', # ro, 32 b, Event ID (high word)
  0x0000000000000000000000014 : 'event_id_lo_get', # ro, 32 b, Event ID (low word)
  0x0000000000000000000000018 : 'param_hi_get', # ro, 32 b, Parameter (high word)
  0x000000000000000000000001c : 'param_lo_get', # ro, 32 b, Parameter (low word)
  0x0000000000000000000000020 : 'tag_get', # ro, 32 b, Tag from the condition
  0x0000000000000000000000024 : 'tef_get', # ro, 32 b, Timing extension field
  0x0000000000000000000000028 : 'deadline_hi_get', # ro, 32 b, Deadline (high word)
  0x000000000000000000000002c : 'deadline_lo_get', # ro, 32 b, Deadline (low word)
  0x0000000000000000000000030 : 'executed_hi_get', # ro, 32 b, Actual execution time (high word)
  0x0000000000000000000000034 : 'executed_lo_get', # ro, 32 b, Actual execution time (low word)
  }

  flagDict = {
  'queue_id'    : 'r', # The index of a_channel_o from the ECA to which this queue is connected (set channel_select=queue_id+1)
  'pop'         : 'wp', # Pop action from the channel's queue
  'flags'       : 'rd', # Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  'num'         : 'rd', # Subchannel target
  'event_id_hi' : 'rd', # Event ID (high word)
  'event_id_lo' : 'rd', # Event ID (low word)
  'param_hi'    : 'rd', # Parameter (high word)
  'param_lo'    : 'rd', # Parameter (low word)
  'tag'         : 'rd', # Tag from the condition
  'tef'         : 'rd', # Timing extension field
  'deadline_hi' : 'rd', # Deadline (high word)
  'deadline_lo' : 'rd', # Deadline (low word)
  'executed_hi' : 'rd', # Actual execution time (high word)
  'executed_lo' : 'rd', # Actual execution time (low word)
  }

  valDict = {
  'queue_id'    : queue_id, # The index of a_channel_o from the ECA to which this queue is connected (set channel_select=queue_id+1)
  'pop'         : 0, # Pop action from the channel's queue
  'flags'       : 0, # Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  'num'         : 0, # Subchannel target
  'event_id_hi' : 0, # Event ID (high word)
  'event_id_lo' : 0, # Event ID (low word)
  'param_hi'    : 0, # Parameter (high word)
  'param_lo'    : 0, # Parameter (low word)
  'tag'         : 0, # Tag from the condition
  'tef'         : 0, # Timing extension field
  'deadline_hi' : 0, # Deadline (high word)
  'deadline_lo' : 0, # Deadline (low word)
  'executed_hi' : 0, # Actual execution time (high word)
  'executed_lo' : 0, # Actual execution time (low word)
  }
