/** @file        oled_regs.h
  * DesignUnit   oled
  * @author      M. Kreider <m.kreider@gsi.de>
  * @date        14/11/2023
  * @version     0.2.0
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <oled_auto>
  */

#ifndef _OLED_H_
#define _OLED_H_

  #define OLED_SDB_VENDOR_ID 0x00000651
  #define OLED_SDB_DEVICE_ID 0x93a6f3c4

  #define OLED_RESET_OWR    0x000000000000000000000000000000000000000000000000000000000000000000000000000 //wo,  1 b, Resets the OLED display
  #define OLED_COL_OFFS_RW  0x000000000000000000000000000000000000000000000000000000000000000000000000004 //rw,  8 b, first visible pixel column. 0x23 for old, 0x30 for new controllers. default is 0x30
  #define OLED_UART_OWR     0x000000000000000000000000000000000000000000000000000000000000000000000000008 //wo,  8 b, UART input FIFO. Ascii b7..0
  #define OLED_CHAR_OWR     0x00000000000000000000000000000000000000000000000000000000000000000000000000c //wo, 20 b, Char input FIFO. Row b14..12, Col b11..8, Ascii b7..0
  #define OLED_RAW_OWR      0x000000000000000000000000000000000000000000000000000000000000000000000000010 //wo, 20 b, Raw  input FIFO. Disp RAM Adr b18..8, Pixel (Col) b7..0

#endif
