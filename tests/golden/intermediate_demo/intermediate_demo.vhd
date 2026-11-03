--! @file        intermediate_demo.xml
--  DesignUnit   intermediate_demo
--! @author      M. Kreider <>
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
use work.intermediate_demo_auto_pkg.all;

entity intermediate_demo is
generic(
  g_channels  : natural := 16;  --Input channels
  g_flags     : natural := 4    --Flag bits
);
Port(
  clk_sys_i     : std_logic;                                              -- Clock input for sys domain
  rst_sys_n_i   : std_logic;                                              -- Reset input (active low) for sys domain
  error_i       : in  std_logic_vector(1-1 downto 0);                     -- Error control
  stall_i       : in  std_logic_vector(1-1 downto 0);                     -- flow control
  status_i      : in  std_logic_vector(g_channels-1 downto 0);            -- 'timestamps pending' bit per channel
  status_V_i    : in  std_logic_vector(1-1 downto 0);                     -- Valid flag - status
  ts_cnt_i      : in  matrix(g_channels-1 downto 0, 16-1 downto 0);       -- Shows channel timestamp count
  ts_cnt_V_i    : in  std_logic_vector(1-1 downto 0);                     -- Valid flag - ts_cnt
  ts_out_i      : in  matrix(g_channels-1 downto 0, 64-1 downto 0);       -- Timestamp fifos in. Use RD flag to pop
  ts_out_V_i    : in  std_logic_vector(1-1 downto 0);                     -- Valid flag - ts_out
  ch_sel_o      : out std_logic_vector(8-1 downto 0);                     -- Channel select register
  clear_fifo_o  : out matrix(g_channels-1 downto 0, 1-1 downto 0);        -- Clears Fifo
  ts_flags_o    : out matrix(g_channels-1 downto 0, g_flags-1 downto 0);  -- timestamp channel flagbits
  ts_out_RD_o   : out std_logic_vector(1-1 downto 0);                     -- Read enable flag - ts_out
  
  slave_i       : in  t_wishbone_slave_in;
  slave_o       : out t_wishbone_slave_out

  
);
end intermediate_demo;

architecture rtl of intermediate_demo is

  signal s_slave_error_i      : std_logic_vector(1-1 downto 0)                    := (others => '0'); -- Error control
  signal s_slave_stall_i      : std_logic_vector(1-1 downto 0)                    := (others => '0'); -- flow control
  signal s_slave_status_V_i   : std_logic_vector(1-1 downto 0)                    := (others => '0'); -- Valid flag - status
  signal s_slave_status_i     : std_logic_vector(g_channels-1 downto 0)           := (others => '0'); -- 'timestamps pending' bit per channel
  signal s_slave_ch_sel_o     : std_logic_vector(8-1 downto 0)                    := (others => '0'); -- Channel select register
  signal s_slave_clear_fifo_o : matrix(g_channels-1 downto 0, 1-1 downto 0)       := (others => '0'); -- Clears Fifo
  signal s_slave_ts_out_RD_o  : std_logic_vector(1-1 downto 0)                    := (others => '0'); -- Read enable flag - ts_out
  signal s_slave_ts_out_V_i   : std_logic_vector(1-1 downto 0)                    := (others => '0'); -- Valid flag - ts_out
  signal s_slave_ts_out_i     : matrix(g_channels-1 downto 0, 64-1 downto 0)      := (others => '0'); -- Timestamp fifos in. Use RD flag to pop
  signal s_slave_ts_cnt_V_i   : std_logic_vector(1-1 downto 0)                    := (others => '0'); -- Valid flag - ts_cnt
  signal s_slave_ts_cnt_i     : matrix(g_channels-1 downto 0, 16-1 downto 0)      := (others => '0'); -- Shows channel timestamp count
  signal s_slave_ts_flags_o   : matrix(g_channels-1 downto 0, g_flags-1 downto 0) := (others => '0'); -- timestamp channel flagbits
  


begin

  INST_intermediate_demo_auto : intermediate_demo_auto
  port map (
    clk_sys_i     => clk_sys_i,
    rst_sys_n_i   => rst_sys_n_i,
    error_i       => s_slave_error_i,
    stall_i       => s_slave_stall_i,
    status_V_i    => s_slave_status_V_i,
    status_i      => s_slave_status_i,
    ch_sel_o      => s_slave_ch_sel_o,
    clear_fifo_o  => s_slave_clear_fifo_o,
    ts_out_RD_o   => s_slave_ts_out_RD_o,
    ts_out_V_i    => s_slave_ts_out_V_i,
    ts_out_i      => s_slave_ts_out_i,
    ts_cnt_V_i    => s_slave_ts_cnt_V_i,
    ts_cnt_i      => s_slave_ts_cnt_i,
    ts_flags_o    => s_slave_ts_flags_o,
    slave_i       => slave_i,
    slave_o       => slave_o  );
end rtl;
