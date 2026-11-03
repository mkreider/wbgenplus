--! @file        dm_diag.xml
--  DesignUnit   dm_diag
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
use work.dm_diag_auto_pkg.all;

entity dm_diag is
generic(
  g_cores : natural := 16 --CPU cores
);
Port(
  clk_ref_i                     : std_logic;                            -- Clock input for ref domain
  rst_ref_n_i                   : std_logic;                            -- Reset input (active low) for ref domain
  error_i                       : in  std_logic_vector(1-1 downto 0);   -- Error control
  stall_i                       : in  std_logic_vector(1-1 downto 0);   -- flow control
  stall_cnt_i                   : in  std_logic_vector(32-1 downto 0);  -- Stall time within observation interval in cycles
  stall_cnt_V_i                 : in  std_logic_vector(1-1 downto 0);   -- Valid flag - stall_cnt
  stall_max_ts_i                : in  std_logic_vector(64-1 downto 0);  -- Timestamp of last max update
  stall_max_ts_V_i              : in  std_logic_vector(1-1 downto 0);   -- Valid flag - stall_max_ts
  stall_streak_max_i            : in  std_logic_vector(32-1 downto 0);  -- Observed max continuous stall in cycles
  stall_streak_max_V_i          : in  std_logic_vector(1-1 downto 0);   -- Valid flag - stall_streak_max
  time_dif_neg_i                : in  std_logic_vector(64-1 downto 0);  -- Observed max neg. ECA time difference in ns between ref clock ticks
  time_dif_neg_V_i              : in  std_logic_vector(1-1 downto 0);   -- Valid flag - time_dif_neg
  time_dif_neg_ts_i             : in  std_logic_vector(64-1 downto 0);  -- (approximate) timestamp of last neg dif update
  time_dif_neg_ts_V_i           : in  std_logic_vector(1-1 downto 0);   -- Valid flag - time_dif_neg_ts
  time_dif_pos_i                : in  std_logic_vector(64-1 downto 0);  -- Observed max pos. ECA time difference in ns between ref clock ticks
  time_dif_pos_V_i              : in  std_logic_vector(1-1 downto 0);   -- Valid flag - time_dif_pos
  time_dif_pos_ts_i             : in  std_logic_vector(64-1 downto 0);  -- (approximate) timestamp of last pos dif update
  time_dif_pos_ts_V_i           : in  std_logic_vector(1-1 downto 0);   -- Valid flag - time_dif_pos_ts
  wr_lock_acqu_last_ts_i        : in  std_logic_vector(64-1 downto 0);  -- timestamp of last wr lock acquired
  wr_lock_acqu_last_ts_V_i      : in  std_logic_vector(1-1 downto 0);   -- Valid flag - wr_lock_acqu_last_ts
  wr_lock_cnt_i                 : in  std_logic_vector(64-1 downto 0);  -- cnt of wr lock bit going from low to high
  wr_lock_cnt_V_i               : in  std_logic_vector(1-1 downto 0);   -- Valid flag - wr_lock_cnt
  wr_lock_loss_last_ts_i        : in  std_logic_vector(64-1 downto 0);  -- timestamp of last wr lock loss
  wr_lock_loss_last_ts_V_i      : in  std_logic_vector(1-1 downto 0);   -- Valid flag - wr_lock_loss_last_ts
  enable_o                      : out std_logic_vector(1-1 downto 0);   -- Enables/disables update. Default is enabled
  reset_o                       : out std_logic_vector(1-1 downto 0);   -- Resets/clears the diagnostic
  stall_observation_interval_o  : out std_logic_vector(32-1 downto 0);  -- Stall observation interval in cycles
  stall_stat_select_o           : out std_logic_vector(8-1 downto 0);   -- Page selector register for Stall observers
  stall_stat_select_RD_o        : out std_logic_vector(1-1 downto 0);   -- Read enable flag - stall_stat_select
  stall_stat_select_WR_o        : out std_logic_vector(1-1 downto 0);   -- Write enable flag - stall_stat_select
  time_observation_interval_o   : out std_logic_vector(64-1 downto 0);  -- TAI time observation interval in ns
  
  ctrl_i                        : in  t_wishbone_slave_in;
  ctrl_o                        : out t_wishbone_slave_out

  
);
end dm_diag;

