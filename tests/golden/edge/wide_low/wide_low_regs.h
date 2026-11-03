/** @file        wide_low_regs.h
  * DesignUnit   wide_low
  * @author      T <t@x>
  * @date        14/11/2023
  * @version     0.0.1
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <wide_low_auto>
  */

#ifndef _WIDE_LOW_H_
#define _WIDE_LOW_H_

  #define WIDE_LOW_SDB_VENDOR_ID 0x00000651
  #define WIDE_LOW_SDB_DEVICE_ID 0x12345678

  #define WIDE_LOW_FIRST_RW   0x0   //rw,  8 b, before
  #define WIDE_LOW_WIDE_RW_0  0x4   //rw, 32 b, 48 bit, not a multiple of the bus width
  #define WIDE_LOW_WIDE_RW_1  0x8   //rw, 16 b, 48 bit, not a multiple of the bus width
  #define WIDE_LOW_STAT_GET_0 0xc   //ro, 32 b, 64 bit, driven
  #define WIDE_LOW_STAT_GET_1 0x10  //ro, 32 b, 64 bit, driven

#endif
