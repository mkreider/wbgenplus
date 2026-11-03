class ebm (object):
  ifname = 'slave'

  adrDict = {
  'clear_owr'     : 0x0000000000000000000000000, # wo,             1 b, Clears EBM buffers
  'flush_owr'     : 0x0000000000000000000000004, # wo,             1 b, Send stored data as an EB packet
  'status_get'    : 0x0000000000000000000000008, # ro,            32 b, Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  'src_mac_rw_0'  : 0x000000000000000000000000c, # rw,            32 b, Source MAC address
  'src_mac_rw_1'  : 0x0000000000000000000000010, # rw,            16 b, Source MAC address
  'src_ip_rw'     : 0x0000000000000000000000014, # rw,            32 b, Source IPV4 address
  'src_port_rw'   : 0x0000000000000000000000018, # rw,            16 b, Source port number
  'dst_mac_rw_0'  : 0x000000000000000000000001c, # rw,            32 b, Destination MAC address
  'dst_mac_rw_1'  : 0x0000000000000000000000020, # rw,            16 b, Destination MAC address
  'dst_ip_rw'     : 0x0000000000000000000000024, # rw,            32 b, Destination IPV4 address
  'dst_port_rw'   : 0x0000000000000000000000028, # rw,            16 b, Destination port number
  'mtu_rw'        : 0x000000000000000000000002c, # rw,            16 b, Maximum packet size
  'adr_hi_rw'     : 0x0000000000000000000000030, # rw, g_adr_bits_hi b, High Address bits inserted into WB operations
  'eb_opt_rw'     : 0x0000000000000000000000034, # rw,            32 b, Default Record Header Options for current transaction
  'sema_rw'       : 0x0000000000000000000000038, # rw,            32 b, Semaphore register in case multiple users want access
  'udp_raw_rw'    : 0x000000000000000000000003c, # rw,             1 b, If this Flag is set, you can create raw udp packets by writing to udp_data
  'udp_data_owr'  : 0x0000000000000000000000040, # wo,            16 b, Raw udp Data input
  }

  adrDict_reverse = {
  0x0000000000000000000000000 : 'clear_owr', # wo,             1 b, Clears EBM buffers
  0x0000000000000000000000004 : 'flush_owr', # wo,             1 b, Send stored data as an EB packet
  0x0000000000000000000000008 : 'status_get', # ro,            32 b, Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  0x000000000000000000000000c : 'src_mac_rw_0', # rw,            32 b, Source MAC address
  0x0000000000000000000000010 : 'src_mac_rw_1', # rw,            16 b, Source MAC address
  0x0000000000000000000000014 : 'src_ip_rw', # rw,            32 b, Source IPV4 address
  0x0000000000000000000000018 : 'src_port_rw', # rw,            16 b, Source port number
  0x000000000000000000000001c : 'dst_mac_rw_0', # rw,            32 b, Destination MAC address
  0x0000000000000000000000020 : 'dst_mac_rw_1', # rw,            16 b, Destination MAC address
  0x0000000000000000000000024 : 'dst_ip_rw', # rw,            32 b, Destination IPV4 address
  0x0000000000000000000000028 : 'dst_port_rw', # rw,            16 b, Destination port number
  0x000000000000000000000002c : 'mtu_rw', # rw,            16 b, Maximum packet size
  0x0000000000000000000000030 : 'adr_hi_rw', # rw, g_adr_bits_hi b, High Address bits inserted into WB operations
  0x0000000000000000000000034 : 'eb_opt_rw', # rw,            32 b, Default Record Header Options for current transaction
  0x0000000000000000000000038 : 'sema_rw', # rw,            32 b, Semaphore register in case multiple users want access
  0x000000000000000000000003c : 'udp_raw_rw', # rw,             1 b, If this Flag is set, you can create raw udp packets by writing to udp_data
  0x0000000000000000000000040 : 'udp_data_owr', # wo,            16 b, Raw udp Data input
  }

  flagDict = {
  'clear'     : 'wp', # Clears EBM buffers
  'flush'     : 'wp', # Send stored data as an EB packet
  'status'    : 'rd', # Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  'src_mac'   : 'rw', # Source MAC address
  'src_ip'    : 'rw', # Source IPV4 address
  'src_port'  : 'rw', # Source port number
  'dst_mac'   : 'rw', # Destination MAC address
  'dst_ip'    : 'rw', # Destination IPV4 address
  'dst_port'  : 'rw', # Destination port number
  'mtu'       : 'rw', # Maximum packet size
  'adr_hi'    : 'rw', # High Address bits inserted into WB operations
  'eb_opt'    : 'rw', # Default Record Header Options for current transaction
  'sema'      : 'rw', # Semaphore register in case multiple users want access
  'udp_raw'   : 'rw', # If this Flag is set, you can create raw udp packets by writing to udp_data
  'udp_data'  : 'wf', # Raw udp Data input
  }

  valDict = {
  'clear'     : 0, # Clears EBM buffers
  'flush'     : 0, # Send stored data as an EB packet
  'status'    : 0, # Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  'src_mac'   : 0xD15EA5EDBABE, # Source MAC address
  'src_ip'    : 0xdeadbeef, # Source IPV4 address
  'src_port'  : 0xebd0, # Source port number
  'dst_mac'   : 0xffffffffffff, # Destination MAC address
  'dst_ip'    : 0xffffffff, # Destination IPV4 address
  'dst_port'  : 0xebd0, # Destination port number
  'mtu'       : 1500, # Maximum packet size
  'adr_hi'    : 0, # High Address bits inserted into WB operations
  'eb_opt'    : 0, # Default Record Header Options for current transaction
  'sema'      : 0, # Semaphore register in case multiple users want access
  'udp_raw'   : 0, # If this Flag is set, you can create raw udp packets by writing to udp_data
  'udp_data'  : 0, # Raw udp Data input
  }
