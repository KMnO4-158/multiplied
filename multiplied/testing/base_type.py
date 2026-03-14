from multiplied.core.dtypes.base import MultipliedMeta


class BaseType(MultipliedMeta):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self._soft_type = list


if __name__ == "__main__":
    testcase = BaseType(10, 11, 12)
    print(testcase._soft_type)
    print(issubclass(type(testcase), MultipliedMeta))
