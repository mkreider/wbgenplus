class ebm (object):
  ifname = 'slave'

  adrDict = {
  'clear_owr'     : 0x00, # wo,             1 b, Clears EBM buffers
  'flush_owr'     : 0x04, # wo,             1 b, Send stored data as an EB packet
  'status_get'    : 0x08, # ro,            32 b, Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  'src_mac_rw_0'  : 0x0c, # rw,            32 b, Source MAC address
  'src_mac_rw_1'  : 0x10, # rw,            16 b, Source MAC address
  'src_ip_rw'     : 0x14, # rw,            32 b, Source IPV4 address
  'src_port_rw'   : 0x18, # rw,            16 b, Source port number
  'dst_mac_rw_0'  : 0x1c, # rw,            32 b, Destination MAC address
  'dst_mac_rw_1'  : 0x20, # rw,            16 b, Destination MAC address
  'dst_ip_rw'     : 0x24, # rw,            32 b, Destination IPV4 address
  'dst_port_rw'   : 0x28, # rw,            16 b, Destination port number
  'mtu_rw'        : 0x2c, # rw,            16 b, Maximum packet size
  'adr_hi_rw'     : 0x30, # rw, g_adr_bits_hi b, High Address bits inserted into WB operations
  'eb_opt_rw'     : 0x34, # rw,            32 b, Default Record Header Options for current transaction
  'sema_rw'       : 0x38, # rw,            32 b, Semaphore register in case multiple users want access
  'udp_raw_rw'    : 0x3c, # rw,             1 b, If this Flag is set, you can create raw udp packets by writing to udp_data
  'udp_data_owr'  : 0x40, # wo,            16 b, Raw udp Data input
  }

  adrDict_reverse = {
  0x00  : 'clear_owr', # wo,             1 b, Clears EBM buffers
  0x04  : 'flush_owr', # wo,             1 b, Send stored data as an EB packet
  0x08  : 'status_get', # ro,            32 b, Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  0x0c  : 'src_mac_rw_0', # rw,            32 b, Source MAC address
  0x10  : 'src_mac_rw_1', # rw,            16 b, Source MAC address
  0x14  : 'src_ip_rw', # rw,            32 b, Source IPV4 address
  0x18  : 'src_port_rw', # rw,            16 b, Source port number
  0x1c  : 'dst_mac_rw_0', # rw,            32 b, Destination MAC address
  0x20  : 'dst_mac_rw_1', # rw,            16 b, Destination MAC address
  0x24  : 'dst_ip_rw', # rw,            32 b, Destination IPV4 address
  0x28  : 'dst_port_rw', # rw,            16 b, Destination port number
  0x2c  : 'mtu_rw', # rw,            16 b, Maximum packet size
  0x30  : 'adr_hi_rw', # rw, g_adr_bits_hi b, High Address bits inserted into WB operations
  0x34  : 'eb_opt_rw', # rw,            32 b, Default Record Header Options for current transaction
  0x38  : 'sema_rw', # rw,            32 b, Semaphore register in case multiple users want access
  0x3c  : 'udp_raw_rw', # rw,             1 b, If this Flag is set, you can create raw udp packets by writing to udp_data
  0x40  : 'udp_data_owr', # wo,            16 b, Raw udp Data input
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
