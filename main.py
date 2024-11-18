import os
import sys
from pathlib import Path


def create_year_day_folder(year: str, day: str) -> None:
    """Create the year-day folder for the problem, as well as the template files."""
    try:
        # Loading the template
        template: str
        with open("./other/template.txt") as file:
            template = file.read()

        # Creating folder
        path: str = f"./{year}/day{day}"
        P: Path = Path(path)

        if not P.exists():
            P.mkdir()
            print(f"Created directory: {path}")

        else:
            print(f"Directory exists: {path}")

        os.chdir(P.absolute())

        # Create solution file
        if not os.path.isfile(f"day{day}.py"):
            with open(f"day{day}.py", "w") as target_file:
                target_file.write(template)

            print(f"Created file: day{day}.py")

        else:
            print(f"{path}/day{day}.py exists")

        # Create the data files
        for i in range(3):
            if not os.path.isfile(f"p{i + 1}.txt"):
                with open(f"p{i + 1}.txt", "w") as file:
                    file.write("")

                print(f"Created data file: p{i + 1}.txt")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    # Creating the necessary folders for solving a problem
    create_year_day_folder(sys.argv[1], sys.argv[2])
