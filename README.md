# Bonds

### Problem Statement
Got 4 bonds in JSON file "bonds.json". Each bonds has 6 fields: 
	ID
	Value – Face Value (Par Value or Value at Maturity)
	Coupon(%) – amount of periodic payment (C = Value * Coupon(%)) *stated in yearly basis
	Yield(%) – interest rate set by the market (assume it is flat across the lifetime)
	Duration – the number of years in security lifetime
	Type – type of periodic payments (A – Annual 1 payment per year | S – Semi-Annual 2 payments a year | Q – Quarterly 4 payments per year | M – Monthly 12 payments)
	
Bond Price Formula: A=[∑_(period i)^(# of Periods)▒C/(1+yield)^(period i)   ]+  Value/〖(1+yield)〗^(period N) 

##### Problem 1: 
Using Bond Price Formula and inputs from the file, create a periodic table for that will contain the information for every bond.

##### Problem 2:
Based on the table you created above, aggregate PV of periodic payments and find Bond Price.


### Program Output
###### Input Table

	+---+------+-------+-------+----+--------+
	| id| value| coupon|  yield|type|duration|
	+---+------+-------+-------+----+--------+
	|xr2| 10000|0.02000|0.03000|   S|       5|
	|ar5| 50000|0.02790|0.02500|   A|       7|
	|lr3|250000|0.06000|0.06500|   Q|      30|
	|kn7| 25000|0.04000|0.04000|   M|       5|
	+---+------+-------+-------+----+--------+
###### Periodic Table

	+-------+------+--------------+-----------------------+------------+
	|Bond ID|Period|Coupon payment|PV of periodic payments|           A|
	+-------+------+--------------+-----------------------+------------+
	|    xr2|     1|   10000.00000|             4000.00000|     0.00000|
	|    xr2|     2|   10000.00000|             1600.00000|     0.00000|
	|    xr2|     3|   10000.00000|              640.00000|     0.00000|
	|    xr2|     4|   10000.00000|              256.00000|     0.00000|
	|    xr2|     5|   10000.00000|              204.80000|  6700.80000|
	|    ar5|     1|  139500.00000|            39857.14286|     0.00000|
	|    ar5|     2|  139500.00000|            11387.75510|     0.00000|
	|    ar5|     3|  139500.00000|             3253.64431|     0.00000|
	|    ar5|     4|  139500.00000|              929.61266|     0.00000|
	|    ar5|     5|  139500.00000|              265.60362|     0.00000|
	|    ar5|     6|  139500.00000|               75.88675|     0.00000|
	|    ar5|     7|  139500.00000|               29.45323| 55799.09853|
	|    lr3|     1|  375000.00000|           142857.14286|     0.00000|
	|    lr3|     2|  375000.00000|            54421.76871|     0.00000|
	|    lr3|     3|  375000.00000|            20732.10236|     0.00000|
	|    lr3|     4|  375000.00000|             7897.94376|     0.00000|
	|    lr3|     5|  375000.00000|             3008.74048|     0.00000|
	|    lr3|     6|  375000.00000|             1146.18685|     0.00000|
	|    lr3|     7|  375000.00000|              436.64261|     0.00000|
	|    lr3|     8|  375000.00000|              166.34004|     0.00000|
	|    lr3|     9|  375000.00000|               63.36763|     0.00000|
	|    lr3|    10|  375000.00000|               24.14005|     0.00000|
	|    lr3|    11|  375000.00000|                9.19621|     0.00000|
	|    lr3|    12|  375000.00000|                3.50332|     0.00000|
	|    lr3|    13|  375000.00000|                1.33460|     0.00000|
	|    lr3|    14|  375000.00000|                0.50842|     0.00000|
	|    lr3|    15|  375000.00000|                0.19368|     0.00000|
	|    lr3|    16|  375000.00000|                0.07378|     0.00000|
	|    lr3|    17|  375000.00000|                0.02811|     0.00000|
	|    lr3|    18|  375000.00000|                0.01071|     0.00000|
	|    lr3|    19|  375000.00000|                0.00408|     0.00000|
	|    lr3|    20|  375000.00000|                0.00155|     0.00000|
	|    lr3|    21|  375000.00000|                0.00059|     0.00000|
	|    lr3|    22|  375000.00000|                0.00023|     0.00000|
	|    lr3|    23|  375000.00000|                0.00009|     0.00000|
	|    lr3|    24|  375000.00000|                0.00003|     0.00000|
	|    lr3|    25|  375000.00000|                0.00001|     0.00000|
	|    lr3|    26|  375000.00000|                0.00000|     0.00000|
	|    lr3|    27|  375000.00000|                0.00000|     0.00000|
	|    lr3|    28|  375000.00000|                0.00000|     0.00000|
	|    lr3|    29|  375000.00000|                0.00000|     0.00000|
	|    lr3|    30|  375000.00000|                0.00000|230769.23077|
	|    kn7|     1|    8333.33333|             6250.00000|     0.00000|
	|    kn7|     2|    8333.33333|             4687.50000|     0.00000|
	|    kn7|     3|    8333.33333|             3515.62500|     0.00000|
	|    kn7|     4|    8333.33333|             2636.71875|     0.00000|
	|    kn7|     5|    8333.33333|             7910.15625| 25000.00000|
	+-------+------+--------------+-----------------------+------------+
###### Bond Price Table

	+-------+------------+------+-------+
	|Bond ID|           A|    FV|  Quote|
	+-------+------------+------+-------+
	|    xr2|  6700.80000| 10000|0.67008|
	|    ar5| 55799.09853| 50000|1.11598|
	|    lr3|230769.23077|250000|0.92308|
	|    kn7| 25000.00000| 25000|1.00000|
	+-------+------------+------+-------+

