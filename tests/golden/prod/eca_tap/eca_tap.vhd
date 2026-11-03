--! @file        eca_tap.xml
--  DesignUnit   eca_tap
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
use work.eca_tap_auto_pkg.all;

entity eca_tap is
Port(
  clk_sys_i     : std_logic;                            -- Clock input for sys domain
  rst_sys_n_i   : std_logic;                            -- Reset input (active low) for sys domain
  cnt_late_i    : in  std_logic_vector(32-1 downto 0);  -- Late Message Count
  cnt_late_V_i  : in  std_logic_vector(1-1 downto 0);   -- Valid flag - cnt_late
  cnt_msg_i     : in  std_logic_vector(64-1 downto 0);  -- Message Count
  cnt_msg_V_i   : in  std_logic_vector(1-1 downto 0);   -- Valid flag - cnt_msg
  diff_acc_i    : in  std_logic_vector(64-1 downto 0);  -- Accumulated differences (dl - ts)
  diff_acc_V_i  : in  std_logic_vector(1-1 downto 0);   -- Valid flag - diff_acc
  diff_max_i    : in  std_logic_vector(64-1 downto 0);  -- Maximum difference
  diff_max_V_i  : in  std_logic_vector(1-1 downto 0);   -- Valid flag - diff_max
  diff_min_i    : in  std_logic_vector(64-1 downto 0);  -- Minimum difference
  diff_min_V_i  : in  std_logic_vector(1-1 downto 0);   -- Valid flag - diff_min
  error_i       : in  std_logic_vector(1-1 downto 0);   -- Error control
  stall_i       : in  std_logic_vector(1-1 downto 0);   -- flow control
  capture_o     : out std_logic_vector(1-1 downto 0);   -- Enable/Disable Capture
  clear_o       : out std_logic_vector(4-1 downto 0);   -- b3: clear late count, b2: clear count/accu, b1: clear max, b0: clear min
  offset_late_o : out std_logic_vector(32-1 downto 0);  -- Offset on difference. Controls condition for Late Message Counter increment
  reset_o       : out std_logic_vector(1-1 downto 0);   -- Resets ECA-Tap
  
  ctrl_i        : in  t_wishbone_slave_in;
  ctrl_o        : out t_wishbone_slave_out

  
);
end eca_tap;

architecture rtl of eca_tap is

  signal s_ctrl_error_i       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Error control
  signal s_ctrl_stall_i       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- flow control
  signal s_ctrl_reset_o       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Resets ECA-Tap
  signal s_ctrl_clear_o       : std_logic_vector(4-1 downto 0)  := (others => '0'); -- b3: clear late count, b2: clear count/accu, b1: clear max, b0: clear min
  signal s_ctrl_capture_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Enable/Disable Capture
  signal s_ctrl_cnt_msg_V_i   : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - cnt_msg
  signal s_ctrl_cnt_msg_i     : std_logic_vector(64-1 downto 0) := (others => '0'); -- Message Count
  signal s_ctrl_diff_acc_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - diff_acc
  signal s_ctrl_diff_acc_i    : std_logic_vector(64-1 downto 0) := (others => '0'); -- Accumulated differences (dl - ts)
  signal s_ctrl_diff_min_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - diff_min
  signal s_ctrl_diff_min_i    : std_logic_vector(64-1 downto 0) := (others => '0'); -- Minimum difference
  signal s_ctrl_diff_max_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - diff_max
  signal s_ctrl_diff_max_i    : std_logic_vector(64-1 downto 0) := (others => '0'); -- Maximum difference
  signal s_ctrl_cnt_late_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - cnt_late
  signal s_ctrl_cnt_late_i    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Late Message Count
  signal s_ctrl_offset_late_o : std_logic_vector(32-1 downto 0) := (others => '0'); -- Offset on difference. Controls condition for Late Message Counter increment
  


begin

  INST_eca_tap_auto : eca_tap_auto
  port map (
    clk_sys_i     => clk_sys_i,
    rst_sys_n_i   => rst_sys_n_i,
    error_i       => s_ctrl_error_i,
    stall_i       => s_ctrl_stall_i,
    reset_o       => s_ctrl_reset_o,
    clear_o       => s_ctrl_clear_o,
    capture_o     => s_ctrl_capture_o,
    cnt_msg_V_i   => s_ctrl_cnt_msg_V_i,
    cnt_msg_i     => s_ctrl_cnt_msg_i,
    diff_acc_V_i  => s_ctrl_diff_acc_V_i,
    diff_acc_i    => s_ctrl_diff_acc_i,
    diff_min_V_i  => s_ctrl_diff_min_V_i,
    diff_min_i    => s_ctrl_diff_min_i,
    diff_max_V_i  => s_ctrl_diff_max_V_i,
    diff_max_i    => s_ctrl_diff_max_i,
    cnt_late_V_i  => s_ctrl_cnt_late_V_i,
    cnt_late_i    => s_ctrl_cnt_late_i,
    offset_late_o => s_ctrl_offset_late_o,
    ctrl_i        => ctrl_i,
    ctrl_o        => ctrl_o  );
end rtl;
