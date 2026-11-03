class eca (object):
  ifname = 'slave'

  adrDict = {
  'channels_get'                : 0x000000000000000000000000000000000000000000000000000000000000000000000000000, # ro,  8 b, Number of channels implemented by the ECA, including the internal IO channel #0
  'search_capacity_get'         : 0x000000000000000000000000000000000000000000000000000000000000000000000000004, # ro, 16 b, Total number of search table entries per active page
  'walker_capacity_get'         : 0x000000000000000000000000000000000000000000000000000000000000000000000000008, # ro, 16 b, Total number of walker table entries per active page
  'latency_get'                 : 0x00000000000000000000000000000000000000000000000000000000000000000000000000c, # ro, 32 b, Delay in ticks (typically nanoseconds) between an event's arrival at the ECA and its earliest possible execution as an action
  'offset_bits_get'             : 0x000000000000000000000000000000000000000000000000000000000000000000000000010, # ro,  8 b, Actions scheduled for execution with a delay in ticks exceeding offset_bits are executed early
  'flip_active_owr'             : 0x000000000000000000000000000000000000000000000000000000000000000000000000014, # wo,  1 b, Flip the active search and walker tables with the inactive tables
  'time_hi_get'                 : 0x000000000000000000000000000000000000000000000000000000000000000000000000018, # ro, 32 b, Ticks (nanoseconds) since Jan 1, 1970 (high word)
  'time_lo_get'                 : 0x00000000000000000000000000000000000000000000000000000000000000000000000001c, # ro, 32 b, Ticks (nanoseconds) since Jan 1, 1970 (low word)
  'search_select_rw'            : 0x000000000000000000000000000000000000000000000000000000000000000000000000020, # rw, 16 b, Read/write this record in the inactive search table
  'search_rw_first_rw'          : 0x000000000000000000000000000000000000000000000000000000000000000000000000024, # rw, 16 b, Scratch register to be written to search_ro_first
  'search_rw_event_hi_rw'       : 0x000000000000000000000000000000000000000000000000000000000000000000000000028, # rw, 32 b, Scratch register to be written to search_ro_event_hi
  'search_rw_event_lo_rw'       : 0x00000000000000000000000000000000000000000000000000000000000000000000000002c, # rw, 32 b, Scratch register to be written to search_ro_event_lo
  'search_write_owr'            : 0x000000000000000000000000000000000000000000000000000000000000000000000000030, # wo,  1 b, Store the scratch registers to the inactive search table record search_select
  'search_ro_first_get'         : 0x000000000000000000000000000000000000000000000000000000000000000000000000034, # ro, 16 b, The first walker entry to execute if an event matches this record in the search table
  'search_ro_event_hi_get'      : 0x000000000000000000000000000000000000000000000000000000000000000000000000038, # ro, 32 b, Event IDs greater than or equal to this value match this search table record (high word)
  'search_ro_event_lo_get'      : 0x00000000000000000000000000000000000000000000000000000000000000000000000003c, # ro, 32 b, Event IDs greater than or equal to this value match this search table record (low word)
  'walker_select_rw'            : 0x000000000000000000000000000000000000000000000000000000000000000000000000040, # rw, 16 b, Read/write this record in the inactive walker table
  'walker_rw_next_rw'           : 0x000000000000000000000000000000000000000000000000000000000000000000000000044, # rw, 16 b, Scratch register to be written to walker_ro_next
  'walker_rw_offset_hi_rw'      : 0x000000000000000000000000000000000000000000000000000000000000000000000000048, # rw, 32 b, Scratch register to be written to walker_ro_offset_hi
  'walker_rw_offset_lo_rw'      : 0x00000000000000000000000000000000000000000000000000000000000000000000000004c, # rw, 32 b, Scratch register to be written to walker_ro_offset_lo
  'walker_rw_tag_rw'            : 0x000000000000000000000000000000000000000000000000000000000000000000000000050, # rw, 32 b, Scratch register to be written to walker_ro_tag
  'walker_rw_flags_rw'          : 0x000000000000000000000000000000000000000000000000000000000000000000000000054, # rw,  4 b, Scratch register to be written to walker_ro_flags
  'walker_rw_channel_rw'        : 0x000000000000000000000000000000000000000000000000000000000000000000000000058, # rw,  8 b, Scratch register to be written to walker_ro_channel
  'walker_rw_num_rw'            : 0x00000000000000000000000000000000000000000000000000000000000000000000000005c, # rw,  8 b, Scratch register to be written to walker_ro_num
  'walker_write_owr'            : 0x000000000000000000000000000000000000000000000000000000000000000000000000060, # wo,  1 b, Store the scratch registers to the inactive walker table record walker_select
  'walker_ro_next_get'          : 0x000000000000000000000000000000000000000000000000000000000000000000000000064, # ro, 16 b, The next walker entry to execute after this record (0xffff = end of list)
  'walker_ro_offset_hi_get'     : 0x000000000000000000000000000000000000000000000000000000000000000000000000068, # ro, 32 b, The resulting action's deadline is the event timestamp plus this offset (high word)
  'walker_ro_offset_lo_get'     : 0x00000000000000000000000000000000000000000000000000000000000000000000000006c, # ro, 32 b, The resulting action's deadline is the event timestamp plus this offset (low word)
  'walker_ro_tag_get'           : 0x000000000000000000000000000000000000000000000000000000000000000000000000070, # ro, 32 b, The resulting actions's tag
  'walker_ro_flags_get'         : 0x000000000000000000000000000000000000000000000000000000000000000000000000074, # ro,  4 b, Execute the resulting action even if it suffers from the errors set in this flag register
  'walker_ro_channel_get'       : 0x000000000000000000000000000000000000000000000000000000000000000000000000078, # ro,  8 b, The channel to which the resulting action will be sent
  'walker_ro_num_get'           : 0x00000000000000000000000000000000000000000000000000000000000000000000000007c, # ro,  8 b, The subchannel to which the resulting action will be sent
  'channel_select_rw'           : 0x000000000000000000000000000000000000000000000000000000000000000000000000080, # rw,  8 b, Read/clear this channel
  'channel_num_select_rw'       : 0x000000000000000000000000000000000000000000000000000000000000000000000000084, # rw,  8 b, Read/clear this subchannel
  'channel_code_select_rw'      : 0x000000000000000000000000000000000000000000000000000000000000000000000000088, # rw,  2 b, Read/clear this error condition (0=late, 1=early, 2=conflict, 3=delayed)
  'channel_type_get'            : 0x000000000000000000000000000000000000000000000000000000000000000000000000090, # ro, 32 b, Type of the selected channel (0=io, 1=linux, 2=wbm, ...)
  'channel_max_num_get'         : 0x000000000000000000000000000000000000000000000000000000000000000000000000094, # ro,  8 b, Total number of subchannels supported by the selected channel
  'channel_capacity_get'        : 0x000000000000000000000000000000000000000000000000000000000000000000000000098, # ro, 16 b, Total number of actions which may be enqueued by the selected channel at a time
  'channel_msi_set_enable_owr'  : 0x00000000000000000000000000000000000000000000000000000000000000000000000009c, # wo,  1 b, Turn on/off MSI messages for the selected channel
  'channel_msi_get_enable_get'  : 0x0000000000000000000000000000000000000000000000000000000000000000000000000a0, # ro,  1 b, Check if MSI messages are enabled for the selected channel
  'channel_msi_set_target_owr'  : 0x0000000000000000000000000000000000000000000000000000000000000000000000000a4, # wo, 32 b, Set the destination MSI address for the selected channel (only possible while it has MSIs disabled)
  'channel_msi_get_target_get'  : 0x0000000000000000000000000000000000000000000000000000000000000000000000000a8, # ro, 32 b, Get the destination MSI address for the selected channel
  'channel_mostfull_ack_get'    : 0x0000000000000000000000000000000000000000000000000000000000000000000000000ac, # ro, 32 b, Read the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  'channel_mostfull_clear_get'  : 0x0000000000000000000000000000000000000000000000000000000000000000000000000b0, # ro, 32 b, Read and clear the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  'channel_valid_count_get'     : 0x0000000000000000000000000000000000000000000000000000000000000000000000000b4, # ro, 32 b, Read and clear the number of actions output by the selected subchannel, MSI=(4<<16|num) will be sent when the count becomes non-zero
  'channel_overflow_count_get'  : 0x0000000000000000000000000000000000000000000000000000000000000000000000000b8, # ro, 32 b, Read and clear the number of actions which could not be enqueued to the selected full channel which were destined for the selected subchannel, MSI=(5<<16|num) will be sent when the count becomes non-zero
  'channel_failed_count_get'    : 0x0000000000000000000000000000000000000000000000000000000000000000000000000bc, # ro, 32 b, Read and clear the number of actions with the selected error code which were destined for the selected subchannel, MSI=(code<<16|num) will be sent when the count becomes non-zero
  'channel_event_id_hi_get'     : 0x0000000000000000000000000000000000000000000000000000000000000000000000000c0, # ro, 32 b, The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_event_id_lo_get'     : 0x0000000000000000000000000000000000000000000000000000000000000000000000000c4, # ro, 32 b, The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_param_hi_get'        : 0x0000000000000000000000000000000000000000000000000000000000000000000000000c8, # ro, 32 b, The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_param_lo_get'        : 0x0000000000000000000000000000000000000000000000000000000000000000000000000cc, # ro, 32 b, The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_tag_get'             : 0x0000000000000000000000000000000000000000000000000000000000000000000000000d0, # ro, 32 b, The tag of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  'channel_tef_get'             : 0x0000000000000000000000000000000000000000000000000000000000000000000000000d4, # ro, 32 b, The TEF of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  'channel_deadline_hi_get'     : 0x0000000000000000000000000000000000000000000000000000000000000000000000000d8, # ro, 32 b, The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_deadline_lo_get'     : 0x0000000000000000000000000000000000000000000000000000000000000000000000000dc, # ro, 32 b, The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_executed_hi_get'     : 0x0000000000000000000000000000000000000000000000000000000000000000000000000e0, # ro, 32 b, The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_executed_lo_get'     : 0x0000000000000000000000000000000000000000000000000000000000000000000000000e4, # ro, 32 b, The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  }

  adrDict_reverse = {
  0x000000000000000000000000000000000000000000000000000000000000000000000000000 : 'channels_get', # ro,  8 b, Number of channels implemented by the ECA, including the internal IO channel #0
  0x000000000000000000000000000000000000000000000000000000000000000000000000004 : 'search_capacity_get', # ro, 16 b, Total number of search table entries per active page
  0x000000000000000000000000000000000000000000000000000000000000000000000000008 : 'walker_capacity_get', # ro, 16 b, Total number of walker table entries per active page
  0x00000000000000000000000000000000000000000000000000000000000000000000000000c : 'latency_get', # ro, 32 b, Delay in ticks (typically nanoseconds) between an event's arrival at the ECA and its earliest possible execution as an action
  0x000000000000000000000000000000000000000000000000000000000000000000000000010 : 'offset_bits_get', # ro,  8 b, Actions scheduled for execution with a delay in ticks exceeding offset_bits are executed early
  0x000000000000000000000000000000000000000000000000000000000000000000000000014 : 'flip_active_owr', # wo,  1 b, Flip the active search and walker tables with the inactive tables
  0x000000000000000000000000000000000000000000000000000000000000000000000000018 : 'time_hi_get', # ro, 32 b, Ticks (nanoseconds) since Jan 1, 1970 (high word)
  0x00000000000000000000000000000000000000000000000000000000000000000000000001c : 'time_lo_get', # ro, 32 b, Ticks (nanoseconds) since Jan 1, 1970 (low word)
  0x000000000000000000000000000000000000000000000000000000000000000000000000020 : 'search_select_rw', # rw, 16 b, Read/write this record in the inactive search table
  0x000000000000000000000000000000000000000000000000000000000000000000000000024 : 'search_rw_first_rw', # rw, 16 b, Scratch register to be written to search_ro_first
  0x000000000000000000000000000000000000000000000000000000000000000000000000028 : 'search_rw_event_hi_rw', # rw, 32 b, Scratch register to be written to search_ro_event_hi
  0x00000000000000000000000000000000000000000000000000000000000000000000000002c : 'search_rw_event_lo_rw', # rw, 32 b, Scratch register to be written to search_ro_event_lo
  0x000000000000000000000000000000000000000000000000000000000000000000000000030 : 'search_write_owr', # wo,  1 b, Store the scratch registers to the inactive search table record search_select
  0x000000000000000000000000000000000000000000000000000000000000000000000000034 : 'search_ro_first_get', # ro, 16 b, The first walker entry to execute if an event matches this record in the search table
  0x000000000000000000000000000000000000000000000000000000000000000000000000038 : 'search_ro_event_hi_get', # ro, 32 b, Event IDs greater than or equal to this value match this search table record (high word)
  0x00000000000000000000000000000000000000000000000000000000000000000000000003c : 'search_ro_event_lo_get', # ro, 32 b, Event IDs greater than or equal to this value match this search table record (low word)
  0x000000000000000000000000000000000000000000000000000000000000000000000000040 : 'walker_select_rw', # rw, 16 b, Read/write this record in the inactive walker table
  0x000000000000000000000000000000000000000000000000000000000000000000000000044 : 'walker_rw_next_rw', # rw, 16 b, Scratch register to be written to walker_ro_next
  0x000000000000000000000000000000000000000000000000000000000000000000000000048 : 'walker_rw_offset_hi_rw', # rw, 32 b, Scratch register to be written to walker_ro_offset_hi
  0x00000000000000000000000000000000000000000000000000000000000000000000000004c : 'walker_rw_offset_lo_rw', # rw, 32 b, Scratch register to be written to walker_ro_offset_lo
  0x000000000000000000000000000000000000000000000000000000000000000000000000050 : 'walker_rw_tag_rw', # rw, 32 b, Scratch register to be written to walker_ro_tag
  0x000000000000000000000000000000000000000000000000000000000000000000000000054 : 'walker_rw_flags_rw', # rw,  4 b, Scratch register to be written to walker_ro_flags
  0x000000000000000000000000000000000000000000000000000000000000000000000000058 : 'walker_rw_channel_rw', # rw,  8 b, Scratch register to be written to walker_ro_channel
  0x00000000000000000000000000000000000000000000000000000000000000000000000005c : 'walker_rw_num_rw', # rw,  8 b, Scratch register to be written to walker_ro_num
  0x000000000000000000000000000000000000000000000000000000000000000000000000060 : 'walker_write_owr', # wo,  1 b, Store the scratch registers to the inactive walker table record walker_select
  0x000000000000000000000000000000000000000000000000000000000000000000000000064 : 'walker_ro_next_get', # ro, 16 b, The next walker entry to execute after this record (0xffff = end of list)
  0x000000000000000000000000000000000000000000000000000000000000000000000000068 : 'walker_ro_offset_hi_get', # ro, 32 b, The resulting action's deadline is the event timestamp plus this offset (high word)
  0x00000000000000000000000000000000000000000000000000000000000000000000000006c : 'walker_ro_offset_lo_get', # ro, 32 b, The resulting action's deadline is the event timestamp plus this offset (low word)
  0x000000000000000000000000000000000000000000000000000000000000000000000000070 : 'walker_ro_tag_get', # ro, 32 b, The resulting actions's tag
  0x000000000000000000000000000000000000000000000000000000000000000000000000074 : 'walker_ro_flags_get', # ro,  4 b, Execute the resulting action even if it suffers from the errors set in this flag register
  0x000000000000000000000000000000000000000000000000000000000000000000000000078 : 'walker_ro_channel_get', # ro,  8 b, The channel to which the resulting action will be sent
  0x00000000000000000000000000000000000000000000000000000000000000000000000007c : 'walker_ro_num_get', # ro,  8 b, The subchannel to which the resulting action will be sent
  0x000000000000000000000000000000000000000000000000000000000000000000000000080 : 'channel_select_rw', # rw,  8 b, Read/clear this channel
  0x000000000000000000000000000000000000000000000000000000000000000000000000084 : 'channel_num_select_rw', # rw,  8 b, Read/clear this subchannel
  0x000000000000000000000000000000000000000000000000000000000000000000000000088 : 'channel_code_select_rw', # rw,  2 b, Read/clear this error condition (0=late, 1=early, 2=conflict, 3=delayed)
  0x000000000000000000000000000000000000000000000000000000000000000000000000090 : 'channel_type_get', # ro, 32 b, Type of the selected channel (0=io, 1=linux, 2=wbm, ...)
  0x000000000000000000000000000000000000000000000000000000000000000000000000094 : 'channel_max_num_get', # ro,  8 b, Total number of subchannels supported by the selected channel
  0x000000000000000000000000000000000000000000000000000000000000000000000000098 : 'channel_capacity_get', # ro, 16 b, Total number of actions which may be enqueued by the selected channel at a time
  0x00000000000000000000000000000000000000000000000000000000000000000000000009c : 'channel_msi_set_enable_owr', # wo,  1 b, Turn on/off MSI messages for the selected channel
  0x0000000000000000000000000000000000000000000000000000000000000000000000000a0 : 'channel_msi_get_enable_get', # ro,  1 b, Check if MSI messages are enabled for the selected channel
  0x0000000000000000000000000000000000000000000000000000000000000000000000000a4 : 'channel_msi_set_target_owr', # wo, 32 b, Set the destination MSI address for the selected channel (only possible while it has MSIs disabled)
  0x0000000000000000000000000000000000000000000000000000000000000000000000000a8 : 'channel_msi_get_target_get', # ro, 32 b, Get the destination MSI address for the selected channel
  0x0000000000000000000000000000000000000000000000000000000000000000000000000ac : 'channel_mostfull_ack_get', # ro, 32 b, Read the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  0x0000000000000000000000000000000000000000000000000000000000000000000000000b0 : 'channel_mostfull_clear_get', # ro, 32 b, Read and clear the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  0x0000000000000000000000000000000000000000000000000000000000000000000000000b4 : 'channel_valid_count_get', # ro, 32 b, Read and clear the number of actions output by the selected subchannel, MSI=(4<<16|num) will be sent when the count becomes non-zero
  0x0000000000000000000000000000000000000000000000000000000000000000000000000b8 : 'channel_overflow_count_get', # ro, 32 b, Read and clear the number of actions which could not be enqueued to the selected full channel which were destined for the selected subchannel, MSI=(5<<16|num) will be sent when the count becomes non-zero
  0x0000000000000000000000000000000000000000000000000000000000000000000000000bc : 'channel_failed_count_get', # ro, 32 b, Read and clear the number of actions with the selected error code which were destined for the selected subchannel, MSI=(code<<16|num) will be sent when the count becomes non-zero
  0x0000000000000000000000000000000000000000000000000000000000000000000000000c0 : 'channel_event_id_hi_get', # ro, 32 b, The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  0x0000000000000000000000000000000000000000000000000000000000000000000000000c4 : 'channel_event_id_lo_get', # ro, 32 b, The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  0x0000000000000000000000000000000000000000000000000000000000000000000000000c8 : 'channel_param_hi_get', # ro, 32 b, The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  0x0000000000000000000000000000000000000000000000000000000000000000000000000cc : 'channel_param_lo_get', # ro, 32 b, The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  0x0000000000000000000000000000000000000000000000000000000000000000000000000d0 : 'channel_tag_get', # ro, 32 b, The tag of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  0x0000000000000000000000000000000000000000000000000000000000000000000000000d4 : 'channel_tef_get', # ro, 32 b, The TEF of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  0x0000000000000000000000000000000000000000000000000000000000000000000000000d8 : 'channel_deadline_hi_get', # ro, 32 b, The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  0x0000000000000000000000000000000000000000000000000000000000000000000000000dc : 'channel_deadline_lo_get', # ro, 32 b, The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  0x0000000000000000000000000000000000000000000000000000000000000000000000000e0 : 'channel_executed_hi_get', # ro, 32 b, The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  0x0000000000000000000000000000000000000000000000000000000000000000000000000e4 : 'channel_executed_lo_get', # ro, 32 b, The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  }

  flagDict = {
  'channels'                : 'r', # Number of channels implemented by the ECA, including the internal IO channel #0
  'search_capacity'         : 'r', # Total number of search table entries per active page
  'walker_capacity'         : 'r', # Total number of walker table entries per active page
  'latency'                 : 'r', # Delay in ticks (typically nanoseconds) between an event's arrival at the ECA and its earliest possible execution as an action
  'offset_bits'             : 'r', # Actions scheduled for execution with a delay in ticks exceeding offset_bits are executed early
  'flip_active'             : 'wp', # Flip the active search and walker tables with the inactive tables
  'time_hi'                 : 'rd', # Ticks (nanoseconds) since Jan 1, 1970 (high word)
  'time_lo'                 : 'rd', # Ticks (nanoseconds) since Jan 1, 1970 (low word)
  'search_select'           : 'rwf', # Read/write this record in the inactive search table
  'search_rw_first'         : 'rw', # Scratch register to be written to search_ro_first
  'search_rw_event_hi'      : 'rw', # Scratch register to be written to search_ro_event_hi
  'search_rw_event_lo'      : 'rw', # Scratch register to be written to search_ro_event_lo
  'search_write'            : 'wp', # Store the scratch registers to the inactive search table record search_select
  'search_ro_first'         : 'rd', # The first walker entry to execute if an event matches this record in the search table
  'search_ro_event_hi'      : 'rd', # Event IDs greater than or equal to this value match this search table record (high word)
  'search_ro_event_lo'      : 'rd', # Event IDs greater than or equal to this value match this search table record (low word)
  'walker_select'           : 'rwf', # Read/write this record in the inactive walker table
  'walker_rw_next'          : 'rw', # Scratch register to be written to walker_ro_next
  'walker_rw_offset_hi'     : 'rw', # Scratch register to be written to walker_ro_offset_hi
  'walker_rw_offset_lo'     : 'rw', # Scratch register to be written to walker_ro_offset_lo
  'walker_rw_tag'           : 'rw', # Scratch register to be written to walker_ro_tag
  'walker_rw_flags'         : 'rw', # Scratch register to be written to walker_ro_flags
  'walker_rw_channel'       : 'rw', # Scratch register to be written to walker_ro_channel
  'walker_rw_num'           : 'rw', # Scratch register to be written to walker_ro_num
  'walker_write'            : 'wp', # Store the scratch registers to the inactive walker table record walker_select
  'walker_ro_next'          : 'rd', # The next walker entry to execute after this record (0xffff = end of list)
  'walker_ro_offset_hi'     : 'rd', # The resulting action's deadline is the event timestamp plus this offset (high word)
  'walker_ro_offset_lo'     : 'rd', # The resulting action's deadline is the event timestamp plus this offset (low word)
  'walker_ro_tag'           : 'rd', # The resulting actions's tag
  'walker_ro_flags'         : 'rd', # Execute the resulting action even if it suffers from the errors set in this flag register
  'walker_ro_channel'       : 'rd', # The channel to which the resulting action will be sent
  'walker_ro_num'           : 'rd', # The subchannel to which the resulting action will be sent
  'channel_select'          : 'rwf', # Read/clear this channel
  'channel_num_select'      : 'rw', # Read/clear this subchannel
  'channel_code_select'     : 'rw', # Read/clear this error condition (0=late, 1=early, 2=conflict, 3=delayed)
  'reserved'                : '', # reserved
  'channel_type'            : 'rd', # Type of the selected channel (0=io, 1=linux, 2=wbm, ...)
  'channel_max_num'         : 'rd', # Total number of subchannels supported by the selected channel
  'channel_capacity'        : 'rd', # Total number of actions which may be enqueued by the selected channel at a time
  'channel_msi_set_enable'  : 'wf', # Turn on/off MSI messages for the selected channel
  'channel_msi_get_enable'  : 'rd', # Check if MSI messages are enabled for the selected channel
  'channel_msi_set_target'  : 'wf', # Set the destination MSI address for the selected channel (only possible while it has MSIs disabled)
  'channel_msi_get_target'  : 'rd', # Get the destination MSI address for the selected channel
  'channel_mostfull_ack'    : 'rdf', # Read the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  'channel_mostfull_clear'  : 'rdf', # Read and clear the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  'channel_valid_count'     : 'rdf', # Read and clear the number of actions output by the selected subchannel, MSI=(4<<16|num) will be sent when the count becomes non-zero
  'channel_overflow_count'  : 'rdf', # Read and clear the number of actions which could not be enqueued to the selected full channel which were destined for the selected subchannel, MSI=(5<<16|num) will be sent when the count becomes non-zero
  'channel_failed_count'    : 'rdf', # Read and clear the number of actions with the selected error code which were destined for the selected subchannel, MSI=(code<<16|num) will be sent when the count becomes non-zero
  'channel_event_id_hi'     : 'rdf', # The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_event_id_lo'     : 'rdf', # The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_param_hi'        : 'rdf', # The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_param_lo'        : 'rdf', # The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_tag'             : 'rdf', # The tag of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  'channel_tef'             : 'rdf', # The TEF of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  'channel_deadline_hi'     : 'rdf', # The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_deadline_lo'     : 'rdf', # The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_executed_hi'     : 'rdf', # The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_executed_lo'     : 'rdf', # The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  }

  valDict = {
  'channels'                : channels, # Number of channels implemented by the ECA, including the internal IO channel #0
  'search_capacity'         : search_capacity, # Total number of search table entries per active page
  'walker_capacity'         : walker_capacity, # Total number of walker table entries per active page
  'latency'                 : latency, # Delay in ticks (typically nanoseconds) between an event's arrival at the ECA and its earliest possible execution as an action
  'offset_bits'             : offset_bits, # Actions scheduled for execution with a delay in ticks exceeding offset_bits are executed early
  'flip_active'             : 0, # Flip the active search and walker tables with the inactive tables
  'time_hi'                 : 0, # Ticks (nanoseconds) since Jan 1, 1970 (high word)
  'time_lo'                 : 0, # Ticks (nanoseconds) since Jan 1, 1970 (low word)
  'search_select'           : 0, # Read/write this record in the inactive search table
  'search_rw_first'         : 0, # Scratch register to be written to search_ro_first
  'search_rw_event_hi'      : 0, # Scratch register to be written to search_ro_event_hi
  'search_rw_event_lo'      : 0, # Scratch register to be written to search_ro_event_lo
  'search_write'            : 0, # Store the scratch registers to the inactive search table record search_select
  'search_ro_first'         : 0, # The first walker entry to execute if an event matches this record in the search table
  'search_ro_event_hi'      : 0, # Event IDs greater than or equal to this value match this search table record (high word)
  'search_ro_event_lo'      : 0, # Event IDs greater than or equal to this value match this search table record (low word)
  'walker_select'           : 0, # Read/write this record in the inactive walker table
  'walker_rw_next'          : 0, # Scratch register to be written to walker_ro_next
  'walker_rw_offset_hi'     : 0, # Scratch register to be written to walker_ro_offset_hi
  'walker_rw_offset_lo'     : 0, # Scratch register to be written to walker_ro_offset_lo
  'walker_rw_tag'           : 0, # Scratch register to be written to walker_ro_tag
  'walker_rw_flags'         : 0, # Scratch register to be written to walker_ro_flags
  'walker_rw_channel'       : 0, # Scratch register to be written to walker_ro_channel
  'walker_rw_num'           : 0, # Scratch register to be written to walker_ro_num
  'walker_write'            : 0, # Store the scratch registers to the inactive walker table record walker_select
  'walker_ro_next'          : 0, # The next walker entry to execute after this record (0xffff = end of list)
  'walker_ro_offset_hi'     : 0, # The resulting action's deadline is the event timestamp plus this offset (high word)
  'walker_ro_offset_lo'     : 0, # The resulting action's deadline is the event timestamp plus this offset (low word)
  'walker_ro_tag'           : 0, # The resulting actions's tag
  'walker_ro_flags'         : 0, # Execute the resulting action even if it suffers from the errors set in this flag register
  'walker_ro_channel'       : 0, # The channel to which the resulting action will be sent
  'walker_ro_num'           : 0, # The subchannel to which the resulting action will be sent
  'channel_select'          : 0, # Read/clear this channel
  'channel_num_select'      : 0, # Read/clear this subchannel
  'channel_code_select'     : 0, # Read/clear this error condition (0=late, 1=early, 2=conflict, 3=delayed)
  'reserved'                : 0, # reserved
  'channel_type'            : 0, # Type of the selected channel (0=io, 1=linux, 2=wbm, ...)
  'channel_max_num'         : 0, # Total number of subchannels supported by the selected channel
  'channel_capacity'        : 0, # Total number of actions which may be enqueued by the selected channel at a time
  'channel_msi_set_enable'  : 0, # Turn on/off MSI messages for the selected channel
  'channel_msi_get_enable'  : 0, # Check if MSI messages are enabled for the selected channel
  'channel_msi_set_target'  : 0, # Set the destination MSI address for the selected channel (only possible while it has MSIs disabled)
  'channel_msi_get_target'  : 0, # Get the destination MSI address for the selected channel
  'channel_mostfull_ack'    : 0, # Read the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  'channel_mostfull_clear'  : 0, # Read and clear the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  'channel_valid_count'     : 0, # Read and clear the number of actions output by the selected subchannel, MSI=(4<<16|num) will be sent when the count becomes non-zero
  'channel_overflow_count'  : 0, # Read and clear the number of actions which could not be enqueued to the selected full channel which were destined for the selected subchannel, MSI=(5<<16|num) will be sent when the count becomes non-zero
  'channel_failed_count'    : 0, # Read and clear the number of actions with the selected error code which were destined for the selected subchannel, MSI=(code<<16|num) will be sent when the count becomes non-zero
  'channel_event_id_hi'     : 0, # The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_event_id_lo'     : 0, # The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_param_hi'        : 0, # The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_param_lo'        : 0, # The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_tag'             : 0, # The tag of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  'channel_tef'             : 0, # The TEF of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  'channel_deadline_hi'     : 0, # The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_deadline_lo'     : 0, # The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  'channel_executed_hi'     : 0, # The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  'channel_executed_lo'     : 0, # The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  }
