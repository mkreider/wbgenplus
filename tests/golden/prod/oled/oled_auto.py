class oled (object):
  ifname = 'slave'

  adrDict = {
  'reset_owr'   : 0x000000000000000000000000000000000000000000000000000000000000000000000000000, # wo,  1 b, Resets the OLED display
  'col_offs_rw' : 0x000000000000000000000000000000000000000000000000000000000000000000000000004, # rw,  8 b, first visible pixel column. 0x23 for old, 0x30 for new controllers. default is 0x30
  'uart_owr'    : 0x000000000000000000000000000000000000000000000000000000000000000000000000008, # wo,  8 b, UART input FIFO. Ascii b7..0
  'char_owr'    : 0x00000000000000000000000000000000000000000000000000000000000000000000000000c, # wo, 20 b, Char input FIFO. Row b14..12, Col b11..8, Ascii b7..0
  'raw_owr'     : 0x000000000000000000000000000000000000000000000000000000000000000000000000010, # wo, 20 b, Raw  input FIFO. Disp RAM Adr b18..8, Pixel (Col) b7..0
  }

  adrDict_reverse = {
  0x000000000000000000000000000000000000000000000000000000000000000000000000000 : 'reset_owr', # wo,  1 b, Resets the OLED display
  0x000000000000000000000000000000000000000000000000000000000000000000000000004 : 'col_offs_rw', # rw,  8 b, first visible pixel column. 0x23 for old, 0x30 for new controllers. default is 0x30
  0x000000000000000000000000000000000000000000000000000000000000000000000000008 : 'uart_owr', # wo,  8 b, UART input FIFO. Ascii b7..0
  0x00000000000000000000000000000000000000000000000000000000000000000000000000c : 'char_owr', # wo, 20 b, Char input FIFO. Row b14..12, Col b11..8, Ascii b7..0
  0x000000000000000000000000000000000000000000000000000000000000000000000000010 : 'raw_owr', # wo, 20 b, Raw  input FIFO. Disp RAM Adr b18..8, Pixel (Col) b7..0
  }

  flagDict = {
  'reset'     : 'wp', # Resets the OLED display
  'col_offs'  : 'rw', # first visible pixel column. 0x23 for old, 0x30 for new controllers. default is 0x30
  'uart'      : 'wf', # UART input FIFO. Ascii b7..0
  'char'      : 'wf', # Char input FIFO. Row b14..12, Col b11..8, Ascii b7..0
  'raw'       : 'wf', # Raw  input FIFO. Disp RAM Adr b18..8, Pixel (Col) b7..0
  }

  valDict = {
  'reset'     : 0, # Resets the OLED display
  'col_offs'  : 0x30, # first visible pixel column. 0x23 for old, 0x30 for new controllers. default is 0x30
  'uart'      : 0, # UART input FIFO. Ascii b7..0
  'char'      : 0, # Char input FIFO. Row b14..12, Col b11..8, Ascii b7..0
  'raw'       : 0, # Raw  input FIFO. Disp RAM Adr b18..8, Pixel (Col) b7..0
  }
