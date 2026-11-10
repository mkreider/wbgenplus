--! @file        reset_comment.xml
--  DesignUnit   reset_comment
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
use work.reset_comment_auto_pkg.all;

entity reset_comment is
generic(
  g_lanes : natural := 4  --lanes, 25% each
);
Port(
  clk_sys_i   : std_logic;                                -- Clock input for sys domain
  rst_sys_n_i : std_logic;                                -- Reset input (active low) for sys domain
  error_i     : in  std_logic_vector(1-1 downto 0);       -- Error control
  pct_i       : in  std_logic_vector(4-1 downto 0);       -- load 50%, %s %d %% stay literal
  pct_V_i     : in  std_logic_vector(1-1 downto 0);       -- Valid flag - pct
  stall_i     : in  std_logic_vector(1-1 downto 0);       -- flow control
  all_ones_o  : out std_logic_vector(8-1 downto 0);       -- reset to ones, 100% sure
  all_zero_o  : out std_logic_vector(8-1 downto 0);       -- reset to zeroes
  hex_rst_o   : out std_logic_vector(16-1 downto 0);      -- hex reset
  pct_RD_o    : out std_logic_vector(1-1 downto 0);       -- Read enable flag - pct
  pct_w_o     : out std_logic_vector(g_lanes-1 downto 0); -- atomic 10% pulse
  
  ctrl_i      : in  t_wishbone_slave_in;
  ctrl_o      : out t_wishbone_slave_out

  
);
end reset_comment;

architecture rtl of reset_comment is

  signal s_ctrl_error_i     : std_logic_vector(1-1 downto 0)        := (others => '0'); -- Error control
  signal s_ctrl_stall_i     : std_logic_vector(1-1 downto 0)        := (others => '0'); -- flow control
  signal s_ctrl_all_ones_o  : std_logic_vector(8-1 downto 0)        := (others => '0'); -- reset to ones, 100% sure
  signal s_ctrl_all_zero_o  : std_logic_vector(8-1 downto 0)        := (others => '0'); -- reset to zeroes
  signal s_ctrl_hex_rst_o   : std_logic_vector(16-1 downto 0)       := (others => '0'); -- hex reset
  signal s_ctrl_pct_RD_o    : std_logic_vector(1-1 downto 0)        := (others => '0'); -- Read enable flag - pct
  signal s_ctrl_pct_V_i     : std_logic_vector(1-1 downto 0)        := (others => '0'); -- Valid flag - pct
  signal s_ctrl_pct_i       : std_logic_vector(4-1 downto 0)        := (others => '0'); -- load 50%, %s %d %% stay literal
  signal s_ctrl_pct_w_o     : std_logic_vector(g_lanes-1 downto 0)  := (others => '0'); -- atomic 10% pulse
  


begin

  INST_reset_comment_auto : reset_comment_auto
  port map (
    clk_sys_i   => clk_sys_i,
    rst_sys_n_i => rst_sys_n_i,
    error_i     => s_ctrl_error_i,
    stall_i     => s_ctrl_stall_i,
    all_ones_o  => s_ctrl_all_ones_o,
    all_zero_o  => s_ctrl_all_zero_o,
    hex_rst_o   => s_ctrl_hex_rst_o,
    pct_RD_o    => s_ctrl_pct_RD_o,
    pct_V_i     => s_ctrl_pct_V_i,
    pct_i       => s_ctrl_pct_i,
    pct_w_o     => s_ctrl_pct_w_o,
    ctrl_i      => ctrl_i,
    ctrl_o      => ctrl_o  );
end rtl;
