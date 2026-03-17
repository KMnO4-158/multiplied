import multiplied as mp
from multiplied.tests import REFERENCE



def main() -> None:
    alg = mp.Algorithm(8)
    template = mp.Template(REFERENCE["mosaic_template"][8]["T"])
    # alg.push(template, mp.Map(REFERENCE["complex_map"][8]))
    alg.auto_resolve_stage()

    for i in alg.exec(4, 20).values():
        print(i)



if __name__ == "__main__":
    main()
