# Data Structures


## Matrix

First, import multiplied and decide on a bitwidth for our algorithm, to keep it simple let's pick 4-bits:

.. code-block:: python

    import multiplied as mp
    matrix = mp.Matrix(4) # 4-bit logical AND matrix


Here's what it looks like:

.. code-block:: python

    print(matrix)


.. code-block:: python

    ____0000
    ___0000_
    __0000__
    _0000___



The ``matrix`` is a "structure" used to generate the logical AND matrix, aka partial
products, for a given set of inputs. It also tells the algorithm *where* each partial
product is located.

.. note::
    To populate an AND matrix without an Algorithm object use:

    .. code-block:: python

        matrix = mp.build_matrix(operand_a=0, operand_b=0, bits=4)





Next, create an algorithm object.

.. code-block:: python

    first_alg = mp.Algorithm(matrix)


The Algorithm object will hold the templates that define a given algorithm. It also holds an internal state to track which template it should use next.


## Template


## Map

Each step of an algorithm needs a pattern or a template, but it also needs to regoup
their partial products before using the next template. This is where maps come in.

First, note that bits can only move vertically as moving horizontally changes it's
value. Therefore, each map value is a signed hexadecimal number.

For simple maps, the map value represents an entire row rather than a specific bit.

.. code:: text

    # Maps for each stage of first_alg

    1st:    2nd:    3rd:

    00      00      00
    00      00      00
    00      FF      00
    FF      00      00

.. note::

    Outputs of each units are packed to the top of their initial row.

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

.. note::

    In other words, these are also valid algorithms:

    .. code:: text

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


## Algorithm

### Reduce

Now let's make some templates. This involves figuring out where you want to place:

- Carry Save Adders -- CSA (Half Adders, HA, are automatically placed when using
simple templates) [3 to 2]

- Adders -- [2 to 1]

and in the future:

- Greedy Adders -- Adder which makes use of carry in (cin) [2 to 1]

Collectively these are arithmetic units. All of which reduce a set of partial products
by 1, each with their characteristics in latency, complexity and size. None of this
applies to multiplied.

.. note::
    Decoders are an exception and can potentially reduce a set of partial products
    by more than 1.

    - Decoders -- [n to n-k]

    They encode specialised operations based on bit position, count, unary count,
    etc. Decoders are in the `roadmap <roadmap>`_.

To inform the algorithm on how a given template reduces groups of partial products,
an array of characters, or pattern is used:

.. code-block:: python

    pattern = [
        a,      # +-
        a,      # | run of 3 == CSA [3 to 2]
        a,      # +-
        b,      # +- run of 1 == None -- no reduction needed
    ]

.. note::

    CSAs work on 3 bits at a time, and returns a 2-bit sum of raised bits.
    Adders work on 2 words at a time, each word being x-bits, and returns a single
    word. Bit pairs which sum to 0b10 are carried through the calculation.

For this 4-bit algorithm it will take 3 rounds, minimum, of reduction to reach out
final output:

.. code-block:: text

    # Patterns for each stage of first_alg

    1st:    2nd:    3rd:    output:

    a       c       e       x
    a       c       e
    a       d       _
    b       _       _

.. note::

    Each arithmetic unit will output to the top of its "run". The next section covers
    how to "map" these outputs.

    Underscores represent no operations or noops.

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
