class eca_tlu (object):
  ifname = 'slave'

  adrDict = {
  'num_inputs_get'  : 0x00, # ro,  8 b, Total number of inputs attached to the TLU
  'input_select_rw' : 0x04, # rw,  8 b, Write the configuration of this input
  'enable_rw'       : 0x08, # rw,  1 b, Will this input generate timing events on an edge
  'stable_rw'       : 0x0c, # rw, 32 b, Signal must be high/low for stable cycles to be counted as a valid transition
  'event_hi_rw'     : 0x10, # rw, 32 b, Timing Event to generate (high word)
  'event_lo_rw'     : 0x14, # rw, 32 b, Timing Event to generate (low word), lowest bit is replaced with the edge of the transition
  'write_owr'       : 0x18, # wo,  1 b, Write register contents to TLU configuration
  }

  adrDict_reverse = {
  0x00  : 'num_inputs_get', # ro,  8 b, Total number of inputs attached to the TLU
  0x04  : 'input_select_rw', # rw,  8 b, Write the configuration of this input
  0x08  : 'enable_rw', # rw,  1 b, Will this input generate timing events on an edge
  0x0c  : 'stable_rw', # rw, 32 b, Signal must be high/low for stable cycles to be counted as a valid transition
  0x10  : 'event_hi_rw', # rw, 32 b, Timing Event to generate (high word)
  0x14  : 'event_lo_rw', # rw, 32 b, Timing Event to generate (low word), lowest bit is replaced with the edge of the transition
  0x18  : 'write_owr', # wo,  1 b, Write register contents to TLU configuration
  }

  flagDict = {
  'num_inputs'    : 'r', # Total number of inputs attached to the TLU
  'input_select'  : 'rw', # Write the configuration of this input
  'enable'        : 'rw', # Will this input generate timing events on an edge
  'stable'        : 'rw', # Signal must be high/low for stable cycles to be counted as a valid transition
  'event_hi'      : 'rw', # Timing Event to generate (high word)
  'event_lo'      : 'rw', # Timing Event to generate (low word), lowest bit is replaced with the edge of the transition
  'write'         : 'wp', # Write register contents to TLU configuration
  }

  valDict = {
  'num_inputs'    : num_inputs, # Total number of inputs attached to the TLU
  'input_select'  : 0, # Write the configuration of this input
  'enable'        : 0, # Will this input generate timing events on an edge
  'stable'        : 0, # Signal must be high/low for stable cycles to be counted as a valid transition
  'event_hi'      : 0, # Timing Event to generate (high word)
  'event_lo'      : 0, # Timing Event to generate (low word), lowest bit is replaced with the edge of the transition
  'write'         : 0, # Write register contents to TLU configuration
  }
