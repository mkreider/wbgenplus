/** @file        reset_comment_regs.h
  * DesignUnit   reset_comment
  * @author      T <t@x>
  * @date        14/11/2023
  * @version     0.0.1
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <reset_comment_auto>
  */

#ifndef _RESET_COMMENT_H_
#define _RESET_COMMENT_H_

  #define RESET_COMMENT_SDB_VENDOR_ID 0x00000651
  #define RESET_COMMENT_SDB_DEVICE_ID 0x12345679

  #define RESET_COMMENT_ALL_ONES_RW  0x00  //rw,       8 b, reset to ones, 100% sure
  #define RESET_COMMENT_ALL_ZERO_RW  0x04  //rw,       8 b, reset to zeroes
  #define RESET_COMMENT_HEX_RST_RW   0x08  //rw,      16 b, hex reset
  #define RESET_COMMENT_PCT_GET      0x0c  //ro,       4 b, load 50%, %s %d %% stay literal
  #define RESET_COMMENT_PCT_W_CLR    0x10  //wo, g_lanes b, atomic 10% pulse
  #define RESET_COMMENT_PCT_W_SET    0x14  //wo, g_lanes b, atomic 10% pulse

#endif
