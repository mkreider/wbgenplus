/** @file        eca_tap_regs.h
  * DesignUnit   eca_tap
  * @author      M. Kreider <m.kreider@gsi.de>
  * @date        14/11/2023
  * @version     0.0.1
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <eca_tap_auto>
  */

#ifndef _ECA_TAP_H_
#define _ECA_TAP_H_

  #define ECA_TAP_SDB_VENDOR_ID 0x00000651
  #define ECA_TAP_SDB_DEVICE_ID 0x0eca07a2

  #define ECA_TAP_RESET_OWR      0x0000000000000000000000000 //wo,  1 b, Resets ECA-Tap
  #define ECA_TAP_CLEAR_OWR      0x0000000000000000000000004 //wo,  4 b, b3: clear late count, b2: clear count/accu, b1: clear max, b0: clear min
  #define ECA_TAP_CAPTURE_RW     0x0000000000000000000000008 //rw,  1 b, Enable/Disable Capture
  #define ECA_TAP_CNT_MSG_GET_0  0x000000000000000000000000c //ro, 32 b, Message Count
  #define ECA_TAP_CNT_MSG_GET_1  0x0000000000000000000000010 //ro, 32 b, Message Count
  #define ECA_TAP_DIFF_ACC_GET_0 0x0000000000000000000000014 //ro, 32 b, Accumulated differences (dl - ts)
  #define ECA_TAP_DIFF_ACC_GET_1 0x0000000000000000000000018 //ro, 32 b, Accumulated differences (dl - ts)
  #define ECA_TAP_DIFF_MIN_GET_0 0x000000000000000000000001c //ro, 32 b, Minimum difference
  #define ECA_TAP_DIFF_MIN_GET_1 0x0000000000000000000000020 //ro, 32 b, Minimum difference
  #define ECA_TAP_DIFF_MAX_GET_0 0x0000000000000000000000024 //ro, 32 b, Maximum difference
  #define ECA_TAP_DIFF_MAX_GET_1 0x0000000000000000000000028 //ro, 32 b, Maximum difference
  #define ECA_TAP_CNT_LATE_GET   0x000000000000000000000002c //ro, 32 b, Late Message Count
  #define ECA_TAP_OFFSET_LATE_RW 0x0000000000000000000000030 //rw, 32 b, Offset on difference. Controls condition for Late Message Counter increment

#endif
