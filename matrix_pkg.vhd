type t_slm is array(natural range <>, natural range <>) of std_logic;

  -- assign row slice

  procedure slv2mrowslice(signal slm : out t_slm; slv : std_logic_vector; constant rowindex : natural; high : natural; low : natural);

  -- get std logic vector from matrix row slice

  function mrowslice2slv(slm : t_slm; rowindex : natural; high : natural; low : natural) return std_logic_vector;

  -- get std logic vector from matrix row

  function mrow2slv(slm : t_slm; rowindex : natural) return std_logic_vector;

  -- flatten matrix to std logic vector

  function m2slv(slm : t_slm) return std_logic_vector;

  -- construct matrix from std logic vector

  function slv2m(slv : std_logic_vector; slm : t_slm) return t_slm;

  --  construct m x n matrix from std logic vector

  function slv2m(slv : std_logic_vector; col_len : natural; row_len : natural) return t_slm;

  
  

  -- assign row slice

  procedure slv2mrowslice(signal slm : out t_slm; slv : std_logic_vector; constant rowindex : natural; high : natural; low : natural) is

    variable temp : std_logic_vector(high downto low);

  begin

    temp := slv(temp'range);

    for i in temp'range loop

            slm(rowindex, i)  <= temp(i);

    end loop;

  end procedure;

  

  -- get std logic vector from matrix row slice

  function mrs2slv(slm : t_slm; rowindex : natural; high : natural; low : natural) return std_logic_vector is

    variable slv : std_logic_vector(high downto low);

  begin

    for i in slv'range loop

            slv(i)  := slm(rowindex, i);

    end loop;

    return slv;

  end function;

  

  -- get std logic vector from matrix row

  function mrow2slv(slm : t_slm; rowindex : natural) return std_logic_vector is

    variable slv : std_logic_vector(slm'high(2) downto slm'low(2));

  begin

    for i in slv'range loop

            slv(i)  := slm(rowindex, i);

    end loop;

    return slv;

  end function;

  

  -- flatten matrix to std logic vector

  function m2slv(slm : t_slm) return std_logic_vector is

    constant row_len : natural := slm'length(2);

    constant col_len : natural := slm'length(1);

    variable slv : std_logic_vector(col_len*row_len-1 downto 0);  

  begin

    for row in 0 to col_len-1 loop

       for col in 0 to row_len-1 loop

            slv(row*row_len+col)  := slm(row, col);

       end loop;

    end loop;

    return slv;

  end function;



  -- std logic vector to matrix

  function slv2m(slv : std_logic_vector; slm : t_slm) return t_slm is

    constant row_len : natural := slm'length(2);

    constant col_len : natural := slm'length(1);

    variable res : t_slm(col_len-1 downto 0, row_len-1 downto 0);

  begin

    for row in 0 to col_len-1 loop

       for col in 0 to row_len-1 loop

            res(row, col)  := slv(slv'length-1 - (row*row_len+col));

       end loop;

    end loop;

    return res;

  end function;

  

  -- std logic vector to m x n matrix

  function slv2m(slv : std_logic_vector; col_len : natural; row_len : natural) return t_slm is

    variable res : t_slm(col_len-1 downto 0, row_len-1 downto 0);

  begin

    for row in 0 to col_len-1 loop
       for col in 0 to row_len-1 loop

            res(row, col)  := slv(slv'length-1 - (row*row_len+col));

       end loop;

    end loop;

    return res;

  end function;
