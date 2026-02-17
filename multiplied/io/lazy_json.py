from collections.abc import Generator
from multiplied import Algorithm, Matrix
import json


def validate_path(path: str) -> None:
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not path.endswith('.json'):
        raise ValueError("path must end with .json")

# ! Need revisiting once loading and storing to .parquet established
def json_pretty_store(scope: Generator, alg: Algorithm, path: str) -> None:
    """Format objects produced by generator then send to JSON file"""

    validate_path(path)
    if not isinstance(scope, Generator):
        raise TypeError("gen must be a generator")
    with open(path, 'w') as f:
        for a, b in scope:
            matrix = Matrix(alg.bits, a=a, b=b)
            pretty = []
            for i in matrix:
                row = [str(x) for x in i]
                pretty += ["".join(row)]
            payload = {
                "A": a,
                "B": b,
                "Product": a * b,
                'Stage_0': {
                    'Matrix': pretty,
                    },
            }
            json.dump(payload, f, indent=4)

def export_algorithm(source: Algorithm, path: str) -> None:
    """
    Export multiplied algorithm to JSON file
    """
    validate_path(path)
    if not isinstance(source, Algorithm):
        raise TypeError("source must be an Algorithm")

    print(source.__dict__)
    # -- convert multiplied objects to built-in ---------------------
    payload = {
        'bits': source.bits,
        'state': source.state,
        'matrix': [str(source.matrix)[:-1].split('\n')],
    }

    alg = {}
    for i, stage in source.algorithm.items():
        alg[i] = {}
        for k, step in stage.items():
            alg[i][k] = [str(step)[:-1].split('\n')]
    payload['algorithm'] = alg

    with open(path, 'w') as f:
        json.dump(payload, f, indent=4)

    return None

def import_algorithm(path: str) -> Algorithm:
    """
    Import multiplied algorithm from JSON file
    """
    # Low priority
    raise NotImplementedError("import_algorithm is not implemented yet")

    # validate_path(path)
    # from multiplied import Template, Matrix, Map
    # with open(path, 'r') as f:
    #     payload = json.load(f)

    # print()
    # print(payload)

    # alg = Algorithm(payload['matrix'])
    # alg.state = payload['state']

    # pretty_alg = payload['algorithm']
    # true_alg = {}
    # for i, stage in pretty_alg.items():
    #     true_alg[i] = {}
    #     for k, step in stage.items():
    #         if step == 'Template':
                # test if result included

            # alg[i][k] = [[str(step)[:-1].split('')] for ]


    # return alg
