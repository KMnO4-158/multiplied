import multiplied as mp


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
        #   binary adder: carry generates through propagates, with a
        #   final carry extending past original width.
        #
        #   [input-------] | [output------]
        #   ...00110110... | ..001100000...
        #   ...00101010... | ...________...

        # -- isolate units -----------------------------------------
        # ! Implement result bounding box to create single point of truth ! #
        # - currently every stage of every matrix reduction needs to resolve
        #   conflicts dynamically before merging vs doing so once via the
        #   resultant template
        bounds: dict = self.algorithm[self.state]["template"].bounds

        # -- reduce -------------------------------------------------
        n = self.bits << 1
        results = {}
        chars = list(bounds.keys())
        # chars.remove("_") # ! this deletes info about rows which are not reduced
        for ch in chars:
            base_index = bounds[ch][0][1]
            match bounds[ch][-1][1] - bounds[ch][0][1] + 1:  # row height
                case 1:  # NOOP
                    output = [copy(self.matrix[base_index][0])]

                case 2:  # ADD
                    # TODO: make use of checksums or use bounds

                    operand_a = copy(self.matrix[base_index][0])
                    operand_b = copy(self.matrix[base_index + 1][0])
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
                    operand_a = copy(self.matrix[base_index][0])
                    operand_b = copy(self.matrix[base_index + 1][0])
                    operand_c = copy(self.matrix[base_index + 2][0])
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
                            continue
                case _:
                    if ch != "_":
                        raise ValueError(
                            f"Unsupported unit type, len={bounds[ch][-1][1] - bounds[ch][0][1]}"
                        )
                    continue

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

        # -- merge units to matrix ----------------------------------
        # Merge in any order, checking for overlaps between borders
        # resolve conflicts by summing present bit positions and shifting
        # a target unit's bit

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
        if 1 < len(results):
            self.matrix = mp.matrix_merge(results, bounds)
        else:
            self.matrix = list(results.values())[0]

        # -- map ----------------------------------------------------

        self.matrix.apply_map(self.algorithm[self.state]["map"])

        return None





def main() -> None:
    alg = ReduceRefactor(8)
    alg.auto_resolve_stage(recursive=False)
    alg.step()

if __name__ == "__main__":
    main()
