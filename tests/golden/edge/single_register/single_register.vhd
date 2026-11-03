--! @file        single_register.xml
--  DesignUnit   single_register
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
use work.single_register_auto_pkg.all;

entity single_register is
Port(
  clk_sys_i   : std_logic;                          -- Clock input for sys domain
  rst_sys_n_i : std_logic;                          -- Reset input (active low) for sys domain
  error_i     : in  std_logic_vector(1-1 downto 0); -- Error control
  stall_i     : in  std_logic_vector(1-1 downto 0); -- flow control
  value_o     : out std_logic_vector(8-1 downto 0); -- only register
  
  ctrl_i      : in  t_wishbone_slave_in;
  ctrl_o      : out t_wishbone_slave_out

  
);
end single_register;

architecture rtl of single_register is

  signal s_ctrl_error_i : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Error control
  signal s_ctrl_stall_i : std_logic_vector(1-1 downto 0)  := (others => '0'); -- flow control
  signal s_ctrl_value_o : std_logic_vector(8-1 downto 0)  := (others => '0'); -- only register
  


begin

  INST_single_register_auto : single_register_auto
  port map (
    clk_sys_i   => clk_sys_i,
    rst_sys_n_i => rst_sys_n_i,
    error_i     => s_ctrl_error_i,
    stall_i     => s_ctrl_stall_i,
    value_o     => s_ctrl_value_o,
    ctrl_i      => ctrl_i,
    ctrl_o      => ctrl_o  );
end rtl;
