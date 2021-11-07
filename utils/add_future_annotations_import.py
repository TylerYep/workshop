FLAKE8_OUTPUT = """

"""


def main() -> None:
    num_lines_added = 0
    add_line = "from __future__ import annotations"
    for line in FLAKE8_OUTPUT.split("\n"):
        if line and add_line in line:
            filename = line.split(":")[0]
            filepath = f"/Users/tyler.yep/robinhood/rh/{filename}"
            with open(filepath, encoding="utf-8") as f:
                lines = f.read()
            if lines.split("\n")[0] != add_line:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"{add_line}\n{lines}")
                num_lines_added += 1

    print(f"Total lines added: {num_lines_added}")


if __name__ == "__main__":
    main()
