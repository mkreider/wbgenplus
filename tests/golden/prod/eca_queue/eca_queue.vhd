--! @file        eca_queue.xml
--  DesignUnit   eca_queue
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
use work.eca_queue_auto_pkg.all;

entity eca_queue is
generic(
  g_queue_id  : natural := 0  --The index of a_channel_o from the ECA to which this queue is connected (set channel_select=queue_id+1)
);
Port(
  clk_sys_i       : std_logic;                            -- Clock input for sys domain
  rst_sys_n_i     : std_logic;                            -- Reset input (active low) for sys domain
  deadline_hi_i   : in  std_logic_vector(32-1 downto 0);  -- Deadline (high word)
  deadline_hi_V_i : in  std_logic_vector(1-1 downto 0);   -- Valid flag - deadline_hi
  deadline_lo_i   : in  std_logic_vector(32-1 downto 0);  -- Deadline (low word)
  deadline_lo_V_i : in  std_logic_vector(1-1 downto 0);   -- Valid flag - deadline_lo
  error_i         : in  std_logic_vector(1-1 downto 0);   -- Error control
  event_id_hi_i   : in  std_logic_vector(32-1 downto 0);  -- Event ID (high word)
  event_id_hi_V_i : in  std_logic_vector(1-1 downto 0);   -- Valid flag - event_id_hi
  event_id_lo_i   : in  std_logic_vector(32-1 downto 0);  -- Event ID (low word)
  event_id_lo_V_i : in  std_logic_vector(1-1 downto 0);   -- Valid flag - event_id_lo
  executed_hi_i   : in  std_logic_vector(32-1 downto 0);  -- Actual execution time (high word)
  executed_hi_V_i : in  std_logic_vector(1-1 downto 0);   -- Valid flag - executed_hi
  executed_lo_i   : in  std_logic_vector(32-1 downto 0);  -- Actual execution time (low word)
  executed_lo_V_i : in  std_logic_vector(1-1 downto 0);   -- Valid flag - executed_lo
  flags_i         : in  std_logic_vector(5-1 downto 0);   -- Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  flags_V_i       : in  std_logic_vector(1-1 downto 0);   -- Valid flag - flags
  num_i           : in  std_logic_vector(8-1 downto 0);   -- Subchannel target
  num_V_i         : in  std_logic_vector(1-1 downto 0);   -- Valid flag - num
  param_hi_i      : in  std_logic_vector(32-1 downto 0);  -- Parameter (high word)
  param_hi_V_i    : in  std_logic_vector(1-1 downto 0);   -- Valid flag - param_hi
  param_lo_i      : in  std_logic_vector(32-1 downto 0);  -- Parameter (low word)
  param_lo_V_i    : in  std_logic_vector(1-1 downto 0);   -- Valid flag - param_lo
  stall_i         : in  std_logic_vector(1-1 downto 0);   -- flow control
  tag_i           : in  std_logic_vector(32-1 downto 0);  -- Tag from the condition
  tag_V_i         : in  std_logic_vector(1-1 downto 0);   -- Valid flag - tag
  tef_i           : in  std_logic_vector(32-1 downto 0);  -- Timing extension field
  tef_V_i         : in  std_logic_vector(1-1 downto 0);   -- Valid flag - tef
  pop_o           : out std_logic_vector(1-1 downto 0);   -- Pop action from the channel's queue
  
  slave_i         : in  t_wishbone_slave_in;
  slave_o         : out t_wishbone_slave_out

  
);
end eca_queue;

architecture rtl of eca_queue is

  signal s_slave_error_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Error control
  signal s_slave_stall_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- flow control
  signal s_slave_pop_o            : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Pop action from the channel's queue
  signal s_slave_flags_V_i        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - flags
  signal s_slave_flags_i          : std_logic_vector(5-1 downto 0)  := (others => '0'); -- Error flags for this action(0=late, 1=early, 2=conflict, 3=delayed, 4=valid)
  signal s_slave_num_V_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - num
  signal s_slave_num_i            : std_logic_vector(8-1 downto 0)  := (others => '0'); -- Subchannel target
  signal s_slave_event_id_hi_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - event_id_hi
  signal s_slave_event_id_hi_i    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Event ID (high word)
  signal s_slave_event_id_lo_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - event_id_lo
  signal s_slave_event_id_lo_i    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Event ID (low word)
  signal s_slave_param_hi_V_i     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - param_hi
  signal s_slave_param_hi_i       : std_logic_vector(32-1 downto 0) := (others => '0'); -- Parameter (high word)
  signal s_slave_param_lo_V_i     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - param_lo
  signal s_slave_param_lo_i       : std_logic_vector(32-1 downto 0) := (others => '0'); -- Parameter (low word)
  signal s_slave_tag_V_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - tag
  signal s_slave_tag_i            : std_logic_vector(32-1 downto 0) := (others => '0'); -- Tag from the condition
  signal s_slave_tef_V_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - tef
  signal s_slave_tef_i            : std_logic_vector(32-1 downto 0) := (others => '0'); -- Timing extension field
  signal s_slave_deadline_hi_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - deadline_hi
  signal s_slave_deadline_hi_i    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Deadline (high word)
  signal s_slave_deadline_lo_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - deadline_lo
  signal s_slave_deadline_lo_i    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Deadline (low word)
  signal s_slave_executed_hi_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - executed_hi
  signal s_slave_executed_hi_i    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Actual execution time (high word)
  signal s_slave_executed_lo_V_i  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - executed_lo
  signal s_slave_executed_lo_i    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Actual execution time (low word)
  


begin

  INST_eca_queue_auto : eca_queue_auto
  port map (
    clk_sys_i       => clk_sys_i,
    rst_sys_n_i     => rst_sys_n_i,
    error_i         => s_slave_error_i,
    stall_i         => s_slave_stall_i,
    pop_o           => s_slave_pop_o,
    flags_V_i       => s_slave_flags_V_i,
    flags_i         => s_slave_flags_i,
    num_V_i         => s_slave_num_V_i,
    num_i           => s_slave_num_i,
    event_id_hi_V_i => s_slave_event_id_hi_V_i,
    event_id_hi_i   => s_slave_event_id_hi_i,
    event_id_lo_V_i => s_slave_event_id_lo_V_i,
    event_id_lo_i   => s_slave_event_id_lo_i,
    param_hi_V_i    => s_slave_param_hi_V_i,
    param_hi_i      => s_slave_param_hi_i,
    param_lo_V_i    => s_slave_param_lo_V_i,
    param_lo_i      => s_slave_param_lo_i,
    tag_V_i         => s_slave_tag_V_i,
    tag_i           => s_slave_tag_i,
    tef_V_i         => s_slave_tef_V_i,
    tef_i           => s_slave_tef_i,
    deadline_hi_V_i => s_slave_deadline_hi_V_i,
    deadline_hi_i   => s_slave_deadline_hi_i,
    deadline_lo_V_i => s_slave_deadline_lo_V_i,
    deadline_lo_i   => s_slave_deadline_lo_i,
    executed_hi_V_i => s_slave_executed_hi_V_i,
    executed_hi_i   => s_slave_executed_hi_i,
    executed_lo_V_i => s_slave_executed_lo_V_i,
    executed_lo_i   => s_slave_executed_lo_i,
    slave_i         => slave_i,
    slave_o         => slave_o  );
end rtl;
