from dataclasses import dataclass


@dataclass
class Component:
    """Representation of a component within the problem."""

    value: int
    red: str
    green: str
    blue: str
    shine: str

    @classmethod
    def parse(cls, line: str) -> "Component":
        """Parse the input line, returning an instance of the class.

        Args:
            line (str): Line to parse.

        Returns:
            Component: Constructed class instance.
        """
        line = line.strip().replace(" ", ":")
        value, r, g, b, *shine = line.split(":")
        return cls(int(value), r, g, b, shine[0] if shine else "")

    @staticmethod
    def to_binary(value: str, to_bit: str) -> str:
        """Get the binary value of the value. `to_bit` specifies the character that becomes a bit, else the rest is 0.

        Args:
            value (str): Value to convert to binary.
            to_bit (str): Character that represents the bit value.

        Returns:
            str: Binary value.
        """
        return "".join("0" if c != to_bit else "1" for c in value)


def part_01() -> None:
    """Solve Part 01."""
    data: list[Component] = []

    with open("./inputs/everybody_codes/stories/03/input_p11.txt", "r") as file:
        for line in file.readlines():
            data.append(Component.parse(line))

    tlt: int = 0
    for component in data:
        r_value: int = int(component.to_binary(component.red, "R"), 2)
        g_value: int = int(component.to_binary(component.green, "G"), 2)
        b_value: int = int(component.to_binary(component.blue, "B"), 2)

        tlt += component.value if g_value > r_value and g_value > b_value else 0

    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solve Part 02."""
    data: list[Component] = []

    with open("./inputs/everybody_codes/stories/03/input_p12.txt", "r") as file:
        for line in file.readlines():
            data.append(Component.parse(line))

    darkest_value: float = float("inf")
    shiniest_value: int = 0
    res: int = 0
    for component in data:
        r_value: int = int(component.to_binary(component.red, "R"), 2)
        g_value: int = int(component.to_binary(component.green, "G"), 2)
        b_value: int = int(component.to_binary(component.blue, "B"), 2)
        shine_value: int = int(component.to_binary(component.shine, "S"), 2)

        sum_scale: int = r_value + g_value + b_value

        if shine_value >= shiniest_value:
            shiniest_value = shine_value

            if sum_scale < darkest_value:
                darkest_value = sum_scale
                res = component.value

    print(f"Part 02: {res}")


def part_03() -> None:
    """Solve Part 03."""
    data: list[Component] = []

    with open("./inputs/everybody_codes/stories/03/input_p13.txt", "r") as file:
        for line in file.readlines():
            data.append(Component.parse(line))

    groups: dict[int, list[int]] = {i: [] for i in range(6)}
    for component in data:
        r_value: int = int(component.to_binary(component.red, "R"), 2)
        g_value: int = int(component.to_binary(component.green, "G"), 2)
        b_value: int = int(component.to_binary(component.blue, "B"), 2)
        shine_value: int = int(component.to_binary(component.shine, "S"), 2)

        # ignore if not in a group
        if 30 < shine_value < 33:
            continue

        # all colour values are equal, ignore
        if len({r_value, g_value, b_value}) == 1:
            continue

        # highest value if 2 different colours, ignore
        if (r_value, g_value, b_value).count(max({r_value, g_value, b_value})) == 2:
            continue

        highest_value: int = max({r_value, g_value, b_value})

        if highest_value == r_value:
            if shine_value < 33:
                groups[0].append(component.value)
            else:
                groups[1].append(component.value)

        elif highest_value == g_value:
            if shine_value < 33:
                groups[2].append(component.value)
            else:
                groups[3].append(component.value)

        else:
            if shine_value < 33:
                groups[4].append(component.value)
            else:
                groups[5].append(component.value)

    tlt: int = sum(sorted(groups.values(), key=len, reverse=True)[0])
    print(f"Part 03: {tlt}")


if __name__ == "__main__":
    part_01()
    part_02()
    part_03()
