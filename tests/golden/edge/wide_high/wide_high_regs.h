/** @file        wide_high_regs.h
  * DesignUnit   wide_high
  * @author      T <t@x>
  * @date        14/11/2023
  * @version     0.0.1
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <wide_high_auto>
  */

#ifndef _WIDE_HIGH_H_
#define _WIDE_HIGH_H_

  #define WIDE_HIGH_SDB_VENDOR_ID 0x00000651
  #define WIDE_HIGH_SDB_DEVICE_ID 0x12345678

  #define WIDE_HIGH_FIRST_RW   0x0   //rw,  8 b, before
  #define WIDE_HIGH_WIDE_RW_1  0x4   //rw, 16 b, 48 bit, not a multiple of the bus width
  #define WIDE_HIGH_WIDE_RW_0  0x8   //rw, 32 b, 48 bit, not a multiple of the bus width
  #define WIDE_HIGH_STAT_GET_1 0xc   //ro, 32 b, 64 bit, driven
  #define WIDE_HIGH_STAT_GET_0 0x10  //ro, 32 b, 64 bit, driven

#endif
