/** @file        simple_demo_regs.h
  * DesignUnit   simple_demo
  * @author      M. Kreider <>
  * @date        14/11/2023
  * @version     0.0.1
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <simple_demo_auto>
  */

#ifndef _SIMPLE_DEMO_H_
#define _SIMPLE_DEMO_H_

  #define SIMPLE_DEMO_SDB_VENDOR_ID 0x00000651
  #define SIMPLE_DEMO_SDB_DEVICE_ID 0x78412212

  #define SIMPLE_DEMO_STATUS_GET 0x00  //ro, g_statusbits b, Shows if the devices are rdy/busy
  #define SIMPLE_DEMO_MODE_GET   0x04  //ro,            8 b, Mode
  #define SIMPLE_DEMO_MODE_CLR   0x08  //wo,            8 b, Mode
  #define SIMPLE_DEMO_MODE_SET   0x0c  //wo,            8 b, Mode
  #define SIMPLE_DEMO_SCPAD_RW_1 0x10  //rw,           32 b, Scratchpad. Can be modified from Bus or outer entity
  #define SIMPLE_DEMO_SCPAD_RW_0 0x14  //rw,           32 b, Scratchpad. Can be modified from Bus or outer entity
  #define SIMPLE_DEMO_COUNT_GET  0x18  //ro,           16 b, Shows Data Input Counter

#endif
