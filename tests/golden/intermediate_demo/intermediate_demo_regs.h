/** @file        intermediate_demo_regs.h
  * DesignUnit   intermediate_demo
  * @author      M. Kreider <>
  * @date        14/11/2023
  * @version     0.0.1
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <intermediate_demo_auto>
  */

#ifndef _INTERMEDIATE_DEMO_H_
#define _INTERMEDIATE_DEMO_H_

  #define INTERMEDIATE_DEMO_SDB_VENDOR_ID 0x00000651
  #define INTERMEDIATE_DEMO_SDB_DEVICE_ID 0x78412212

  #define INTERMEDIATE_DEMO_STATUS_GET     0x000 //ro, g_channels b, 'timestamps pending' bit per channel
  #define INTERMEDIATE_DEMO_CH_QTY_GET     0x004 //ro,          5 b, Individually controllable flag bits
  #define INTERMEDIATE_DEMO_CH_SEL_RW      0x020 //rw,          8 b, Channel select register
  #define INTERMEDIATE_DEMO_CLEAR_FIFO_OWR 0x100 //wo,          1 b, Clears Fifo
  #define INTERMEDIATE_DEMO_TS_OUT_GET_0   0x104 //ro,         32 b, Timestamp fifos in. Use RD flag to pop
  #define INTERMEDIATE_DEMO_TS_OUT_GET_1   0x108 //ro,         32 b, Timestamp fifos in. Use RD flag to pop
  #define INTERMEDIATE_DEMO_TS_CNT_GET     0x10c //ro,         16 b, Shows channel timestamp count
  #define INTERMEDIATE_DEMO_TS_FLAGS_RW    0x110 //rw,    g_flags b, timestamp channel flagbits

#endif
