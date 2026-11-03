--! @file        eca.xml
--  DesignUnit   eca
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
use work.eca_auto_pkg.all;

entity eca is
generic(
  g_channels        : natural := 1;     --Number of channels implemented by the ECA, including the internal IO channel #0
  g_search_capacity : natural := 512;   --Total number of search table entries per active page
  g_walker_capacity : natural := 256;   --Total number of walker table entries per active page
  g_latency         : natural := 4096;  --Delay in ticks (typically nanoseconds) between an event's arrival at the ECA and its earliest possible execution as an action
  g_offset_bits     : natural := 32     --Actions scheduled for execution with a delay in ticks exceeding offset_bits are executed early
);
Port(
  clk_sys_i                   : std_logic;                            -- Clock input for sys domain
  rst_sys_n_i                 : std_logic;                            -- Reset input (active low) for sys domain
  channel_capacity_i          : in  std_logic_vector(16-1 downto 0);  -- Total number of actions which may be enqueued by the selected channel at a time
  channel_capacity_V_i        : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_capacity
  channel_deadline_hi_i       : in  std_logic_vector(32-1 downto 0);  -- The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  channel_deadline_hi_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_deadline_hi
  channel_deadline_lo_i       : in  std_logic_vector(32-1 downto 0);  -- The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  channel_deadline_lo_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_deadline_lo
  channel_event_id_hi_i       : in  std_logic_vector(32-1 downto 0);  -- The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  channel_event_id_hi_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_event_id_hi
  channel_event_id_lo_i       : in  std_logic_vector(32-1 downto 0);  -- The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  channel_event_id_lo_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_event_id_lo
  channel_executed_hi_i       : in  std_logic_vector(32-1 downto 0);  -- The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  channel_executed_hi_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_executed_hi
  channel_executed_lo_i       : in  std_logic_vector(32-1 downto 0);  -- The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  channel_executed_lo_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_executed_lo
  channel_failed_count_i      : in  std_logic_vector(32-1 downto 0);  -- Read and clear the number of actions with the selected error code which were destined for the selected subchannel, MSI=(code<<16|num) will be sent when the count becomes non-zero
  channel_failed_count_V_i    : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_failed_count
  channel_max_num_i           : in  std_logic_vector(8-1 downto 0);   -- Total number of subchannels supported by the selected channel
  channel_max_num_V_i         : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_max_num
  channel_mostfull_ack_i      : in  std_logic_vector(32-1 downto 0);  -- Read the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  channel_mostfull_ack_V_i    : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_mostfull_ack
  channel_mostfull_clear_i    : in  std_logic_vector(32-1 downto 0);  -- Read and clear the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  channel_mostfull_clear_V_i  : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_mostfull_clear
  channel_msi_get_enable_i    : in  std_logic_vector(1-1 downto 0);   -- Check if MSI messages are enabled for the selected channel
  channel_msi_get_enable_V_i  : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_msi_get_enable
  channel_msi_get_target_i    : in  std_logic_vector(32-1 downto 0);  -- Get the destination MSI address for the selected channel
  channel_msi_get_target_V_i  : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_msi_get_target
  channel_overflow_count_i    : in  std_logic_vector(32-1 downto 0);  -- Read and clear the number of actions which could not be enqueued to the selected full channel which were destined for the selected subchannel, MSI=(5<<16|num) will be sent when the count becomes non-zero
  channel_overflow_count_V_i  : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_overflow_count
  channel_param_hi_i          : in  std_logic_vector(32-1 downto 0);  -- The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  channel_param_hi_V_i        : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_param_hi
  channel_param_lo_i          : in  std_logic_vector(32-1 downto 0);  -- The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  channel_param_lo_V_i        : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_param_lo
  channel_tag_i               : in  std_logic_vector(32-1 downto 0);  -- The tag of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  channel_tag_V_i             : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_tag
  channel_tef_i               : in  std_logic_vector(32-1 downto 0);  -- The TEF of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  channel_tef_V_i             : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_tef
  channel_type_i              : in  std_logic_vector(32-1 downto 0);  -- Type of the selected channel (0=io, 1=linux, 2=wbm, ...)
  channel_type_V_i            : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_type
  channel_valid_count_i       : in  std_logic_vector(32-1 downto 0);  -- Read and clear the number of actions output by the selected subchannel, MSI=(4<<16|num) will be sent when the count becomes non-zero
  channel_valid_count_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - channel_valid_count
  error_i                     : in  std_logic_vector(1-1 downto 0);   -- Error control
  search_ro_event_hi_i        : in  std_logic_vector(32-1 downto 0);  -- Event IDs greater than or equal to this value match this search table record (high word)
  search_ro_event_hi_V_i      : in  std_logic_vector(1-1 downto 0);   -- Valid flag - search_ro_event_hi
  search_ro_event_lo_i        : in  std_logic_vector(32-1 downto 0);  -- Event IDs greater than or equal to this value match this search table record (low word)
  search_ro_event_lo_V_i      : in  std_logic_vector(1-1 downto 0);   -- Valid flag - search_ro_event_lo
  search_ro_first_i           : in  std_logic_vector(16-1 downto 0);  -- The first walker entry to execute if an event matches this record in the search table
  search_ro_first_V_i         : in  std_logic_vector(1-1 downto 0);   -- Valid flag - search_ro_first
  stall_i                     : in  std_logic_vector(1-1 downto 0);   -- flow control
  time_hi_i                   : in  std_logic_vector(32-1 downto 0);  -- Ticks (nanoseconds) since Jan 1, 1970 (high word)
  time_hi_V_i                 : in  std_logic_vector(1-1 downto 0);   -- Valid flag - time_hi
  time_lo_i                   : in  std_logic_vector(32-1 downto 0);  -- Ticks (nanoseconds) since Jan 1, 1970 (low word)
  time_lo_V_i                 : in  std_logic_vector(1-1 downto 0);   -- Valid flag - time_lo
  walker_ro_channel_i         : in  std_logic_vector(8-1 downto 0);   -- The channel to which the resulting action will be sent
  walker_ro_channel_V_i       : in  std_logic_vector(1-1 downto 0);   -- Valid flag - walker_ro_channel
  walker_ro_flags_i           : in  std_logic_vector(4-1 downto 0);   -- Execute the resulting action even if it suffers from the errors set in this flag register
  walker_ro_flags_V_i         : in  std_logic_vector(1-1 downto 0);   -- Valid flag - walker_ro_flags
  walker_ro_next_i            : in  std_logic_vector(16-1 downto 0);  -- The next walker entry to execute after this record (0xffff = end of list)
  walker_ro_next_V_i          : in  std_logic_vector(1-1 downto 0);   -- Valid flag - walker_ro_next
  walker_ro_num_i             : in  std_logic_vector(8-1 downto 0);   -- The subchannel to which the resulting action will be sent
  walker_ro_num_V_i           : in  std_logic_vector(1-1 downto 0);   -- Valid flag - walker_ro_num
  walker_ro_offset_hi_i       : in  std_logic_vector(32-1 downto 0);  -- The resulting action's deadline is the event timestamp plus this offset (high word)
  walker_ro_offset_hi_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - walker_ro_offset_hi
  walker_ro_offset_lo_i       : in  std_logic_vector(32-1 downto 0);  -- The resulting action's deadline is the event timestamp plus this offset (low word)
  walker_ro_offset_lo_V_i     : in  std_logic_vector(1-1 downto 0);   -- Valid flag - walker_ro_offset_lo
  walker_ro_tag_i             : in  std_logic_vector(32-1 downto 0);  -- The resulting actions's tag
  walker_ro_tag_V_i           : in  std_logic_vector(1-1 downto 0);   -- Valid flag - walker_ro_tag
  channel_code_select_o       : out std_logic_vector(2-1 downto 0);   -- Read/clear this error condition (0=late, 1=early, 2=conflict, 3=delayed)
  channel_deadline_hi_RD_o    : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_deadline_hi
  channel_deadline_lo_RD_o    : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_deadline_lo
  channel_event_id_hi_RD_o    : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_event_id_hi
  channel_event_id_lo_RD_o    : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_event_id_lo
  channel_executed_hi_RD_o    : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_executed_hi
  channel_executed_lo_RD_o    : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_executed_lo
  channel_failed_count_RD_o   : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_failed_count
  channel_mostfull_ack_RD_o   : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_mostfull_ack
  channel_mostfull_clear_RD_o : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_mostfull_clear
  channel_msi_set_enable_o    : out std_logic_vector(1-1 downto 0);   -- Turn on/off MSI messages for the selected channel
  channel_msi_set_enable_WR_o : out std_logic_vector(1-1 downto 0);   -- Write enable flag - channel_msi_set_enable
  channel_msi_set_target_o    : out std_logic_vector(32-1 downto 0);  -- Set the destination MSI address for the selected channel (only possible while it has MSIs disabled)
  channel_msi_set_target_WR_o : out std_logic_vector(1-1 downto 0);   -- Write enable flag - channel_msi_set_target
  channel_num_select_o        : out std_logic_vector(8-1 downto 0);   -- Read/clear this subchannel
  channel_overflow_count_RD_o : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_overflow_count
  channel_param_hi_RD_o       : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_param_hi
  channel_param_lo_RD_o       : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_param_lo
  channel_select_o            : out std_logic_vector(8-1 downto 0);   -- Read/clear this channel
  channel_select_RD_o         : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_select
  channel_select_WR_o         : out std_logic_vector(1-1 downto 0);   -- Write enable flag - channel_select
  channel_tag_RD_o            : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_tag
  channel_tef_RD_o            : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_tef
  channel_valid_count_RD_o    : out std_logic_vector(1-1 downto 0);   -- Read enable flag - channel_valid_count
  flip_active_o               : out std_logic_vector(1-1 downto 0);   -- Flip the active search and walker tables with the inactive tables
  search_rw_event_hi_o        : out std_logic_vector(32-1 downto 0);  -- Scratch register to be written to search_ro_event_hi
  search_rw_event_lo_o        : out std_logic_vector(32-1 downto 0);  -- Scratch register to be written to search_ro_event_lo
  search_rw_first_o           : out std_logic_vector(16-1 downto 0);  -- Scratch register to be written to search_ro_first
  search_select_o             : out std_logic_vector(16-1 downto 0);  -- Read/write this record in the inactive search table
  search_select_RD_o          : out std_logic_vector(1-1 downto 0);   -- Read enable flag - search_select
  search_select_WR_o          : out std_logic_vector(1-1 downto 0);   -- Write enable flag - search_select
  search_write_o              : out std_logic_vector(1-1 downto 0);   -- Store the scratch registers to the inactive search table record search_select
  walker_rw_channel_o         : out std_logic_vector(8-1 downto 0);   -- Scratch register to be written to walker_ro_channel
  walker_rw_flags_o           : out std_logic_vector(4-1 downto 0);   -- Scratch register to be written to walker_ro_flags
  walker_rw_next_o            : out std_logic_vector(16-1 downto 0);  -- Scratch register to be written to walker_ro_next
  walker_rw_num_o             : out std_logic_vector(8-1 downto 0);   -- Scratch register to be written to walker_ro_num
  walker_rw_offset_hi_o       : out std_logic_vector(32-1 downto 0);  -- Scratch register to be written to walker_ro_offset_hi
  walker_rw_offset_lo_o       : out std_logic_vector(32-1 downto 0);  -- Scratch register to be written to walker_ro_offset_lo
  walker_rw_tag_o             : out std_logic_vector(32-1 downto 0);  -- Scratch register to be written to walker_ro_tag
  walker_select_o             : out std_logic_vector(16-1 downto 0);  -- Read/write this record in the inactive walker table
  walker_select_RD_o          : out std_logic_vector(1-1 downto 0);   -- Read enable flag - walker_select
  walker_select_WR_o          : out std_logic_vector(1-1 downto 0);   -- Write enable flag - walker_select
  walker_write_o              : out std_logic_vector(1-1 downto 0);   -- Store the scratch registers to the inactive walker table record walker_select
  
  slave_i                     : in  t_wishbone_slave_in;
  slave_o                     : out t_wishbone_slave_out

  
);
end eca;

