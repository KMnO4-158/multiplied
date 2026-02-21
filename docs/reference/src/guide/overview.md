# Overview

This project was initially focused on how [saturation](https://en.wikipedia.org/wiki/Saturation_arithmetic)
allows for the optimisation of a combinational [multiplier](https://en.wikipedia.org/wiki/Binary_multiplier).

Generating and analysing designs by hand is labour intensive even for small datasets.
For entire [truth tables](https://en.wikipedia.org/wiki/Truth_table), this becomes
close to impossible after 8-bits.

## Algorithms

The first "stage" of s combinational multiplier creates all possible partial products.
These products are then reduced across multiple stages using a range of methods.
Eventually all products are reduced to one output.

A [Wallace tree](https://en.wikipedia.org/wiki/Wallace_tree) is one of many
multiplication strategies. Let's multiply 11 * 12:

```text
11 * 12 -> 0b1011 * 0b1100
```

Can be represented like so:

```text
   [ S0:AND ]  ->  [ S1:ADD ]  ->  [ S2:ADD ]
        1011      
   [____0000] 0       
   [___0000_] 0    [__000000] 
   [__1011__] 1   
   [_1011___] 1    [100001__]      [10000100]
   ----------         
0b [10000100] -> 132
```

This is only 4-bits, but you get the idea. First partial products "fan out" and
then reduced in subsequent layers.

Note that for any multiplication the output can be up to **2x** the input width.


### Saturation

Using the 11 * 12 example above, if the output was saturated to 4-bits, the result
would be 15 since the maximum value is 0b1111 -> 15.
Typically, saturation restricts the output bit width to the input bit width:
x-bits --> 2x-bits -(clamp)-> x-bits. Multiplications which produce an [overflow](https://en.wikipedia.org/wiki/Integer_overflow)
trigger a signal to flood the output bits to 1, resulting in the maximum value of
the bit width.

As demonstrated in the example above:

```text
11 * 12 -> 0b1011 * 0b1100 -> 0b10000100 -[Clamp=4b]-> 0b1111

    Cout|1011
   -----+-----   
   [____|0000] 0
   [___0|000_] 0
   [__10|11__] 1
   [_101|1___] 1
   -----+-----
IF !0 ->|1111  -> 15

```

Most of the complex templates will be directed to find optimisation strategies to
make te most of saturation. Many overflow edge cases can be found very early in
the reduction process, take the AND matrix stage, while some are harder to isolate
and arise deeper in the combinational logic.

## Templates

Describing how each stages reduces partial products.

### Simple Templates -- Patterns

Patterns should be represented as a list with each element on
a new line, this makes it clear how each layer is reduced:
(Becomes tedious for 16-bit+, that said, complex templates will be 100x worse
dependng on the coplexity)

```py
>>> my_pattern = [
    1,
    1,
    2,
    2,
    2,
    .
    .
    .
]
```

The "run" of a given element determines where adders, run=2, or a
combination of CSAs and HAs, run=3, are used. Elements can be
int or strings, as long as they follow the "run" principle.

E.g:
my_pattern's first run is equal to 2, it's second is 3.

Complex templates require a more rigorous approach.



## Complex Templates


Simple templates used a vector, internally these are translated to a hard coded
complex template. Complex templates are matrices outlining what operations occur
and where they occur. They also have a range of tools inaccessible to simple templates,
such as user defined positions for CSAs, Adders, Decoders and Bit-Mapping.






## Analysis

Json is availiable for small truthtables and quickly visualising designs
Parquet is recommended for large truth tables and intensive analysis

### Further Reading

multiplied:
[Structures](https://github.com/EphraimCompEng/multiplied/tree/master/docs/structures)
[Algorithms](https://github.com/EphraimCompEng/multiplied/tree/master/docs/algorithms)
[Analysis](https://github.com/EphraimCompEng/multiplied/tree/master/docs/analysis)

Multiplication:

Useful video: Sanjay Vidhyadharan, "[Advanced VLSI Design: Arithmetic Circuits:
Part-2](https://youtu.be/yZbLL1q76X8)"
