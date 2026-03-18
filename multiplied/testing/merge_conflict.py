import multiplied as mp
from multiplied.tests import REFERENCE



def main() -> None:
    alg = mp.Algorithm(8)
    mp.mprint(REFERENCE["mosaic_template"][8]["T"])
    template = mp.Template(REFERENCE["mosaic_template"][8]["T"])
    print(template)
    alg.push(template, mp.Map(REFERENCE["zero_map"][8]))
    # # alg.auto_resolve_stage()
    # print(template.result)
    # print(template.re_bounds)

    for i in alg.exec(255, 128).values():
        print(i)



if __name__ == "__main__":
    main()
