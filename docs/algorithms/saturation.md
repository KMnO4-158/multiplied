# Saturation

A combinational multiplier starts by creating all possible partial products. Then, reduces the number of partial products across multiple stages, eventually all products are reduced to one output.

For example, using a [Wallice tree](https://en.wikipedia.org/wiki/Wallice_tree)  to multiplied 11 * 12: 

```
11 * 12 -> 0b1011 * 0b1100
```

Can be represented like so:
```
        1011
   [____0000] 0
   [___0000_] 0
   [__1011__] 1
   [_1011___] 1
   ----------
0b [10000100] -> 132
```

This is oversimplified and only 4-bit, but you get the idea.

Note that for any multiplication the output can be upto **2x** the input width.


##

Using the 11 * 12 example above, if the output was saturated to 4-bits, the result would be 15 since the maximum value is 0b1111 -> 15.
Typically, saturation restricts the output bit width to the input bit width. 




"""

    Here are scenarios I want to like to test:

    Type I
    a) Input values < 255
    b) Input pairs which do not cross overflow threshold during
       AND-matrix

       overflow|valid
       --------+-----------
        -------|00000000
        ------0|0000000-
        -----00|000000--
        ----000|00000---
        ---0000|0000----
        --00000|000-----
        -000000|00------
        0000000|0-------

    c) Input pairs which overflow in partial product reduction



    """
