---
file_format: mystnb
kernelspec:
  name: python3
---

# Data Structures

Each structure within Multiplied aims to provide fine grain control of the algorithm's
design. From automatic generation, to controlling how bits move between stages and
the ability to chose where arithmetic units are placed.

This page will cover the major data structures in Multiplied. For a brief introduction
to Multiplied check out the [quickstart guide](../quickstart.md).

## Matrix

Combinational multiplication generates [partial products](https://en.wikipedia.org/wiki/Binary_multiplier#Binary_long_multiplication)
which are reduced to a single product. The ``Matrix`` object contains the partial
product matrix(PPM) while also tracking which bits are important via it's formatting
style.


let's create 4-bit Matrix Object:

```{code-cell} ipython3
import multiplied as mp
matrix = mp.Matrix(4) # 4-bit partial product matrix
```

And here's what it looks like:

```{code-cell} ipython3
print(matrix)
```


```{note}
The width of the matrix is 2x the operand bit width. This is because
the maximum output of a product of two x-bit numbers results in a 2x-bit value.

15 * 15 = 225 -> 0b1111 * 0b1111 = 0b11100001
```

The ``Matrix`` structure gives Multiplied objects fine grain access to
bits and partial products while keeping data human readable.


### Wallace Tree

instead of generating a zeroed matrix, we can generate a matrix with a two
operands:


```{code-cell} ipython3
matrix = mp.Matrix(4, a=15, b=3)
print(matrix)
```

By default the matrix generates a [Wallace tree](https://en.wikipedia.org/wiki/Wallace_tree#Detailed_explanation).


### Dadda Tree


With an extra step it can be adjusted to resemble the start of a [Dadda tree](https://en.wikipedia.org/wiki/Dadda_multiplier#Algorithm_example).

```{code-cell} ipython3
matrix = mp.Matrix(4, a=15, b=3)

# maps bits to the top of the matrix
_ = mp.hoist(matrix)  # discard returned map
print(matrix)
```

````{important}
A method of generating a Dadda tree Matrix object is planned:
```{code}
matrix = mp.Matrix(4, a=15, b=3, dadda=True)
```
````

(struct-template)=

## Template

Templates defines the types of [arithmetic units](https://en.wikipedia.org/wiki/Arithmetic_logic_unit)
used and where they are placed within each algorithm stage.

The goal of a template is to "reduce" the number of partial products.

Multiplied allows two overarching methods to create templates:

### Pattern Based Templates

Patterns are arrays which define an arithmetic unit to be places across entire
rows of the Matrix:

```{code-cell} ipython3
# template based on two arithmetic units 
pattern = mp.Pattern(["a", "a", "a", "b", "b", "c", "c", "d"]) 
template = mp.Template(pattern)

print(pattern)
print(template)
```

### Arithmetic Units

As shown above each group or "run" of characters represents a single arithmetic
unit, each of which falls into **three** categories:

#### CSAs


Units spanning three rows define a [CSA](https://en.wikipedia.org/wiki/Carry-save_adder)
Each taking in 3 inputs  and returning a sum and a carry.


```{code} text
[ Template     ]  [ Pattern ]  [ Result       ]
________aAaAaAaA       a       ______aAaAaAaAaA
_______AaAaAaAa_       a       ______AaAaAaAa__
______aAaAaAaA__       a       ________________
```

```{note}
The utility of a CSA is the size and speed of it's circuit. Instead of wasting space
using large full adders, many smaller CSAs will produce the same reduction, faster.
```


#### Adders

Units spanning two rows define an [adder](https://en.wikipedia.org/wiki/Adder_(electronics)),
each taking in two values and returning the combined sum.

```{code} text
[ Template     ]  [ Pattern ] [ Result       ]
_____BbBbBbBb___       b      ___bbBbBbBbBb___
____bBbBbBbB____       b      ________________
```

```{code} text
___CcCcCcCc_____       c      _ccCcCcCcCc_____
__cCcCcCcC______       c      ________________
```



#### NOOPs

Units spanning a single row are considered as NOOP or no operation.

```{code} text
[ Template     ]  [ Pattern ]  [ Result       ]
_dDdDdDdD_______       d       _dDdDdDdD_______
```

```{note}
Decoders are also planned, potentially reducing inputs by more than 1.

By encoding specialised operations based on bit position, count, unary count,
etc. a decoder can also offer unique operations.
```

### Complex Templates

Pattern based templates can be used as a starting point for more complex templates:

```{code-cell} ipython3

raw_template = template.template
raw_result = template.result

for t in raw_template:
    print(t)

print("----")

for r in raw_result:
    print(r)
```

Using the print out to build a new template and result:

```{code-cell} ipython3
complex_template = [
    ["_", "_", "_", "_", "_", "_", "_", "_", "a", "A", "a", "A", "a", "x", "x", "x"],
    ["_", "_", "_", "_", "_", "_", "_", "A", "a", "A", "a", "A", "a", "y", "y", "_"],
    ["_", "_", "_", "_", "_", "_", "a", "A", "a", "A", "a", "A", "a", "z", "_", "_"],
    ["_", "_", "_", "_", "_", "B", "b", "B", "b", "B", "b", "B", "b", "_", "_", "_"],
    ["_", "_", "_", "_", "b", "B", "b", "B", "b", "B", "b", "B", "_", "_", "_", "_"],
    ["_", "_", "_", "C", "c", "C", "c", "C", "c", "C", "c", "_", "_", "_", "_", "_"],
    ["_", "_", "c", "C", "c", "C", "c", "C", "c", "C", "_", "_", "_", "_", "_", "_"],
    ["_", "d", "D", "d", "D", "d", "D", "d", "D", "_", "_", "_", "_", "_", "_", "_"],
]
complex_result = [
    ["_", "_", "_", "_", "_", "_", "a", "A", "a", "A", "a", "A", "a", "x", "x", "x"],
    ["_", "_", "_", "_", "_", "_", "A", "a", "A", "a", "A", "a", "_", "y", "y", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "z", "_", "_"],
    ["_", "_", "_", "b", "b", "B", "b", "B", "b", "B", "b", "B", "b", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "c", "c", "C", "c", "C", "c", "C", "c", "C", "c", "_", "_", "_", "_", "_"],
    ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
    ["_", "d", "D", "d", "D", "d", "D", "d", "D", "_", "_", "_", "_", "_", "_", "_"],
]


new_template = mp.Template(complex_template, result=complex_result)
print(new_template)

```

```{warning}
Currently a resultant template must be supplied when creating a template without
using a pattern. 

Auto-resolution of resultant templates is planned.
```


## Map

Each step of an algorithm needs a pattern or a template, but it also needs to regroup
their partial products before using the next template. This is where maps come in.

First, note that bits can only move vertically as moving horizontally changes it's
value. Therefore, each map value is a signed hexadecimal number.

For simple maps, the map value represents an entire row rather than a specific bit.

```{code} text

# Maps for each stage of first_alg

1st:    2nd:    3rd:

00      00      00
00      00      00
00      FF      00
FF      00      00
```


```{note}

  Outputs of each units are packed to the top of their initial row.
```

Here's the breakdown of this example:

1st stage - Move first 2 rows of result down by 1 [-1 = FF = down * 1]

2nd stage - Move middle 2 rows of result down by 1 [-1 = FF = down * 1]

3rd stage - No moves required


Algorithms use a template to produce a result, which is then "mapped" to the next
template. Each Adder/CSA/etc. needs to know where it should output in relation to
the next template.
This means as long as outputs are mapped correctly to inputs, the placements of
arithmetic units can be anywhere. The final output (x from the pattern example)
can be anywhere within the matrix.

````{note}
In other words, these are also valid algorithms:

```{code} text

# [ Key ]
# char | r :: arithmetic unit | result

# Another valid algorithm               # Another

1st:    2nd:    3rd:    output:         1st:    2nd:    3rd:    output:

a r                                     a r     c r
a r     c r                             a r     c r     d r     x
a       c r     d r                     a       c       d
b r     c       d       x               b r

# maps                                  # maps


01      00      00                      00      01      00
01      01      00                      00      01      00
00      01      01                      00      00      00
00      00      00                      FF      00      00
```
````

## Algorithm

The Algorithm object bundle templates and maps to define a multiplication algorithm.
A given stage contains:

```{code} python
"template" : mp.Template  # source and resultant templates
"pseudo"   : mp.Matrix  # resultant matrix after reduction + map 
"map"      : mp.Map  # modifies bit positions
```

This guide will use pattern based templates to demonstrate the structure of an Algorithm,
for a more comprehensive overview check out the [complex algorithm guide](/guide/complex.md).

### Population


completely automatic generation...

```{code-cell} ipython3
auto_alg = mp.Algorithm(4)
auto_alg.auto_resolve_stage(recursive=True)
print(auto_alg)
```

Push templates or patterns one at a time:

```{code-cell} ipython
alg = mp.Algorithm(4)
alg.push(mp.Pattern(["a", "a", "b", "b"]))
print(alg)
```

```{note}
Pushing a pattern will automatically generate a new stage based on the prior stage.
```

Automatically generate the rest:

```{code-cell} ipython
alg.auto_resolve_stage(recursive=True)
print(alg)
```

### Execution


Use ``exec()`` to run the algorithm using two operands:

```{code-cell} ipython3
a = 15
b = 15
output = alg.exec(a, b)

for m in output.values():
    print(m)

# convert result to decimal
print(int("".join(alg.matrix.matrix[0]), 2))
print(a * b)
```

Manually provide starting matrix and step through an algorithm:

```{code-cell} ipython
starting_ppm = mp.Matrix(4, a=5, b=9)
alg.reset(starting_ppm)
print(alg.matrix)  # initial state
print(alg.step())
print(alg.step())
```

### Saturation

Some workloads require operations clamped to the source bit width such as
[digital signal processing](https://en.wikipedia.org/wiki/Digital_signal_processing)(DSP)
and working with [RGB](https://en.wikipedia.org/wiki/RGB_color_model) pixel values.
This clamping is called [saturation](https://en.wikipedia.org/wiki/Saturation_arithmetic).


```{code} text
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

```{code-cell} ipython3
alg.saturation = True


for m in alg.exec(11, 12).values():
    print(m)
```
