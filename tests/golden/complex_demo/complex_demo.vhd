--! @file        complex_demo.xml
--  DesignUnit   complex_demo
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
use work.complex_demo_auto_pkg.all;

entity complex_demo is
generic(
  g_channels  : natural := 16 --Input channels
);
Port(
  clk_sys_i                 : std_logic;                                        -- Clock input for sys domain
  rst_sys_n_i               : std_logic;                                        -- Reset input (active low) for sys domain
  clk_ref_i                 : std_logic;                                        -- Clock input for ref domain
  rst_ref_n_i               : std_logic;                                        -- Reset input (active low) for ref domain
  status_ref_i              : in  std_logic_vector(g_channels-1 downto 0);      -- tlu 'timestamps pending' bit per channel
  status_V_ref_i            : in  std_logic_vector(1-1 downto 0);               -- Valid flag - status
  cmd_ref_o                 : out std_logic_vector(16-1 downto 0);              -- Cmd for tlu controller
  cmd_fifo_out_pop_ref_i    : in std_logic;
  cmd_fifo_out_empty_ref_o  : out std_logic;
  cnt_i                     : in  matrix(g_channels-1 downto 0, 16-1 downto 0); -- Shows channel timestamp count
  cnt_V_i                   : in  std_logic_vector(1-1 downto 0);               -- Valid flag - cnt
  error_i                   : in  std_logic_vector(1-1 downto 0);               -- Error control
  stall_i                   : in  std_logic_vector(1-1 downto 0);               -- flow control
  ts_out_i                  : in  matrix(g_channels-1 downto 0, 64-1 downto 0); -- Timestamp fifos in. Use RD flag to pop
  ts_out_V_i                : in  std_logic_vector(1-1 downto 0);               -- Valid flag - ts_out
  ch_sel_o                  : out std_logic_vector(8-1 downto 0);               -- Channel select register
  clear_fifo_o              : out matrix(g_channels-1 downto 0, 1-1 downto 0);  -- Clears Fifo
  ts_flags_o                : out matrix(g_channels-1 downto 0, 32-1 downto 0); -- timestamp channel flagbits
  ts_out_RD_o               : out std_logic_vector(1-1 downto 0);               -- Read enable flag - ts_out
  
  data_i                    : in  t_wishbone_slave_in;
  data_o                    : out t_wishbone_slave_out

  
  
  
);
end complex_demo;

architecture rtl of complex_demo is

  signal s_data_error_i         : std_logic_vector(1-1 downto 0)                := (others => '0'); -- Error control
  signal s_data_stall_i         : std_logic_vector(1-1 downto 0)                := (others => '0'); -- flow control
  signal s_data_status_V_ref_i  : std_logic_vector(1-1 downto 0)                := (others => '0'); -- Valid flag - status
  signal s_data_status_ref_i    : std_logic_vector(g_channels-1 downto 0)       := (others => '0'); -- tlu 'timestamps pending' bit per channel
  signal s_data_cmd_ref_o       : std_logic_vector(16-1 downto 0)               := (others => '0'); -- Cmd for tlu controller
  signal s_data_ch_sel_o        : std_logic_vector(8-1 downto 0)                := (others => '0'); -- Channel select register
  signal s_data_clear_fifo_o    : matrix(g_channels-1 downto 0, 1-1 downto 0)   := (others => '0'); -- Clears Fifo
  signal s_data_ts_out_RD_o     : std_logic_vector(1-1 downto 0)                := (others => '0'); -- Read enable flag - ts_out
  signal s_data_ts_out_V_i      : std_logic_vector(1-1 downto 0)                := (others => '0'); -- Valid flag - ts_out
  signal s_data_ts_out_i        : matrix(g_channels-1 downto 0, 64-1 downto 0)  := (others => '0'); -- Timestamp fifos in. Use RD flag to pop
  signal s_data_cnt_V_i         : std_logic_vector(1-1 downto 0)                := (others => '0'); -- Valid flag - cnt
  signal s_data_cnt_i           : matrix(g_channels-1 downto 0, 16-1 downto 0)  := (others => '0'); -- Shows channel timestamp count
  signal s_data_ts_flags_o      : matrix(g_channels-1 downto 0, 32-1 downto 0)  := (others => '0'); -- timestamp channel flagbits
  


begin

  INST_complex_demo_auto : complex_demo_auto
  port map (
    clk_sys_i       => clk_sys_i,
    rst_sys_n_i     => rst_sys_n_i,
    clk_ref_i       => clk_ref_i,
    rst_ref_n_i     => rst_ref_n_i,
    error_i         => s_data_error_i,
    stall_i         => s_data_stall_i,
    status_V_ref_i  => s_data_status_V_ref_i,
    status_ref_i    => s_data_status_ref_i,
    cmd_ref_o       => s_data_cmd_ref_o,
    ch_sel_o        => s_data_ch_sel_o,
    clear_fifo_o    => s_data_clear_fifo_o,
    ts_out_RD_o     => s_data_ts_out_RD_o,
    ts_out_V_i      => s_data_ts_out_V_i,
    ts_out_i        => s_data_ts_out_i,
    cnt_V_i         => s_data_cnt_V_i,
    cnt_i           => s_data_cnt_i,
    ts_flags_o      => s_data_ts_flags_o,
    data_i          => data_i,
    data_o          => data_o  );
end rtl;
