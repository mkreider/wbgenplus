class eca_queue (object):
  ifname = 'slave'

  adrDict = {
  'queue_id_get'    : 0x00, # ro,  8 b, The index of a_channel_o from the ECA to which this queue is connected (set channel_select=queue_id+1)
  'pop_owr'         : 0x04, # wo,  1 b, Pop action from the channel's queue
  'flags_get'       : 0x08, # ro,  5 b, Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  'num_get'         : 0x0c, # ro,  8 b, Subchannel target
  'event_id_hi_get' : 0x10, # ro, 32 b, Event ID (high word)
  'event_id_lo_get' : 0x14, # ro, 32 b, Event ID (low word)
  'param_hi_get'    : 0x18, # ro, 32 b, Parameter (high word)
  'param_lo_get'    : 0x1c, # ro, 32 b, Parameter (low word)
  'tag_get'         : 0x20, # ro, 32 b, Tag from the condition
  'tef_get'         : 0x24, # ro, 32 b, Timing extension field
  'deadline_hi_get' : 0x28, # ro, 32 b, Deadline (high word)
  'deadline_lo_get' : 0x2c, # ro, 32 b, Deadline (low word)
  'executed_hi_get' : 0x30, # ro, 32 b, Actual execution time (high word)
  'executed_lo_get' : 0x34, # ro, 32 b, Actual execution time (low word)
  }

  adrDict_reverse = {
  0x00  : 'queue_id_get', # ro,  8 b, The index of a_channel_o from the ECA to which this queue is connected (set channel_select=queue_id+1)
  0x04  : 'pop_owr', # wo,  1 b, Pop action from the channel's queue
  0x08  : 'flags_get', # ro,  5 b, Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  0x0c  : 'num_get', # ro,  8 b, Subchannel target
  0x10  : 'event_id_hi_get', # ro, 32 b, Event ID (high word)
  0x14  : 'event_id_lo_get', # ro, 32 b, Event ID (low word)
  0x18  : 'param_hi_get', # ro, 32 b, Parameter (high word)
  0x1c  : 'param_lo_get', # ro, 32 b, Parameter (low word)
  0x20  : 'tag_get', # ro, 32 b, Tag from the condition
  0x24  : 'tef_get', # ro, 32 b, Timing extension field
  0x28  : 'deadline_hi_get', # ro, 32 b, Deadline (high word)
  0x2c  : 'deadline_lo_get', # ro, 32 b, Deadline (low word)
  0x30  : 'executed_hi_get', # ro, 32 b, Actual execution time (high word)
  0x34  : 'executed_lo_get', # ro, 32 b, Actual execution time (low word)
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
