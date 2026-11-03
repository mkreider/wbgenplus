/** @file        prio_regs.h
  * DesignUnit   prio
  * @author      M. Kreider <m.kreider@gsi.de>
  * @date        14/11/2023
  * @version     0.0.1
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <prio_auto>
  */

#ifndef _PRIO_H_
#define _PRIO_H_

  #define PRIO_SDB_VENDOR_ID 0x00000651
  #define PRIO_SDB_DEVICE_ID 0x10040200

  #define PRIO_RESET_OWR          0x00000 //wo,          1 b, Resets the Priority Queue
  #define PRIO_MODE_GET           0x00004 //ro,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  #define PRIO_MODE_CLR           0x00008 //wo,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  #define PRIO_MODE_SET           0x0000c //wo,          3 b, b2: Time limit, b1: Msg limit, b0 enable
  #define PRIO_CLEAR_OWR          0x00010 //wo,          1 b, Clears counters and status
  #define PRIO_ST_FULL_GET        0x00014 //ro, g_channels b, Channel Full flag (n..0) 
  #define PRIO_ST_LATE_GET        0x00018 //ro,          1 b, Late message detected
  #define PRIO_EBM_ADR_RW         0x0001c //rw,         32 b, Etherbone Master address
  #define PRIO_ECA_ADR_RW         0x00020 //rw,         32 b, Event Condition Action Unit address
  #define PRIO_TX_MAX_MSGS_RW     0x00024 //rw,          8 b, Max msgs per packet
  #define PRIO_TX_MAX_WAIT_RW     0x00028 //rw,         32 b, Max wait time for non empty packet
  #define PRIO_TX_RATE_LIMIT_RW   0x0002c //rw,         32 b, Max msgs per milliseconds
  #define PRIO_OFFS_LATE_RW_0     0x00030 //rw,         32 b, Time offset before message is late
  #define PRIO_OFFS_LATE_RW_1     0x00034 //rw,         32 b, Time offset before message is late
  #define PRIO_CNT_LATE_GET       0x00038 //ro,         32 b, Sum of all late messages
  #define PRIO_TS_LATE_GET_0      0x0003c //ro,         32 b, First late Timestamp
  #define PRIO_TS_LATE_GET_1      0x00040 //ro,         32 b, First late Timestamp
  #define PRIO_CNT_OUT_ALL_GET_0  0x00044 //ro,         32 b, Sum of all outgoing messages
  #define PRIO_CNT_OUT_ALL_GET_1  0x00048 //ro,         32 b, Sum of all outgoing messages

#endif
