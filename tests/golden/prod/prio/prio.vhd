--! @file        prio.xml
--  DesignUnit   prio
--! @author      M. Kreider <m.kreider@gsi.de>
--! @date        14/11/2023
--! @version     0.0.1
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
use work.prio_auto_pkg.all;

entity prio is
generic(
  g_channels  : natural := 16 --Input channels
);
Port(
  clk_sys_i       : std_logic;                                    -- Clock input for sys domain
  rst_sys_n_i     : std_logic;                                    -- Reset input (active low) for sys domain
  cnt_late_i      : in  std_logic_vector(32-1 downto 0);          -- Sum of all late messages
  cnt_late_V_i    : in  std_logic_vector(1-1 downto 0);           -- Valid flag - cnt_late
  cnt_out_all_i   : in  std_logic_vector(64-1 downto 0);          -- Sum of all outgoing messages
  cnt_out_all_V_i : in  std_logic_vector(1-1 downto 0);           -- Valid flag - cnt_out_all
  error_i         : in  std_logic_vector(1-1 downto 0);           -- Error control
  st_full_i       : in  std_logic_vector(g_channels-1 downto 0);  -- Channel Full flag (n..0) 
  st_full_V_i     : in  std_logic_vector(1-1 downto 0);           -- Valid flag - st_full
  st_late_i       : in  std_logic_vector(1-1 downto 0);           -- Late message detected
  st_late_V_i     : in  std_logic_vector(1-1 downto 0);           -- Valid flag - st_late
  stall_i         : in  std_logic_vector(1-1 downto 0);           -- flow control
  ts_late_i       : in  std_logic_vector(64-1 downto 0);          -- First late Timestamp
  ts_late_V_i     : in  std_logic_vector(1-1 downto 0);           -- Valid flag - ts_late
  clear_o         : out std_logic_vector(1-1 downto 0);           -- Clears counters and status
  ebm_adr_o       : out std_logic_vector(32-1 downto 0);          -- Etherbone Master address
  eca_adr_o       : out std_logic_vector(32-1 downto 0);          -- Event Condition Action Unit address
  mode_o          : out std_logic_vector(3-1 downto 0);           -- b2: Time limit, b1: Msg limit, b0 enable
  offs_late_o     : out std_logic_vector(64-1 downto 0);          -- Time offset before message is late
  reset_o         : out std_logic_vector(1-1 downto 0);           -- Resets the Priority Queue
  tx_max_msgs_o   : out std_logic_vector(8-1 downto 0);           -- Max msgs per packet
  tx_max_wait_o   : out std_logic_vector(32-1 downto 0);          -- Max wait time for non empty packet
  tx_rate_limit_o : out std_logic_vector(32-1 downto 0);          -- Max msgs per milliseconds
  
  ctrl_i          : in  t_wishbone_slave_in;
  ctrl_o          : out t_wishbone_slave_out

  
);
end prio;

architecture rtl of prio is

  signal s_ctrl_error_i         : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Error control
  signal s_ctrl_stall_i         : std_logic_vector(1-1 downto 0)          := (others => '0'); -- flow control
  signal s_ctrl_reset_o         : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Resets the Priority Queue
  signal s_ctrl_mode_o          : std_logic_vector(3-1 downto 0)          := (others => '0'); -- b2: Time limit, b1: Msg limit, b0 enable
  signal s_ctrl_clear_o         : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Clears counters and status
  signal s_ctrl_st_full_V_i     : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Valid flag - st_full
  signal s_ctrl_st_full_i       : std_logic_vector(g_channels-1 downto 0) := (others => '0'); -- Channel Full flag (n..0) 
  signal s_ctrl_st_late_V_i     : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Valid flag - st_late
  signal s_ctrl_st_late_i       : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Late message detected
  signal s_ctrl_ebm_adr_o       : std_logic_vector(32-1 downto 0)         := (others => '0'); -- Etherbone Master address
  signal s_ctrl_eca_adr_o       : std_logic_vector(32-1 downto 0)         := (others => '0'); -- Event Condition Action Unit address
  signal s_ctrl_tx_max_msgs_o   : std_logic_vector(8-1 downto 0)          := (others => '0'); -- Max msgs per packet
  signal s_ctrl_tx_max_wait_o   : std_logic_vector(32-1 downto 0)         := (others => '0'); -- Max wait time for non empty packet
  signal s_ctrl_tx_rate_limit_o : std_logic_vector(32-1 downto 0)         := (others => '0'); -- Max msgs per milliseconds
  signal s_ctrl_offs_late_o     : std_logic_vector(64-1 downto 0)         := (others => '0'); -- Time offset before message is late
  signal s_ctrl_cnt_late_V_i    : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Valid flag - cnt_late
  signal s_ctrl_cnt_late_i      : std_logic_vector(32-1 downto 0)         := (others => '0'); -- Sum of all late messages
  signal s_ctrl_ts_late_V_i     : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Valid flag - ts_late
  signal s_ctrl_ts_late_i       : std_logic_vector(64-1 downto 0)         := (others => '0'); -- First late Timestamp
  signal s_ctrl_cnt_out_all_V_i : std_logic_vector(1-1 downto 0)          := (others => '0'); -- Valid flag - cnt_out_all
  signal s_ctrl_cnt_out_all_i   : std_logic_vector(64-1 downto 0)         := (others => '0'); -- Sum of all outgoing messages
  


begin

  INST_prio_auto : prio_auto
  port map (
    clk_sys_i       => clk_sys_i,
    rst_sys_n_i     => rst_sys_n_i,
    error_i         => s_ctrl_error_i,
    stall_i         => s_ctrl_stall_i,
    reset_o         => s_ctrl_reset_o,
    mode_o          => s_ctrl_mode_o,
    clear_o         => s_ctrl_clear_o,
    st_full_V_i     => s_ctrl_st_full_V_i,
    st_full_i       => s_ctrl_st_full_i,
    st_late_V_i     => s_ctrl_st_late_V_i,
    st_late_i       => s_ctrl_st_late_i,
    ebm_adr_o       => s_ctrl_ebm_adr_o,
    eca_adr_o       => s_ctrl_eca_adr_o,
    tx_max_msgs_o   => s_ctrl_tx_max_msgs_o,
    tx_max_wait_o   => s_ctrl_tx_max_wait_o,
    tx_rate_limit_o => s_ctrl_tx_rate_limit_o,
    offs_late_o     => s_ctrl_offs_late_o,
    cnt_late_V_i    => s_ctrl_cnt_late_V_i,
    cnt_late_i      => s_ctrl_cnt_late_i,
    ts_late_V_i     => s_ctrl_ts_late_V_i,
    ts_late_i       => s_ctrl_ts_late_i,
    cnt_out_all_V_i => s_ctrl_cnt_out_all_V_i,
    cnt_out_all_i   => s_ctrl_cnt_out_all_i,
    ctrl_i          => ctrl_i,
    ctrl_o          => ctrl_o  );
end rtl;
