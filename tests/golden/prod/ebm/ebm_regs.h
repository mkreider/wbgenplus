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

      #define EBM_CLEAR_OWR    0x00  //wo,             1 b, Clears EBM buffers
  #define EBM_FLUSH_OWR    0x04  //wo,             1 b, Send stored data as an EB packet
  #define EBM_STATUS_GET   0x08  //ro,            32 b, Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  #define EBM_SRC_MAC_RW_0 0x0c  //rw,            32 b, Source MAC address
  #define EBM_SRC_MAC_RW_1 0x10  //rw,            16 b, Source MAC address
  #define EBM_SRC_IP_RW    0x14  //rw,            32 b, Source IPV4 address
  #define EBM_SRC_PORT_RW  0x18  //rw,            16 b, Source port number
  #define EBM_DST_MAC_RW_0 0x1c  //rw,            32 b, Destination MAC address
  #define EBM_DST_MAC_RW_1 0x20  //rw,            16 b, Destination MAC address
  #define EBM_DST_IP_RW    0x24  //rw,            32 b, Destination IPV4 address
  #define EBM_DST_PORT_RW  0x28  //rw,            16 b, Destination port number
  #define EBM_MTU_RW       0x2c  //rw,            16 b, Maximum packet size
  #define EBM_ADR_HI_RW    0x30  //rw, g_adr_bits_hi b, High Address bits inserted into WB operations
  #define EBM_EB_OPT_RW    0x34  //rw,            32 b, Default Record Header Options for current transaction
  #define EBM_SEMA_RW      0x38  //rw,            32 b, Semaphore register in case multiple users want access
  #define EBM_UDP_RAW_RW   0x3c  //rw,             1 b, If this Flag is set, you can create raw udp packets by writing to udp_data
  #define EBM_UDP_DATA_OWR 0x40  //wo,            16 b, Raw udp Data input

#endif
