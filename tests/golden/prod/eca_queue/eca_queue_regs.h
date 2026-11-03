/** @file        eca_queue_regs.h
  * DesignUnit   eca_queue
  * @author      Wesley W. Terpstra <w.terpstra@gsi.de>
  * @date        14/11/2023
  * @version     2.0
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <eca_queue_auto>
  */

#ifndef _ECA_QUEUE_H_
#define _ECA_QUEUE_H_

  #define ECA_QUEUE_SDB_VENDOR_ID 0x00000651
  #define ECA_QUEUE_SDB_DEVICE_ID 0xd5a3faea

  #define ECA_QUEUE_QUEUE_ID_GET     0x0000000000000000000000000 //ro,  8 b, The index of a_channel_o from the ECA to which this queue is connected (set channel_select=queue_id+1)
  #define ECA_QUEUE_POP_OWR          0x0000000000000000000000004 //wo,  1 b, Pop action from the channel's queue
  #define ECA_QUEUE_FLAGS_GET        0x0000000000000000000000008 //ro,  5 b, Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  #define ECA_QUEUE_NUM_GET          0x000000000000000000000000c //ro,  8 b, Subchannel target
  #define ECA_QUEUE_EVENT_ID_HI_GET  0x0000000000000000000000010 //ro, 32 b, Event ID (high word)
  #define ECA_QUEUE_EVENT_ID_LO_GET  0x0000000000000000000000014 //ro, 32 b, Event ID (low word)
  #define ECA_QUEUE_PARAM_HI_GET     0x0000000000000000000000018 //ro, 32 b, Parameter (high word)
  #define ECA_QUEUE_PARAM_LO_GET     0x000000000000000000000001c //ro, 32 b, Parameter (low word)
  #define ECA_QUEUE_TAG_GET          0x0000000000000000000000020 //ro, 32 b, Tag from the condition
  #define ECA_QUEUE_TEF_GET          0x0000000000000000000000024 //ro, 32 b, Timing extension field
  #define ECA_QUEUE_DEADLINE_HI_GET  0x0000000000000000000000028 //ro, 32 b, Deadline (high word)
  #define ECA_QUEUE_DEADLINE_LO_GET  0x000000000000000000000002c //ro, 32 b, Deadline (low word)
  #define ECA_QUEUE_EXECUTED_HI_GET  0x0000000000000000000000030 //ro, 32 b, Actual execution time (high word)
  #define ECA_QUEUE_EXECUTED_LO_GET  0x0000000000000000000000034 //ro, 32 b, Actual execution time (low word)

#endif
