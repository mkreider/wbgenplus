class reset_comment (object):
  ifname = 'ctrl'

  adrDict = {
  'all_ones_rw' : 0x00, # rw,       8 b, reset to ones, 100% sure
  'all_zero_rw' : 0x04, # rw,       8 b, reset to zeroes
  'hex_rst_rw'  : 0x08, # rw,      16 b, hex reset
  'pct_get'     : 0x0c, # ro,       4 b, load 50%, %s %d %% stay literal
  'pct_w_clr'   : 0x10, # wo, g_lanes b, atomic 10% pulse
  'pct_w_set'   : 0x14, # wo, g_lanes b, atomic 10% pulse
  }

  adrDict_reverse = {
  0x00  : 'all_ones_rw', # rw,       8 b, reset to ones, 100% sure
  0x04  : 'all_zero_rw', # rw,       8 b, reset to zeroes
  0x08  : 'hex_rst_rw', # rw,      16 b, hex reset
  0x0c  : 'pct_get', # ro,       4 b, load 50%, %s %d %% stay literal
  0x10  : 'pct_w_clr', # wo, g_lanes b, atomic 10% pulse
  0x14  : 'pct_w_set', # wo, g_lanes b, atomic 10% pulse
  }

  flagDict = {
  'all_ones'  : 'rw', # reset to ones, 100% sure
  'all_zero'  : 'rw', # reset to zeroes
  'hex_rst'   : 'rw', # hex reset
  'pct'       : 'rdf', # load 50%, %s %d %% stay literal
  'pct_w'     : 'wap', # atomic 10% pulse
  }

  valDict = {
  'all_ones'  : ones, # reset to ones, 100% sure
  'all_zero'  : 0, # reset to zeroes
  'hex_rst'   : 0xbeef, # hex reset
  'pct'       : 0, # load 50%, %s %d %% stay literal
  'pct_w'     : 0, # atomic 10% pulse
  }
