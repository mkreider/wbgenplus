--! @file        oled.xml
--  DesignUnit   oled
--! @author      M. Kreider <m.kreider@gsi.de>
--! @date        14/11/2023
--! @version     0.2.0
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
use work.oled_auto_pkg.all;

entity oled is
Port(
  clk_sys_i   : std_logic;                            -- Clock input for sys domain
  rst_sys_n_i : std_logic;                            -- Reset input (active low) for sys domain
  error_i     : in  std_logic_vector(1-1 downto 0);   -- Error control
  stall_i     : in  std_logic_vector(1-1 downto 0);   -- flow control
  char_o      : out std_logic_vector(20-1 downto 0);  -- Char input FIFO. Row b14..12, Col b11..8, Ascii b7..0
  char_WR_o   : out std_logic_vector(1-1 downto 0);   -- Write enable flag - char
  col_offs_o  : out std_logic_vector(8-1 downto 0);   -- first visible pixel column. 0x23 for old, 0x30 for new controllers. default is 0x30
  raw_o       : out std_logic_vector(20-1 downto 0);  -- Raw  input FIFO. Disp RAM Adr b18..8, Pixel (Col) b7..0
  raw_WR_o    : out std_logic_vector(1-1 downto 0);   -- Write enable flag - raw
  reset_o     : out std_logic_vector(1-1 downto 0);   -- Resets the OLED display
  uart_o      : out std_logic_vector(8-1 downto 0);   -- UART input FIFO. Ascii b7..0
  uart_WR_o   : out std_logic_vector(1-1 downto 0);   -- Write enable flag - uart
  
  slave_i     : in  t_wishbone_slave_in;
  slave_o     : out t_wishbone_slave_out

  
);
end oled;

architecture rtl of oled is

  signal s_slave_error_i    : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Error control
  signal s_slave_stall_i    : std_logic_vector(1-1 downto 0)  := (others => '0'); -- flow control
  signal s_slave_reset_o    : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Resets the OLED display
  signal s_slave_col_offs_o : std_logic_vector(8-1 downto 0)  := (others => '0'); -- first visible pixel column. 0x23 for old, 0x30 for new controllers. default is 0x30
  signal s_slave_uart_WR_o  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - uart
  signal s_slave_uart_o     : std_logic_vector(8-1 downto 0)  := (others => '0'); -- UART input FIFO. Ascii b7..0
  signal s_slave_char_WR_o  : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - char
  signal s_slave_char_o     : std_logic_vector(20-1 downto 0) := (others => '0'); -- Char input FIFO. Row b14..12, Col b11..8, Ascii b7..0
  signal s_slave_raw_WR_o   : std_logic_vector(1-1 downto 0)  := (others => '0'); -- Write enable flag - raw
  signal s_slave_raw_o      : std_logic_vector(20-1 downto 0) := (others => '0'); -- Raw  input FIFO. Disp RAM Adr b18..8, Pixel (Col) b7..0
  


begin

  INST_oled_auto : oled_auto
  port map (
    clk_sys_i   => clk_sys_i,
    rst_sys_n_i => rst_sys_n_i,
    error_i     => s_slave_error_i,
    stall_i     => s_slave_stall_i,
    reset_o     => s_slave_reset_o,
    col_offs_o  => s_slave_col_offs_o,
    uart_WR_o   => s_slave_uart_WR_o,
    uart_o      => s_slave_uart_o,
    char_WR_o   => s_slave_char_WR_o,
    char_o      => s_slave_char_o,
    raw_WR_o    => s_slave_raw_WR_o,
    raw_o       => s_slave_raw_o,
    slave_i     => slave_i,
    slave_o     => slave_o  );
end rtl;
