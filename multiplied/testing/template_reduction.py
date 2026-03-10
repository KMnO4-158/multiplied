import multiplied as mp


def main() -> None:
    pattern = mp.Pattern(["a", "a", "b", "b", "c", "c", "d", "d"])
    template = mp.Template(pattern)
    raw_template = template.template
    mp.mprint(raw_template)
    no_result_template = mp.Template(raw_template, result=[])
    print(no_result_template)


if __name__ == "__main__":
    main()
