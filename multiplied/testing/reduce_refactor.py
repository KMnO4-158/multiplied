import multiplied as mp
from multiplied.tests import REFERENCE


"""Algorithm.__reduce method fails with complex templates

Strategy:

    > split ppm using templates bounds
    > reduce each ppm in isolation
        - use bounds to isolate lines for reduction
    > merge [ppm]s using template.result bounds
        - conflicts are accumulated for a given column
            ~ once all columns are merged, append conflicts
            ~ conflicting columns are hoisted to first
              non-conflicting column index.

"""


class ReduceRefactor(mp.Algorithm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)   # runs Parent.__init__
    #     print("init")

    def _reduce(self) -> None:
        """use template or pattern to reduce a given matrix."""
        from copy import copy

        # -- implementation -----------------------------------------
        #
        # Arithmetic units are defined by how many rows they cover, or
        # their 'run', the length of which determines the type of unit:
        #
        # run = 3:
        #   CSA: carry is placed to the left of source column
        #   and one row down to avoid corrupting adjacent columns.
        #
        #   [input-------] | [output------]
        #   ...00100010... | ...00100010...
        #   ...00101010... | ..00101010....
        #   ...00101010... | ...________...
        #
        # run = 2:
        #   binary adder: generates carry through propagates, with a
        #   final carry extending past original width.
        #
        #   [input-------] | [output------]
        #   ...00110110... | ..001100000...
        #   ...00101010... | ...________...

        # -- isolate units -----------------------------------------

        bounds = self.algorithm[self.state]["template"].bounds
        units = mp.matrix_scatter(self.matrix.matrix, bounds)

        # -- reduce -------------------------------------------------
        n = self.bits << 1
        results = {}
        chars = list(bounds.keys())
        for ch in chars:
            base_index = bounds[ch][0][1]
            matrix = units[ch]
            print(ch, bounds[ch])
            mp.mprint(matrix)
            match bounds[ch][-1][1] - bounds[ch][0][1] + 1:  # row height
                case 1:  # NOOP
                    output = results[ch] = mp.Matrix(matrix)
                    print(output)
                    continue

                case 2:  # ADD
                    # TODO: make use of checksums or use bounds

                    operand_a = copy(matrix[base_index])
                    operand_b = copy(matrix[base_index + 1])
                    checksum = [False] * n

                    # -- skip empty rows ----------------------------
                    start = 0
                    while operand_a[start] == "_" and operand_b[start] == "_":
                        start += 1

                    for i in range(start, n):
                        # -- row checksum ---------------------------
                        if operand_a[i] != "_" or operand_b[i] != "_":
                            checksum[i] = True

                        # -- normalise binary -----------------------
                        if operand_a[i] == "_" and operand_b[i] != "_":
                            operand_a[i] = "0"

                        elif operand_b[i] == "_" and operand_a[i] != "_":
                            operand_b[i] = "0"

                        elif operand_a[i] == "_" and operand_b[i] == "_":
                            operand_a[i] = "0"
                            operand_b[i] = "0"

                    # -- binary addition ----------------------------
                    bits_ = sum(checksum)
                    cout = 1 if not checksum[0] else 0
                    int_a = int("".join(operand_a[start : start + bits_]), 2)
                    int_b = int("".join(operand_b[start : start + bits_]), 2)

                    output = [["_"] * (start - cout)]
                    output[0] += list(f"{int_a + int_b:0{bits_ + cout}b}")
                    output[0] += ["_"] * (n - bits_ - start)

                case 3:  # CSA
                    # TODO: make use of checksums or use bounds
                    operand_a = copy(matrix[base_index])
                    operand_b = copy(matrix[base_index + 1])
                    operand_c = copy(matrix[base_index + 2])

                    empty = False
                    output = [["_"] * n, ["_"] * n]
                    start = 0

                    # -- skip empty rows ----------------------------
                    while (
                        operand_a[start] == "_"
                        and operand_b[start] == "_"
                        and operand_c[start] == "_"
                    ):
                        start += 1

                    # -- sum columns -------------------------------
                    for i in range(start, n):
                        csa_sum = 0
                        csa_sum += 1 if operand_a[i] == "1" else 0
                        csa_sum += 1 if operand_b[i] == "1" else 0
                        csa_sum += 1 if operand_c[i] == "1" else 0

                        output[0][i] = csa_sum  # uses index to store sum in-place
                        empty = (
                            (operand_c[i] == "_")
                            + (operand_b[i] == "_")
                            + (operand_a[i] == "_")
                        )
                        # -- check end of unit ----------------------
                        if empty == 3:
                            output[0][i] = "_"  # set as empty since sum unused
                            break
                        if empty == 2:
                            output[0][i] = "1" if csa_sum & 1 else "0"
                            continue

                        # -- brute force index 0 --------------------
                        # ! remove try catch:
                        # ! handle index zero outside of loop
                        # ! unit may not even overlap index 0
                        try:
                            output[0][i] = "1" if csa_sum & 1 else "0"
                            output[1][i - 1] = "1" if csa_sum & 2 else "0"
                        except IndexError:
                            pass
                case _:
                    if ch != "_":
                        raise ValueError(
                            f"Unsupported unit type, len={bounds[ch][-1][1] - bounds[ch][0][1]}"
                        )
                    results[ch] = mp.Matrix(matrix)
                    continue

            print(output)
            # -- build unit into matrix -----------------------------
            unit_result = [[]] * self.bits
            i = 0
            while i < base_index:
                unit_result[i] = ["_"] * n
                i += 1
            for row in output:
                unit_result[i] = row
                i += 1
            while i < self.bits:
                unit_result[i] = ["_"] * n
                i += 1
            results[ch] = mp.Matrix(unit_result)

        # ! difficult sanity checks --------------------------------- ! #
        # Complex scenarios, where NOOP, CSA and ADD units intersect
        # will require extensive checks:
        #
        #   [example--] || [region--]
        #   ...BbaAa... || ....ba....
        #   ...CcaAa... || ....ca....
        #   ...CcaAa... || ....ca....
        #
        #
        # If repeated along the same y-axis, resolution can get very tricky.
        # One method could be skipping merges and opting for merges with non
        # conflicting units, repeat until few partially merged templates remain
        # and finally resolve conflicts, if possible.
        #
        # These conflicts can quickly be found by checking the sum of possible
        # bit positions in a given region of intersecting arithmetic units.
        # The example's sum for the first column is == 3.  This should raise a
        # flag indicating it should be merged later.
        #
        # This functionality to be implemented at a later date.

        # -- merge --------------------------------------------------
        re_bounds = self.algorithm[self.state]["template"].re_bounds

        if 1 < len(results):
            self.matrix = mp.matrix_merge(results, re_bounds)
        else:
            self.matrix = list(results.values())[0]

        # -- map ----------------------------------------------------

        self.matrix.apply_map(self.algorithm[self.state]["map"])

        return None


