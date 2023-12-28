from pathlib import Path


def convert_mm_dd_yy_to_yyyy_mm_dd(extension: str = ".md") -> None:
    for filepath in Path().glob(f"*{extension}"):
        new_name = "2020-" + str(filepath).replace("-20" + extension, "")
        parts = new_name.split("-")
        for i, part in enumerate(parts):
            if len(part) < 2:
                parts[i] = "0" + parts[i]
        padded_name = "-".join(parts) + extension
        filepath.rename(padded_name)


def add_header(extension: str = ".md") -> None:
    header = (
        "---\n"
        "title: {}\n"
        "author: Tyler Yep\n"
        "author_title: Software Engineer @ Robinhood\n"
        "author_url: https://github.com/tyleryep\n"
        "author_image_url: https://github.com/tyleryep.png\n"
        "tags: [robinhood, intern]\n"
        "---\n"
    )
    for filepath in Path().glob(f"*{extension}"):
        with filepath.open("r+", encoding="utf-8") as f:
            top_line = f.readline().replace("# ", "").replace("\n", "")
            old = f.read()
            f.seek(0)
            f.write(header.format(top_line))
            f.write(old)


add_header()
