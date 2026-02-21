---
file_format: mystnb
kernelspec:
  name: python3
---

# **Quickstart**

Multiplied is a library for exploring and quickly defining [combinational](https://en.wikipedia.org/wiki/Combinational_logic)
multiplication algorithms. The library also bundles built-in tools to analyse and
visualise algorithms through [Pandas](https://pandas.pydata.org/) and [Matplotlib](https://matplotlib.org/).

This guide will quickly walk through each area of Multiplied, without delving too
deeply into the details.


## **Algorithms**

A given combinational multiplier is defined by a sequence of "stages" which continuously
reduce an initial set of [partial products](https://en.wikipedia.org/wiki/Binary_multiplier#Binary_long_multiplication)
into a single output product.

First import the module and define the bitwidth of the algorithm:

```{code-cell}
import multiplied as mp

alg = mp.Algorithm(4)
```

Then automatically generate a basic algorithm.

```{code-cell}

alg.auto_resolve_stage(recursive=True)  # recursive=True -- default
print(alg)
```

As the output shows, each stage is made up of a [Template](guide/structures.html#Template),
pseudo [Matrix](guide/structures.html#Matrix), and a [Map](guide/structures.html#Map).

**Templates**:

- Represent arithmetic units via characters
- Resultant templates show where bits will be placed after a given stage

**Pseudo Matrix**:

- Shows the partial product matrix after reduction and maps have been applied
- Each matrix has a width two times it's height:
  - two values of x-bits can multiply to produce a 2x-bit value

**Maps**:

- 2-bit hexadecimal values define how far each bit is vertically shifted after reduction
- Positive values shift bits up
- negative values shift bits down

## Execution

The algorithm can now execute using input operands to verify it works:

```{code-cell}
a = 15
b = 13
output = alg.exec(a, b)

for m in output.values():
    print(m)

# convert result to decimal
print(int("".join(alg.matrix.matrix[0]), 2))
print(a * b)
```

Stage 0 represents the initial starting partial product matrix with each following
stage being reduced by [Adders](https://en.wikipedia.org/wiki/Adder_(electronics))
("units" which cover 2 rows) and [Carry Save Adders](https://en.wikipedia.org/wiki/Carry-save_adder)
("units" which cover 3 rows).

## **Generating Data**

Now a truth table can be generated and stored to a Pandas [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html#pandas.DataFrame):

```{code-cell}
import pandas as pd

domain_ = (1, 15)  # range of possible operand values for a and b
range_ = (1, 255)  # range of possible output values
scope = mp.truth_scope(domain_, range_)  # generator clamps range to domain

# scope yields input tuples (a, b) to generate a Pandas DataFrame
df = mp.truth_dataframe(scope, alg)

```

## **DataFrame Layout**

Multiplied makes use of Pandas DataFrames to store generated truth tables.
A generated truth table  can be defined by three regions:

### Operands

These columns hold the input and output operands for a given  

```{code-cell} ipython3
:tags: [remove-input]

cols = df.columns[:3]          
print(df[cols].tail())

```

### **Formatted Output**

Stores outputs produced by a given execution of the algorithm as seen above

```{code-cell} ipython3
:tags: [remove-input]

pd.set_option('display.max_columns',None)
pd.set_option("display.width", 1000)
cols = df.columns[-3]          
print(df[cols].to_frame().tail())
```


:::{note}
test
:::



### **Raw Output**

```{code-cell} ipython3
:tags: [remove-input]

cols = df.columns[35:43]          
print(df[cols].tail())
```

#### \[s\]tage

> Number of reductions needed to return a single product

#### \[p\]artial product

> A given row in a partial product matrix


#### \[b\]it

> Bit index within a partial product


## **Visualisation**

Finally, the generated data is ready to be visualised. Let's keep it simple and
generate a 2D heatmap:

```{code-cell}

mp.df_global_heatmap("example.png", "Fancy Title", df)

```

And a 3D heatmap, isolating each stage of the algorithm:

```{code-cell}

mp.df_global_3d_heatmap("example3d.png", "Fancy Title", df)

```
