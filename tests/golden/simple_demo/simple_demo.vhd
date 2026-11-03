--! @file        simple_demo.xml
--  DesignUnit   simple_demo
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
use work.simple_demo_auto_pkg.all;

entity simple_demo is
generic(
  g_statusbits  : natural := 16 --Number of bits in status register
);
Port(
  clk_sys_i   : std_logic;                                      -- Clock input for sys domain
  rst_sys_n_i : std_logic;                                      -- Reset input (active low) for sys domain
  count_i     : in  std_logic_vector(16-1 downto 0);            -- Shows Data Input Counter
  count_V_i   : in  std_logic_vector(1-1 downto 0);             -- Valid flag - count
  error_i     : in  std_logic_vector(1-1 downto 0);             -- Error control
  scpad_V_i   : in  std_logic_vector(1-1 downto 0);             -- Valid flag - scpad
  stall_i     : in  std_logic_vector(1-1 downto 0);             -- flow control
  status_i    : in  std_logic_vector(g_statusbits-1 downto 0);  -- Shows if the devices are rdy/busy
  status_V_i  : in  std_logic_vector(1-1 downto 0);             -- Valid flag - status
  mode_o      : out std_logic_vector(8-1 downto 0);             -- Mode
  mode_RD_o   : out std_logic_vector(1-1 downto 0);             -- Read enable flag - mode
  mode_WR_o   : out std_logic_vector(1-1 downto 0);             -- Write enable flag - mode
  scpad_o     : out std_logic_vector(64-1 downto 0);            -- Scratchpad. Can be modified from Bus or outer entity
  scpad_i     : in  std_logic_vector(64-1 downto 0);            -- Scratchpad. Can be modified from Bus or outer entity
  scpad_RD_o  : out std_logic_vector(1-1 downto 0);             -- Read enable flag - scpad
  scpad_WR_o  : out std_logic_vector(1-1 downto 0);             -- Write enable flag - scpad
  
  slave_i     : in  t_wishbone_slave_in;
  slave_o     : out t_wishbone_slave_out

  
);
end simple_demo;

architecture rtl of simple_demo is

  signal s_slave_error_i    : std_logic_vector(1-1 downto 0)            := (others => '0'); -- Error control
  signal s_slave_stall_i    : std_logic_vector(1-1 downto 0)            := (others => '0'); -- flow control
  signal s_slave_status_V_i : std_logic_vector(1-1 downto 0)            := (others => '0'); -- Valid flag - status
  signal s_slave_status_i   : std_logic_vector(g_statusbits-1 downto 0) := (others => '0'); -- Shows if the devices are rdy/busy
  signal s_slave_mode_WR_o  : std_logic_vector(1-1 downto 0)            := (others => '0'); -- Write enable flag - mode
  signal s_slave_mode_RD_o  : std_logic_vector(1-1 downto 0)            := (others => '0'); -- Read enable flag - mode
  signal s_slave_mode_o     : std_logic_vector(8-1 downto 0)            := (others => '0'); -- Mode
  signal s_slave_scpad_WR_o : std_logic_vector(1-1 downto 0)            := (others => '0'); -- Write enable flag - scpad
  signal s_slave_scpad_RD_o : std_logic_vector(1-1 downto 0)            := (others => '0'); -- Read enable flag - scpad
  signal s_slave_scpad_V_i  : std_logic_vector(1-1 downto 0)            := (others => '0'); -- Valid flag - scpad
  signal s_slave_scpad_o    : std_logic_vector(64-1 downto 0)           := (others => '0'); -- Scratchpad. Can be modified from Bus or outer entity
  signal s_slave_scpad_i    : std_logic_vector(64-1 downto 0)           := (others => '0'); -- Scratchpad. Can be modified from Bus or outer entity
  signal s_slave_count_V_i  : std_logic_vector(1-1 downto 0)            := (others => '0'); -- Valid flag - count
  signal s_slave_count_i    : std_logic_vector(16-1 downto 0)           := (others => '0'); -- Shows Data Input Counter
  


begin

  INST_simple_demo_auto : simple_demo_auto
  port map (
    clk_sys_i   => clk_sys_i,
    rst_sys_n_i => rst_sys_n_i,
    error_i     => s_slave_error_i,
    stall_i     => s_slave_stall_i,
    status_V_i  => s_slave_status_V_i,
    status_i    => s_slave_status_i,
    mode_WR_o   => s_slave_mode_WR_o,
    mode_RD_o   => s_slave_mode_RD_o,
    mode_o      => s_slave_mode_o,
    scpad_WR_o  => s_slave_scpad_WR_o,
    scpad_RD_o  => s_slave_scpad_RD_o,
    scpad_V_i   => s_slave_scpad_V_i,
    scpad_o     => s_slave_scpad_o,
    scpad_i     => s_slave_scpad_i,
    count_V_i   => s_slave_count_V_i,
    count_i     => s_slave_count_i,
    slave_i     => slave_i,
    slave_o     => slave_o  );
end rtl;
