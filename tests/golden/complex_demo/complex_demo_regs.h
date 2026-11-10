/** @file        complex_demo_regs.h
  * DesignUnit   complex_demo
  * @author      M. Kreider <>
  * @date        14/11/2023
  * @version     0.0.1
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <complex_demo_auto>
  */

#ifndef _COMPLEX_DEMO_H_
#define _COMPLEX_DEMO_H_

  #define COMPLEX_DEMO_SDB_VENDOR_ID 0x00000651
  #define COMPLEX_DEMO_SDB_DEVICE_ID 0x78412212

  #define COMPLEX_DEMO_STATUS_GET     0x000 //ro, g_channels b, tlu 'timestamps pending' bit per channel
  #define COMPLEX_DEMO_CMD_OWR        0x004 //wo,         16 b, Cmd for tlu controller
  #define COMPLEX_DEMO_CH_QTY_GET     0x008 //ro,          5 b, Individually controllable flag bits
  #define COMPLEX_DEMO_CH_SEL_RW      0x020 //rw,          8 b, Channel select register
  #define COMPLEX_DEMO_CLEAR_FIFO_OWR 0x100 //wo,          1 b, Clears Fifo
  #define COMPLEX_DEMO_TS_OUT_GET_1   0x104 //ro,         32 b, Timestamp fifos in. Use RD flag to pop
  #define COMPLEX_DEMO_TS_OUT_GET_0   0x108 //ro,         32 b, Timestamp fifos in. Use RD flag to pop
  #define COMPLEX_DEMO_CNT_GET        0x10c //ro,         16 b, Shows channel timestamp count
  #define COMPLEX_DEMO_TS_FLAGS_RW    0x110 //rw,    g_flags b, timestamp channel flagbits

#endif
