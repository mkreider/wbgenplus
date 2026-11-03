/** @file        ebm_regs.h
  * DesignUnit   ebm
  * @author      M. Kreider <>
  * @date        14/11/2023
  * @version     0.2.0
  * @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
  *
  * @brief       Register map for Wishbone interface of VHDL entity <ebm_auto>
  */

#ifndef _EBM_H_
#define _EBM_H_

      #define EBM_CLEAR_OWR    0x0000000000000000000000000 //wo,             1 b, Clears EBM buffers
  #define EBM_FLUSH_OWR    0x0000000000000000000000004 //wo,             1 b, Send stored data as an EB packet
  #define EBM_STATUS_GET   0x0000000000000000000000008 //ro,            32 b, Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  #define EBM_SRC_MAC_RW_0 0x000000000000000000000000c //rw,            32 b, Source MAC address
  #define EBM_SRC_MAC_RW_1 0x0000000000000000000000010 //rw,            16 b, Source MAC address
  #define EBM_SRC_IP_RW    0x0000000000000000000000014 //rw,            32 b, Source IPV4 address
  #define EBM_SRC_PORT_RW  0x0000000000000000000000018 //rw,            16 b, Source port number
  #define EBM_DST_MAC_RW_0 0x000000000000000000000001c //rw,            32 b, Destination MAC address
  #define EBM_DST_MAC_RW_1 0x0000000000000000000000020 //rw,            16 b, Destination MAC address
  #define EBM_DST_IP_RW    0x0000000000000000000000024 //rw,            32 b, Destination IPV4 address
  #define EBM_DST_PORT_RW  0x0000000000000000000000028 //rw,            16 b, Destination port number
  #define EBM_MTU_RW       0x000000000000000000000002c //rw,            16 b, Maximum packet size
  #define EBM_ADR_HI_RW    0x0000000000000000000000030 //rw, g_adr_bits_hi b, High Address bits inserted into WB operations
  #define EBM_EB_OPT_RW    0x0000000000000000000000034 //rw,            32 b, Default Record Header Options for current transaction
  #define EBM_SEMA_RW      0x0000000000000000000000038 //rw,            32 b, Semaphore register in case multiple users want access
  #define EBM_UDP_RAW_RW   0x000000000000000000000003c //rw,             1 b, If this Flag is set, you can create raw udp packets by writing to udp_data
  #define EBM_UDP_DATA_OWR 0x0000000000000000000000040 //wo,            16 b, Raw udp Data input

#endif