architecture rtl of eca is

  signal s_slave_error_i                      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Error control
  signal s_slave_stall_i                      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- flow control
  signal s_slave_flip_active_o                : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Flip the active search and walker tables with the inactive tables
  signal s_slave_time_hi_V_i                  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - time_hi
  signal s_slave_time_hi_i                    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Ticks (nanoseconds) since Jan 1, 1970 (high word)
  signal s_slave_time_lo_V_i                  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - time_lo
  signal s_slave_time_lo_i                    : std_logic_vector(32-1 downto 0) := (others => '0'); -- Ticks (nanoseconds) since Jan 1, 1970 (low word)
  signal s_slave_search_select_WR_o           : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - search_select
  signal s_slave_search_select_RD_o           : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - search_select
  signal s_slave_search_select_o              : std_logic_vector(16-1 downto 0) := (others => '0'); -- Read/write this record in the inactive search table
  signal s_slave_search_rw_first_o            : std_logic_vector(16-1 downto 0) := (others => '0'); -- Scratch register to be written to search_ro_first
  signal s_slave_search_rw_event_hi_o         : std_logic_vector(32-1 downto 0) := (others => '0'); -- Scratch register to be written to search_ro_event_hi
  signal s_slave_search_rw_event_lo_o         : std_logic_vector(32-1 downto 0) := (others => '0'); -- Scratch register to be written to search_ro_event_lo
  signal s_slave_search_write_o               : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Store the scratch registers to the inactive search table record search_select
  signal s_slave_search_ro_first_V_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - search_ro_first
  signal s_slave_search_ro_first_i            : std_logic_vector(16-1 downto 0) := (others => '0'); -- The first walker entry to execute if an event matches this record in the search table
  signal s_slave_search_ro_event_hi_V_i       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - search_ro_event_hi
  signal s_slave_search_ro_event_hi_i         : std_logic_vector(32-1 downto 0) := (others => '0'); -- Event IDs greater than or equal to this value match this search table record (high word)
  signal s_slave_search_ro_event_lo_V_i       : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - search_ro_event_lo
  signal s_slave_search_ro_event_lo_i         : std_logic_vector(32-1 downto 0) := (others => '0'); -- Event IDs greater than or equal to this value match this search table record (low word)
  signal s_slave_walker_select_WR_o           : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - walker_select
  signal s_slave_walker_select_RD_o           : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - walker_select
  signal s_slave_walker_select_o              : std_logic_vector(16-1 downto 0) := (others => '0'); -- Read/write this record in the inactive walker table
  signal s_slave_walker_rw_next_o             : std_logic_vector(16-1 downto 0) := (others => '0'); -- Scratch register to be written to walker_ro_next
  signal s_slave_walker_rw_offset_hi_o        : std_logic_vector(32-1 downto 0) := (others => '0'); -- Scratch register to be written to walker_ro_offset_hi
  signal s_slave_walker_rw_offset_lo_o        : std_logic_vector(32-1 downto 0) := (others => '0'); -- Scratch register to be written to walker_ro_offset_lo
  signal s_slave_walker_rw_tag_o              : std_logic_vector(32-1 downto 0) := (others => '0'); -- Scratch register to be written to walker_ro_tag
  signal s_slave_walker_rw_flags_o            : std_logic_vector(4-1 downto 0)  := (others => '0'); -- Scratch register to be written to walker_ro_flags
  signal s_slave_walker_rw_channel_o          : std_logic_vector(8-1 downto 0)  := (others => '0'); -- Scratch register to be written to walker_ro_channel
  signal s_slave_walker_rw_num_o              : std_logic_vector(8-1 downto 0)  := (others => '0'); -- Scratch register to be written to walker_ro_num
  signal s_slave_walker_write_o               : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Store the scratch registers to the inactive walker table record walker_select
  signal s_slave_walker_ro_next_V_i           : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - walker_ro_next
  signal s_slave_walker_ro_next_i             : std_logic_vector(16-1 downto 0) := (others => '0'); -- The next walker entry to execute after this record (0xffff = end of list)
  signal s_slave_walker_ro_offset_hi_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - walker_ro_offset_hi
  signal s_slave_walker_ro_offset_hi_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- The resulting action's deadline is the event timestamp plus this offset (high word)
  signal s_slave_walker_ro_offset_lo_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - walker_ro_offset_lo
  signal s_slave_walker_ro_offset_lo_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- The resulting action's deadline is the event timestamp plus this offset (low word)
  signal s_slave_walker_ro_tag_V_i            : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - walker_ro_tag
  signal s_slave_walker_ro_tag_i              : std_logic_vector(32-1 downto 0) := (others => '0'); -- The resulting actions's tag
  signal s_slave_walker_ro_flags_V_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - walker_ro_flags
  signal s_slave_walker_ro_flags_i            : std_logic_vector(4-1 downto 0)  := (others => '0'); -- Execute the resulting action even if it suffers from the errors set in this flag register
  signal s_slave_walker_ro_channel_V_i        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - walker_ro_channel
  signal s_slave_walker_ro_channel_i          : std_logic_vector(8-1 downto 0)  := (others => '0'); -- The channel to which the resulting action will be sent
  signal s_slave_walker_ro_num_V_i            : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - walker_ro_num
  signal s_slave_walker_ro_num_i              : std_logic_vector(8-1 downto 0)  := (others => '0'); -- The subchannel to which the resulting action will be sent
  signal s_slave_channel_select_WR_o          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - channel_select
  signal s_slave_channel_select_RD_o          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_select
  signal s_slave_channel_select_o             : std_logic_vector(8-1 downto 0)  := (others => '0'); -- Read/clear this channel
  signal s_slave_channel_num_select_o         : std_logic_vector(8-1 downto 0)  := (others => '0'); -- Read/clear this subchannel
  signal s_slave_channel_code_select_o        : std_logic_vector(2-1 downto 0)  := (others => '0'); -- Read/clear this error condition (0=late, 1=early, 2=conflict, 3=delayed)
  signal s_slave_channel_type_V_i             : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_type
  signal s_slave_channel_type_i               : std_logic_vector(32-1 downto 0) := (others => '0'); -- Type of the selected channel (0=io, 1=linux, 2=wbm, ...)
  signal s_slave_channel_max_num_V_i          : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_max_num
  signal s_slave_channel_max_num_i            : std_logic_vector(8-1 downto 0)  := (others => '0'); -- Total number of subchannels supported by the selected channel
  signal s_slave_channel_capacity_V_i         : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_capacity
  signal s_slave_channel_capacity_i           : std_logic_vector(16-1 downto 0) := (others => '0'); -- Total number of actions which may be enqueued by the selected channel at a time
  signal s_slave_channel_msi_set_enable_WR_o  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - channel_msi_set_enable
  signal s_slave_channel_msi_set_enable_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Turn on/off MSI messages for the selected channel
  signal s_slave_channel_msi_get_enable_V_i   : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_msi_get_enable
  signal s_slave_channel_msi_get_enable_i     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Check if MSI messages are enabled for the selected channel
  signal s_slave_channel_msi_set_target_WR_o  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - channel_msi_set_target
  signal s_slave_channel_msi_set_target_o     : std_logic_vector(32-1 downto 0) := (others => '0'); -- Set the destination MSI address for the selected channel (only possible while it has MSIs disabled)
  signal s_slave_channel_msi_get_target_V_i   : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_msi_get_target
  signal s_slave_channel_msi_get_target_i     : std_logic_vector(32-1 downto 0) := (others => '0'); -- Get the destination MSI address for the selected channel
  signal s_slave_channel_mostfull_ack_RD_o    : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_mostfull_ack
  signal s_slave_channel_mostfull_ack_V_i     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_mostfull_ack
  signal s_slave_channel_mostfull_ack_i       : std_logic_vector(32-1 downto 0) := (others => '0'); -- Read the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  signal s_slave_channel_mostfull_clear_RD_o  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_mostfull_clear
  signal s_slave_channel_mostfull_clear_V_i   : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_mostfull_clear
  signal s_slave_channel_mostfull_clear_i     : std_logic_vector(32-1 downto 0) := (others => '0'); -- Read and clear the selected channel's fill status (used_now<<16 | used_most), MSI=(6<<16) will be sent if used_most changes
  signal s_slave_channel_valid_count_RD_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_valid_count
  signal s_slave_channel_valid_count_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_valid_count
  signal s_slave_channel_valid_count_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- Read and clear the number of actions output by the selected subchannel, MSI=(4<<16|num) will be sent when the count becomes non-zero
  signal s_slave_channel_overflow_count_RD_o  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_overflow_count
  signal s_slave_channel_overflow_count_V_i   : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_overflow_count
  signal s_slave_channel_overflow_count_i     : std_logic_vector(32-1 downto 0) := (others => '0'); -- Read and clear the number of actions which could not be enqueued to the selected full channel which were destined for the selected subchannel, MSI=(5<<16|num) will be sent when the count becomes non-zero
  signal s_slave_channel_failed_count_RD_o    : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_failed_count
  signal s_slave_channel_failed_count_V_i     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_failed_count
  signal s_slave_channel_failed_count_i       : std_logic_vector(32-1 downto 0) := (others => '0'); -- Read and clear the number of actions with the selected error code which were destined for the selected subchannel, MSI=(code<<16|num) will be sent when the count becomes non-zero
  signal s_slave_channel_event_id_hi_RD_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_event_id_hi
  signal s_slave_channel_event_id_hi_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_event_id_hi
  signal s_slave_channel_event_id_hi_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  signal s_slave_channel_event_id_lo_RD_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_event_id_lo
  signal s_slave_channel_event_id_lo_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_event_id_lo
  signal s_slave_channel_event_id_lo_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- The event ID of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  signal s_slave_channel_param_hi_RD_o        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_param_hi
  signal s_slave_channel_param_hi_V_i         : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_param_hi
  signal s_slave_channel_param_hi_i           : std_logic_vector(32-1 downto 0) := (others => '0'); -- The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  signal s_slave_channel_param_lo_RD_o        : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_param_lo
  signal s_slave_channel_param_lo_V_i         : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_param_lo
  signal s_slave_channel_param_lo_i           : std_logic_vector(32-1 downto 0) := (others => '0'); -- The parameter of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  signal s_slave_channel_tag_RD_o             : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_tag
  signal s_slave_channel_tag_V_i              : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_tag
  signal s_slave_channel_tag_i                : std_logic_vector(32-1 downto 0) := (others => '0'); -- The tag of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  signal s_slave_channel_tef_RD_o             : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_tef
  signal s_slave_channel_tef_V_i              : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_tef
  signal s_slave_channel_tef_i                : std_logic_vector(32-1 downto 0) := (others => '0'); -- The TEF of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read
  signal s_slave_channel_deadline_hi_RD_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_deadline_hi
  signal s_slave_channel_deadline_hi_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_deadline_hi
  signal s_slave_channel_deadline_hi_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  signal s_slave_channel_deadline_lo_RD_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_deadline_lo
  signal s_slave_channel_deadline_lo_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_deadline_lo
  signal s_slave_channel_deadline_lo_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- The deadline of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  signal s_slave_channel_executed_hi_RD_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_executed_hi
  signal s_slave_channel_executed_hi_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_executed_hi
  signal s_slave_channel_executed_hi_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (high word)
  signal s_slave_channel_executed_lo_RD_o     : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Read enable flag - channel_executed_lo
  signal s_slave_channel_executed_lo_V_i      : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Valid flag - channel_executed_lo
  signal s_slave_channel_executed_lo_i        : std_logic_vector(32-1 downto 0) := (others => '0'); -- The actual execution time of the first action with the selected error code on the selected subchannel, cleared when channel_failed_count is read (low word)
  


