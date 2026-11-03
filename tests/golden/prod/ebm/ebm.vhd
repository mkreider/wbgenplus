--! @file        ebm.xml
--  DesignUnit   ebm
--! @author      M. Kreider <>
--! @date        14/11/2023
--! @version     0.2.0
--! @copyright   2023 GSI Helmholtz Centre for Heavy Ion Research GmbH
--!

--TODO: This is a stub, finish/update it yourself
--! @brief *** ADD BRIEF DESCRIPTION HERE ***
--!
--------------------------------------------------------------------------------
--! This library is free software; you can redistribute it and/or
--! modify it under the terms of the GNU Lesser General Public
--! License as published by the Free Software Foundation; either
--! version 3 of the License, or (at your option) any later version.
--!
--! This library is distributed in the hope that it will be useful,
--! but WITHOUT ANY WARRANTY; without even the implied warranty of
--! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
--! Lesser General Public License for more details.
--!
--! You should have received a copy of the GNU Lesser General Public
--! License along with this library. If not, see <http://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.wishbone_pkg.all;
use work.wbgenplus_pkg.all;
use work.genram_pkg.all;
use work.ebm_auto_pkg.all;

entity ebm is
generic(
  g_adr_bits_hi : natural := 10 --Number of high address bits
);
Port(
  clk_sys_i     : std_logic;                                      -- Clock input for sys domain
  rst_sys_n_i   : std_logic;                                      -- Reset input (active low) for sys domain
  error_i       : in  std_logic_vector(1-1 downto 0);             -- Error control
  stall_i       : in  std_logic_vector(1-1 downto 0);             -- flow control
  status_i      : in  std_logic_vector(32-1 downto 0);            -- Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  status_V_i    : in  std_logic_vector(1-1 downto 0);             -- Valid flag - status
  adr_hi_o      : out std_logic_vector(g_adr_bits_hi-1 downto 0); -- High Address bits inserted into WB operations
  clear_o       : out std_logic_vector(1-1 downto 0);             -- Clears EBM buffers
  dst_ip_o      : out std_logic_vector(32-1 downto 0);            -- Destination IPV4 address
  dst_mac_o     : out std_logic_vector(48-1 downto 0);            -- Destination MAC address
  dst_port_o    : out std_logic_vector(16-1 downto 0);            -- Destination port number
  eb_opt_o      : out std_logic_vector(32-1 downto 0);            -- Default Record Header Options for current transaction
  flush_o       : out std_logic_vector(1-1 downto 0);             -- Send stored data as an EB packet
  mtu_o         : out std_logic_vector(16-1 downto 0);            -- Maximum packet size
  sema_o        : out std_logic_vector(32-1 downto 0);            -- Semaphore register in case multiple users want access
  src_ip_o      : out std_logic_vector(32-1 downto 0);            -- Source IPV4 address
  src_mac_o     : out std_logic_vector(48-1 downto 0);            -- Source MAC address
  src_port_o    : out std_logic_vector(16-1 downto 0);            -- Source port number
  udp_data_o    : out std_logic_vector(16-1 downto 0);            -- Raw udp Data input
  udp_data_WR_o : out std_logic_vector(1-1 downto 0);             -- Write enable flag - udp_data
  udp_raw_o     : out std_logic_vector(1-1 downto 0);             -- If this Flag is set, you can create raw udp packets by writing to udp_data
  
  slave_i       : in  t_wishbone_slave_in;
  slave_o       : out t_wishbone_slave_out

  
);
end ebm;

architecture rtl of ebm is

  signal s_slave_error_i        : std_logic_vector(1-1 downto 0)              := (others => '0'); -- Error control
  signal s_slave_stall_i        : std_logic_vector(1-1 downto 0)              := (others => '0'); -- flow control
  signal s_slave_clear_o        : std_logic_vector(1-1 downto 0)              := (others => '0'); -- Clears EBM buffers
  signal s_slave_flush_o        : std_logic_vector(1-1 downto 0)              := (others => '0'); -- Send stored data as an EB packet
  signal s_slave_status_V_i     : std_logic_vector(1-1 downto 0)              := (others => '0'); -- Valid flag - status
  signal s_slave_status_i       : std_logic_vector(32-1 downto 0)             := (others => '0'); -- Status. 31..16: Packet counter. b2: Error b1: busy b0: configured
  signal s_slave_src_mac_o      : std_logic_vector(48-1 downto 0)             := (others => '0'); -- Source MAC address
  signal s_slave_src_ip_o       : std_logic_vector(32-1 downto 0)             := (others => '0'); -- Source IPV4 address
  signal s_slave_src_port_o     : std_logic_vector(16-1 downto 0)             := (others => '0'); -- Source port number
  signal s_slave_dst_mac_o      : std_logic_vector(48-1 downto 0)             := (others => '0'); -- Destination MAC address
  signal s_slave_dst_ip_o       : std_logic_vector(32-1 downto 0)             := (others => '0'); -- Destination IPV4 address
  signal s_slave_dst_port_o     : std_logic_vector(16-1 downto 0)             := (others => '0'); -- Destination port number
  signal s_slave_mtu_o          : std_logic_vector(16-1 downto 0)             := (others => '0'); -- Maximum packet size
  signal s_slave_adr_hi_o       : std_logic_vector(g_adr_bits_hi-1 downto 0)  := (others => '0'); -- High Address bits inserted into WB operations
  signal s_slave_eb_opt_o       : std_logic_vector(32-1 downto 0)             := (others => '0'); -- Default Record Header Options for current transaction
  signal s_slave_sema_o         : std_logic_vector(32-1 downto 0)             := (others => '0'); -- Semaphore register in case multiple users want access
  signal s_slave_udp_raw_o      : std_logic_vector(1-1 downto 0)              := (others => '0'); -- If this Flag is set, you can create raw udp packets by writing to udp_data
  signal s_slave_udp_data_WR_o  : std_logic_vector(1-1 downto 0)              := (others => '0'); -- Write enable flag - udp_data
  signal s_slave_udp_data_o     : std_logic_vector(16-1 downto 0)             := (others => '0'); -- Raw udp Data input
  


begin

  INST_ebm_auto : ebm_auto
  port map (
    clk_sys_i     => clk_sys_i,
    rst_sys_n_i   => rst_sys_n_i,
    error_i       => s_slave_error_i,
    stall_i       => s_slave_stall_i,
    clear_o       => s_slave_clear_o,
    flush_o       => s_slave_flush_o,
    status_V_i    => s_slave_status_V_i,
    status_i      => s_slave_status_i,
    src_mac_o     => s_slave_src_mac_o,
    src_ip_o      => s_slave_src_ip_o,
    src_port_o    => s_slave_src_port_o,
    dst_mac_o     => s_slave_dst_mac_o,
    dst_ip_o      => s_slave_dst_ip_o,
    dst_port_o    => s_slave_dst_port_o,
    mtu_o         => s_slave_mtu_o,
    adr_hi_o      => s_slave_adr_hi_o,
    eb_opt_o      => s_slave_eb_opt_o,
    sema_o        => s_slave_sema_o,
    udp_raw_o     => s_slave_udp_raw_o,
    udp_data_WR_o => s_slave_udp_data_WR_o,
    udp_data_o    => s_slave_udp_data_o,
    slave_i       => slave_i,
    slave_o       => slave_o  );
end rtl;
