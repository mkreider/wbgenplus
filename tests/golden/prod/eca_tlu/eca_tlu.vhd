--! @file        eca_tlu.xml
--  DesignUnit   eca_tlu
--! @author      Wesley W. Terpstra <w.terpstra@gsi.de>
--! @date        14/11/2023
--! @version     2.0
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
use work.eca_tlu_auto_pkg.all;

entity eca_tlu is
generic(
  g_num_inputs  : natural := 0  --Total number of inputs attached to the TLU
);
Port(
  clk_sys_i       : std_logic;                            -- Clock input for sys domain
  rst_sys_n_i     : std_logic;                            -- Reset input (active low) for sys domain
  error_i         : in  std_logic_vector(1-1 downto 0);   -- Error control
  stall_i         : in  std_logic_vector(1-1 downto 0);   -- flow control
  enable_o        : out std_logic_vector(1-1 downto 0);   -- Will this input generate timing events on an edge
  event_hi_o      : out std_logic_vector(32-1 downto 0);  -- Timing Event to generate (high word)
  event_lo_o      : out std_logic_vector(32-1 downto 0);  -- Timing Event to generate (low word), lowest bit is replaced with the edge of the transition
  input_select_o  : out std_logic_vector(8-1 downto 0);   -- Write the configuration of this input
  stable_o        : out std_logic_vector(32-1 downto 0);  -- Signal must be high/low for stable cycles to be counted as a valid transition
  write_o         : out std_logic_vector(1-1 downto 0);   -- Write register contents to TLU configuration
  
  slave_i         : in  t_wishbone_slave_in;
  slave_o         : out t_wishbone_slave_out

  
);
end eca_tlu;

architecture rtl of eca_tlu is

  signal s_slave_error_i        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Error control
  signal s_slave_stall_i        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- flow control
  signal s_slave_input_select_o : std_logic_vector(8-1 downto 0)  := (others => '0'); -- Write the configuration of this input
  signal s_slave_enable_o       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Will this input generate timing events on an edge
  signal s_slave_stable_o       : std_logic_vector(32-1 downto 0) := (others => '0'); -- Signal must be high/low for stable cycles to be counted as a valid transition
  signal s_slave_event_hi_o     : std_logic_vector(32-1 downto 0) := (others => '0'); -- Timing Event to generate (high word)
  signal s_slave_event_lo_o     : std_logic_vector(32-1 downto 0) := (others => '0'); -- Timing Event to generate (low word), lowest bit is replaced with the edge of the transition
  signal s_slave_write_o        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write register contents to TLU configuration
  


begin

  INST_eca_tlu_auto : eca_tlu_auto
  port map (
    clk_sys_i       => clk_sys_i,
    rst_sys_n_i     => rst_sys_n_i,
    error_i         => s_slave_error_i,
    stall_i         => s_slave_stall_i,
    input_select_o  => s_slave_input_select_o,
    enable_o        => s_slave_enable_o,
    stable_o        => s_slave_stable_o,
    event_hi_o      => s_slave_event_hi_o,
    event_lo_o      => s_slave_event_lo_o,
    write_o         => s_slave_write_o,
    slave_i         => slave_i,
    slave_o         => slave_o  );
end rtl;
