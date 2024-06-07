  6           0 LOAD_CONST               1 (65535)
              2 STORE_FAST               2 (a)

  7           4 LOAD_CONST               2 (489)
              6 STORE_FAST               3 (b)

 10           8 LOAD_FAST                2 (a)
             10 LOAD_FAST                3 (b)
             12 COMPARE_OP               3 (!=)
             14 POP_JUMP_IF_FALSE       25 (to 50)

 11     >>   16 LOAD_FAST                2 (a)
             18 LOAD_FAST                3 (b)
             20 COMPARE_OP               4 (>)
             22 POP_JUMP_IF_FALSE       17 (to 34)

 12          24 LOAD_FAST                2 (a)
             26 LOAD_FAST                3 (b)
             28 INPLACE_SUBTRACT
             30 STORE_FAST               2 (a)
             32 JUMP_FORWARD             4 (to 42)

 14     >>   34 LOAD_FAST                3 (b)
             36 LOAD_FAST                2 (a)
             38 INPLACE_SUBTRACT
             40 STORE_FAST               3 (b)

 10     >>   42 LOAD_FAST                2 (a)
             44 LOAD_FAST                3 (b)
             46 COMPARE_OP               3 (!=)
             48 POP_JUMP_IF_TRUE         8 (to 16)

 16     >>   50 LOAD_FAST                2 (a)
             52 LOAD_FAST                0 (guess)
             54 COMPARE_OP               2 (==)
             56 POP_JUMP_IF_FALSE       35 (to 70)
             58 LOAD_FAST                1 (birth_year_minus_the_guess)
             60 LOAD_CONST               3 (1593)
             62 COMPARE_OP               2 (==)
             64 POP_JUMP_IF_FALSE       35 (to 70)

 17          66 LOAD_CONST               4 (True)
             68 RETURN_VALUE

 19     >>   70 LOAD_GLOBAL              0 (print)
             72 LOAD_CONST               5 ('Error calculating GCD of a = 65535 and b = (2**16 >> 7) - 0x17.')
             74 CALL_FUNCTION            1
             76 POP_TOP

 20          78 LOAD_CONST               6 (False)
             80 RETURN_VALUE
