import multiplied as mp
from multiplied.tests import REFERENCE

"""
Strategy:

    > Upon creation calculate bounds
    > add a __setattr__ function to update bounds if map is modified

"""


def main() -> None:
    ref_dadda_map = REFERENCE["dadda_map"][8]
    print(mp.Map(ref_dadda_map))

    count = 0
    for y in ref_dadda_map:
        for x in y:
            if x == "00":
                count += 1

    shape = (len(ref_dadda_map), len(ref_dadda_map[0]))
    print(f"Cycles wasted: {count}")
    print(f"Efficiency: % {100 * count/(shape[0]*shape[1])}")



if __name__ == "__main__":
    main()