begin

  INST_eca_auto : eca_auto
  port map (
    clk_sys_i                   => clk_sys_i,
    rst_sys_n_i                 => rst_sys_n_i,
    error_i                     => s_slave_error_i,
    stall_i                     => s_slave_stall_i,
    flip_active_o               => s_slave_flip_active_o,
    time_hi_V_i                 => s_slave_time_hi_V_i,
    time_hi_i                   => s_slave_time_hi_i,
    time_lo_V_i                 => s_slave_time_lo_V_i,
    time_lo_i                   => s_slave_time_lo_i,
    search_select_WR_o          => s_slave_search_select_WR_o,
    search_select_RD_o          => s_slave_search_select_RD_o,
    search_select_o             => s_slave_search_select_o,
    search_rw_first_o           => s_slave_search_rw_first_o,
    search_rw_event_hi_o        => s_slave_search_rw_event_hi_o,
    search_rw_event_lo_o        => s_slave_search_rw_event_lo_o,
    search_write_o              => s_slave_search_write_o,
    search_ro_first_V_i         => s_slave_search_ro_first_V_i,
    search_ro_first_i           => s_slave_search_ro_first_i,
    search_ro_event_hi_V_i      => s_slave_search_ro_event_hi_V_i,
    search_ro_event_hi_i        => s_slave_search_ro_event_hi_i,
    search_ro_event_lo_V_i      => s_slave_search_ro_event_lo_V_i,
    search_ro_event_lo_i        => s_slave_search_ro_event_lo_i,
    walker_select_WR_o          => s_slave_walker_select_WR_o,
    walker_select_RD_o          => s_slave_walker_select_RD_o,
    walker_select_o             => s_slave_walker_select_o,
    walker_rw_next_o            => s_slave_walker_rw_next_o,
    walker_rw_offset_hi_o       => s_slave_walker_rw_offset_hi_o,
    walker_rw_offset_lo_o       => s_slave_walker_rw_offset_lo_o,
    walker_rw_tag_o             => s_slave_walker_rw_tag_o,
    walker_rw_flags_o           => s_slave_walker_rw_flags_o,
    walker_rw_channel_o         => s_slave_walker_rw_channel_o,
    walker_rw_num_o             => s_slave_walker_rw_num_o,
    walker_write_o              => s_slave_walker_write_o,
    walker_ro_next_V_i          => s_slave_walker_ro_next_V_i,
    walker_ro_next_i            => s_slave_walker_ro_next_i,
    walker_ro_offset_hi_V_i     => s_slave_walker_ro_offset_hi_V_i,
    walker_ro_offset_hi_i       => s_slave_walker_ro_offset_hi_i,
    walker_ro_offset_lo_V_i     => s_slave_walker_ro_offset_lo_V_i,
    walker_ro_offset_lo_i       => s_slave_walker_ro_offset_lo_i,
    walker_ro_tag_V_i           => s_slave_walker_ro_tag_V_i,
    walker_ro_tag_i             => s_slave_walker_ro_tag_i,
    walker_ro_flags_V_i         => s_slave_walker_ro_flags_V_i,
    walker_ro_flags_i           => s_slave_walker_ro_flags_i,
    walker_ro_channel_V_i       => s_slave_walker_ro_channel_V_i,
    walker_ro_channel_i         => s_slave_walker_ro_channel_i,
    walker_ro_num_V_i           => s_slave_walker_ro_num_V_i,
    walker_ro_num_i             => s_slave_walker_ro_num_i,
    channel_select_WR_o         => s_slave_channel_select_WR_o,
    channel_select_RD_o         => s_slave_channel_select_RD_o,
    channel_select_o            => s_slave_channel_select_o,
    channel_num_select_o        => s_slave_channel_num_select_o,
    channel_code_select_o       => s_slave_channel_code_select_o,
    channel_type_V_i            => s_slave_channel_type_V_i,
    channel_type_i              => s_slave_channel_type_i,
    channel_max_num_V_i         => s_slave_channel_max_num_V_i,
    channel_max_num_i           => s_slave_channel_max_num_i,
    channel_capacity_V_i        => s_slave_channel_capacity_V_i,
    channel_capacity_i          => s_slave_channel_capacity_i,
    channel_msi_set_enable_WR_o => s_slave_channel_msi_set_enable_WR_o,
    channel_msi_set_enable_o    => s_slave_channel_msi_set_enable_o,
    channel_msi_get_enable_V_i  => s_slave_channel_msi_get_enable_V_i,
    channel_msi_get_enable_i    => s_slave_channel_msi_get_enable_i,
    channel_msi_set_target_WR_o => s_slave_channel_msi_set_target_WR_o,
    channel_msi_set_target_o    => s_slave_channel_msi_set_target_o,
    channel_msi_get_target_V_i  => s_slave_channel_msi_get_target_V_i,
    channel_msi_get_target_i    => s_slave_channel_msi_get_target_i,
    channel_mostfull_ack_RD_o   => s_slave_channel_mostfull_ack_RD_o,
    channel_mostfull_ack_V_i    => s_slave_channel_mostfull_ack_V_i,
    channel_mostfull_ack_i      => s_slave_channel_mostfull_ack_i,
    channel_mostfull_clear_RD_o => s_slave_channel_mostfull_clear_RD_o,
    channel_mostfull_clear_V_i  => s_slave_channel_mostfull_clear_V_i,
    channel_mostfull_clear_i    => s_slave_channel_mostfull_clear_i,
    channel_valid_count_RD_o    => s_slave_channel_valid_count_RD_o,
    channel_valid_count_V_i     => s_slave_channel_valid_count_V_i,
    channel_valid_count_i       => s_slave_channel_valid_count_i,
    channel_overflow_count_RD_o => s_slave_channel_overflow_count_RD_o,
    channel_overflow_count_V_i  => s_slave_channel_overflow_count_V_i,
    channel_overflow_count_i    => s_slave_channel_overflow_count_i,
    channel_failed_count_RD_o   => s_slave_channel_failed_count_RD_o,
    channel_failed_count_V_i    => s_slave_channel_failed_count_V_i,
    channel_failed_count_i      => s_slave_channel_failed_count_i,
    channel_event_id_hi_RD_o    => s_slave_channel_event_id_hi_RD_o,
    channel_event_id_hi_V_i     => s_slave_channel_event_id_hi_V_i,
    channel_event_id_hi_i       => s_slave_channel_event_id_hi_i,
    channel_event_id_lo_RD_o    => s_slave_channel_event_id_lo_RD_o,
    channel_event_id_lo_V_i     => s_slave_channel_event_id_lo_V_i,
    channel_event_id_lo_i       => s_slave_channel_event_id_lo_i,
    channel_param_hi_RD_o       => s_slave_channel_param_hi_RD_o,
    channel_param_hi_V_i        => s_slave_channel_param_hi_V_i,
    channel_param_hi_i          => s_slave_channel_param_hi_i,
    channel_param_lo_RD_o       => s_slave_channel_param_lo_RD_o,
    channel_param_lo_V_i        => s_slave_channel_param_lo_V_i,
    channel_param_lo_i          => s_slave_channel_param_lo_i,
    channel_tag_RD_o            => s_slave_channel_tag_RD_o,
    channel_tag_V_i             => s_slave_channel_tag_V_i,
    channel_tag_i               => s_slave_channel_tag_i,
    channel_tef_RD_o            => s_slave_channel_tef_RD_o,
    channel_tef_V_i             => s_slave_channel_tef_V_i,
    channel_tef_i               => s_slave_channel_tef_i,
    channel_deadline_hi_RD_o    => s_slave_channel_deadline_hi_RD_o,
    channel_deadline_hi_V_i     => s_slave_channel_deadline_hi_V_i,
    channel_deadline_hi_i       => s_slave_channel_deadline_hi_i,
    channel_deadline_lo_RD_o    => s_slave_channel_deadline_lo_RD_o,
    channel_deadline_lo_V_i     => s_slave_channel_deadline_lo_V_i,
    channel_deadline_lo_i       => s_slave_channel_deadline_lo_i,
    channel_executed_hi_RD_o    => s_slave_channel_executed_hi_RD_o,
    channel_executed_hi_V_i     => s_slave_channel_executed_hi_V_i,
    channel_executed_hi_i       => s_slave_channel_executed_hi_i,
    channel_executed_lo_RD_o    => s_slave_channel_executed_lo_RD_o,
    channel_executed_lo_V_i     => s_slave_channel_executed_lo_V_i,
    channel_executed_lo_i       => s_slave_channel_executed_lo_i,
    slave_i                     => slave_i,
    slave_o                     => slave_o  );
end rtl;