architecture rtl of dm_diag is

  signal s_ctrl_error_i                       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Error control
  signal s_ctrl_stall_i                       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- flow control
  signal s_ctrl_reset_o                       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Resets/clears the diagnostic
  signal s_ctrl_enable_o                      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Enables/disables update. Default is enabled
  signal s_ctrl_time_observation_interval_o   : std_logic_vector(64-1 downto 0) := (others => '0'); -- TAI time observation interval in ns
  signal s_ctrl_time_dif_pos_V_i              : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - time_dif_pos
  signal s_ctrl_time_dif_pos_i                : std_logic_vector(64-1 downto 0) := (others => '0'); -- Observed max pos. ECA time difference in ns between ref clock ticks
  signal s_ctrl_time_dif_pos_ts_V_i           : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - time_dif_pos_ts
  signal s_ctrl_time_dif_pos_ts_i             : std_logic_vector(64-1 downto 0) := (others => '0'); -- (approximate) timestamp of last pos dif update
  signal s_ctrl_time_dif_neg_V_i              : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - time_dif_neg
  signal s_ctrl_time_dif_neg_i                : std_logic_vector(64-1 downto 0) := (others => '0'); -- Observed max neg. ECA time difference in ns between ref clock ticks
  signal s_ctrl_time_dif_neg_ts_V_i           : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - time_dif_neg_ts
  signal s_ctrl_time_dif_neg_ts_i             : std_logic_vector(64-1 downto 0) := (others => '0'); -- (approximate) timestamp of last neg dif update
  signal s_ctrl_wr_lock_cnt_V_i               : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - wr_lock_cnt
  signal s_ctrl_wr_lock_cnt_i                 : std_logic_vector(64-1 downto 0) := (others => '0'); -- cnt of wr lock bit going from low to high
  signal s_ctrl_wr_lock_loss_last_ts_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - wr_lock_loss_last_ts
  signal s_ctrl_wr_lock_loss_last_ts_i        : std_logic_vector(64-1 downto 0) := (others => '0'); -- timestamp of last wr lock loss
  signal s_ctrl_wr_lock_acqu_last_ts_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - wr_lock_acqu_last_ts
  signal s_ctrl_wr_lock_acqu_last_ts_i        : std_logic_vector(64-1 downto 0) := (others => '0'); -- timestamp of last wr lock acquired
  signal s_ctrl_stall_observation_interval_o  : std_logic_vector(32-1 downto 0) := (others => '0'); -- Stall observation interval in cycles
  signal s_ctrl_stall_stat_select_WR_o        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - stall_stat_select
  signal s_ctrl_stall_stat_select_RD_o        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - stall_stat_select
  signal s_ctrl_stall_stat_select_o           : std_logic_vector(8-1 downto 0)  := (others => '0'); -- Page selector register for Stall observers
  signal s_ctrl_stall_streak_max_V_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - stall_streak_max
  signal s_ctrl_stall_streak_max_i            : std_logic_vector(32-1 downto 0) := (others => '0'); -- Observed max continuous stall in cycles
  signal s_ctrl_stall_cnt_V_i                 : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - stall_cnt
  signal s_ctrl_stall_cnt_i                   : std_logic_vector(32-1 downto 0) := (others => '0'); -- Stall time within observation interval in cycles
  signal s_ctrl_stall_max_ts_V_i              : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - stall_max_ts
  signal s_ctrl_stall_max_ts_i                : std_logic_vector(64-1 downto 0) := (others => '0'); -- Timestamp of last max update
  


begin

  INST_dm_diag_auto : dm_diag_auto
  port map (
    clk_ref_i                     => clk_ref_i,
    rst_ref_n_i                   => rst_ref_n_i,
    error_i                       => s_ctrl_error_i,
    stall_i                       => s_ctrl_stall_i,
    reset_o                       => s_ctrl_reset_o,
    enable_o                      => s_ctrl_enable_o,
    time_observation_interval_o   => s_ctrl_time_observation_interval_o,
    time_dif_pos_V_i              => s_ctrl_time_dif_pos_V_i,
    time_dif_pos_i                => s_ctrl_time_dif_pos_i,
    time_dif_pos_ts_V_i           => s_ctrl_time_dif_pos_ts_V_i,
    time_dif_pos_ts_i             => s_ctrl_time_dif_pos_ts_i,
    time_dif_neg_V_i              => s_ctrl_time_dif_neg_V_i,
    time_dif_neg_i                => s_ctrl_time_dif_neg_i,
    time_dif_neg_ts_V_i           => s_ctrl_time_dif_neg_ts_V_i,
    time_dif_neg_ts_i             => s_ctrl_time_dif_neg_ts_i,
    wr_lock_cnt_V_i               => s_ctrl_wr_lock_cnt_V_i,
    wr_lock_cnt_i                 => s_ctrl_wr_lock_cnt_i,
    wr_lock_loss_last_ts_V_i      => s_ctrl_wr_lock_loss_last_ts_V_i,
    wr_lock_loss_last_ts_i        => s_ctrl_wr_lock_loss_last_ts_i,
    wr_lock_acqu_last_ts_V_i      => s_ctrl_wr_lock_acqu_last_ts_V_i,
    wr_lock_acqu_last_ts_i        => s_ctrl_wr_lock_acqu_last_ts_i,
    stall_observation_interval_o  => s_ctrl_stall_observation_interval_o,
    stall_stat_select_WR_o        => s_ctrl_stall_stat_select_WR_o,
    stall_stat_select_RD_o        => s_ctrl_stall_stat_select_RD_o,
    stall_stat_select_o           => s_ctrl_stall_stat_select_o,
    stall_streak_max_V_i          => s_ctrl_stall_streak_max_V_i,
    stall_streak_max_i            => s_ctrl_stall_streak_max_i,
    stall_cnt_V_i                 => s_ctrl_stall_cnt_V_i,
    stall_cnt_i                   => s_ctrl_stall_cnt_i,
    stall_max_ts_V_i              => s_ctrl_stall_max_ts_V_i,
    stall_max_ts_i                => s_ctrl_stall_max_ts_i,
    ctrl_i                        => ctrl_i,
    ctrl_o                        => ctrl_o  );
end rtl;
