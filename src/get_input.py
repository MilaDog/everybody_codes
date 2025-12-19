import argparse
import os
from datetime import datetime as dt
from pathlib import Path

PARSER = argparse.ArgumentParser()

PARSER.add_argument("-d", "--day", help="Day of the event to get. [01, 25]")
PARSER.add_argument("-y", "--year", help="Year of the event to get. [2015, current-year)")
PARSER.add_argument("-l", "--language", help="Language being used.")


# EXCEPTIONS
class TemplateException(Exception):
    """Exception for handling the loading of solution templates."""

    def __init__(self, message: str):
        self.message: str = message


def get_template(language: str) -> str:
    """Return the solution template for the given language."""
    match language.lower():
        case "python":
            try:
                with open(os.path.join(Path(__file__).resolve().parent, "templates/template.py")) as file:
                    return file.read()

            except Exception:
                raise TemplateException(f"Unable to load {language.upper()} template.")

        case _:
            raise TemplateException(f"Unknown language: {language.upper()}.")


def create_solution_folder(language: str, year: str, day: str) -> Path:
    """Create the target folder that will contain the problem solution file."""
    folder_path: Path = Path(__file__).resolve().parent
    match language.lower():
        case "python":
            folder_path /= f"{language.lower()}/{year}/{str(day).zfill(2)}"

        case _:
            print(f"Unknown langauge: {language.upper()}")
            exit(1)

    if not folder_path.exists():
        folder_path.mkdir(parents=True)
        print(f"Created solution directory: `{folder_path}`.")

    else:
        print(f"Directory exists: `{folder_path}`.")

    return folder_path


def create_solution_file(path: Path, language: str, year: str, day: str) -> None:
    """Create the solution file using the target template."""
    template: str = ""

    try:
        template = get_template(language=language)

    except TemplateException as ex:
        print(ex.message)
        exit(1)

    # Replacing placeholders
    template = template.replace("%%YEAR%%", str(year))
    template = template.replace("%%DAY%%", str(day).zfill(2))

    # Create solution file
    match language.lower():
        case "python":
            path /= f"day{str(day).zfill(2)}.py"

        case _:
            print(f"Unknown langauge: {language.upper()}")
            exit(1)

    if not os.path.isfile(path):
        with open(path, "w") as target_file:
            target_file.write(template)

        print(f"Created solution file: `{path}`")

    else:
        print(f"Solution file already exists: `{path}`")


def create_input_file(year: str, day: str) -> None:
    """Create the data file for the given day and year."""
    inputs_path: Path = Path(f"./inputs/everybody_codes/{year}/{str(day).zfill(2)}")

    if not inputs_path.exists():
        inputs_path.mkdir(parents=True, exist_ok=True)
        print(f"Created inputs folder: `{inputs_path}`.")

    for i in range(3):
        input_file_name: str = f"input_p0{i + 1}.txt"

        if not os.path.isfile(inputs_path / input_file_name):
            with open(inputs_path / input_file_name, "w") as file:
                # file.write(get_day_input(day=day, year=year))
                file.write("")

            print(f"Created data file: `{inputs_path / input_file_name}`.")

    else:
        print("Input file already exists.")


def main() -> None:
    """Entry point."""
    args = PARSER.parse_args()

    day: int = int(args.day) if args.day else dt.now().day
    year: int = int(args.year) if args.year else dt.now().year
    language: str = args.language if args.language else "python"

    # Checks
    invalid: bool = False
    if day < 1 or day > 20:
        print(f"Invalid day {day}.")
        invalid = True

    if year < 2024 or year > dt.now().year:
        print(f"Invalid year {year}.")
        invalid = True

    if invalid:
        return

    target_folder: Path = create_solution_folder(language=language, day=str(day), year=str(year))
    create_solution_file(path=target_folder, language=language, day=str(day), year=str(year))
    create_input_file(year=str(year), day=str(day))


if __name__ == "__main__":
    main()
