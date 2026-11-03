--! @file        wide_low.xml
--  DesignUnit   wide_low
--! @author      T <t@x>
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
use work.wide_low_auto_pkg.all;

entity wide_low is
Port(
  clk_sys_i   : std_logic;                            -- Clock input for sys domain
  rst_sys_n_i : std_logic;                            -- Reset input (active low) for sys domain
  error_i     : in  std_logic_vector(1-1 downto 0);   -- Error control
  stall_i     : in  std_logic_vector(1-1 downto 0);   -- flow control
  stat_i      : in  std_logic_vector(64-1 downto 0);  -- 64 bit, driven
  stat_V_i    : in  std_logic_vector(1-1 downto 0);   -- Valid flag - stat
  first_o     : out std_logic_vector(8-1 downto 0);   -- before
  wide_o      : out std_logic_vector(48-1 downto 0);  -- 48 bit, not a multiple of the bus width
  
  ctrl_i      : in  t_wishbone_slave_in;
  ctrl_o      : out t_wishbone_slave_out

  
);
end wide_low;

architecture rtl of wide_low is

  signal s_ctrl_error_i   : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Error control
  signal s_ctrl_stall_i   : std_logic_vector(1-1 downto 0)  := (others => '0'); -- flow control
  signal s_ctrl_first_o   : std_logic_vector(8-1 downto 0)  := (others => '0'); -- before
  signal s_ctrl_wide_o    : std_logic_vector(48-1 downto 0) := (others => '0'); -- 48 bit, not a multiple of the bus width
  signal s_ctrl_stat_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - stat
  signal s_ctrl_stat_i    : std_logic_vector(64-1 downto 0) := (others => '0'); -- 64 bit, driven
  


begin

  INST_wide_low_auto : wide_low_auto
  port map (
    clk_sys_i   => clk_sys_i,
    rst_sys_n_i => rst_sys_n_i,
    error_i     => s_ctrl_error_i,
    stall_i     => s_ctrl_stall_i,
    first_o     => s_ctrl_first_o,
    wide_o      => s_ctrl_wide_o,
    stat_V_i    => s_ctrl_stat_V_i,
    stat_i      => s_ctrl_stat_i,
    ctrl_i      => ctrl_i,
    ctrl_o      => ctrl_o  );
end rtl;