def main() -> None:
    alg = mp.Algorithm(8)
    template = mp.Template(mp.Pattern(["a", "b", "b", "c", "c", "c", "_", "_"]))
    alg.push(template)
    alg.auto_resolve_stage()
    print(alg)
    output = alg.exec(255, 128)
    for i in output.values():
        print(i)

    product = int("".join(list(output.values())[-1][0][0]), 2)
    print(product)

    alg = mp.Algorithm(8)
    ref_complex_template = mp.Template(REFERENCE["complex_template"][8]["T"])
    print(ref_complex_template)
    alg.push(ref_complex_template)
    alg.auto_resolve_stage()
    print(alg)
    output = alg.exec(127, 255)
    for i in output.values():
        print(i)

    product = int("".join(list(output.values())[-1][0][0]), 2)
    print(product)
    print(127 * 255)


if __name__ == "__main__":
    main()

"""

# -- build template and result ------------------------------
keys = sorted(template_slices.keys())
template = []
result = []
for k in keys:
    template += template_slices[k][0]
    result += template_slices[k][1]



[(6, 0), (15, 0), (6, 1), (11, 1), (13, 1), (14, 1), (13, 2), (13, 2)]
______1011111111
______111111_11_
_____________1__
________________
________________
________________
________________
________________
"""
