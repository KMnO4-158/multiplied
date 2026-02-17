from pathlib import Path
import multiplied as mp
# import pathlib


def test_to_json_4():
    scope = mp.truth_scope((1, 15), (1, 255))
    alg   = mp.Algorithm(4)
    path  = Path(__file__).parent.parent.parent / 'examples/datasets/example_4b_mult_truthtable.json'

    mp.json_pretty_store(scope, alg, str(path))


def test_to_json_8():
    scope = mp.truth_scope((1, 255), (1, 1000))
    alg   = mp.Algorithm(8)
    path  = Path(__file__).parent.parent.parent / 'examples/datasets/example_8b_mult_truthtable.json'
    mp.json_pretty_store(scope, alg, str(path))

def main() -> None:
    ...


if __name__ == '__main__':
    main()
