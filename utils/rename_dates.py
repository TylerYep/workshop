from pathlib import Path


def mm_dd_yy_TO_yyyy_mm_dd(extension=".md"):
    for filename in Path().glob(f"*{extension}"):
        new_name = "2020-" + str(filename).replace("-20" + extension, "")
        parts = new_name.split("-")
        for i, part in enumerate(parts):
            if len(part) < 2:
                parts[i] = "0" + parts[i]
        padded_name = "-".join(parts) + extension
        filename.rename(padded_name)


def add_header(extension=".md"):
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
    for filename in Path().glob(f"*{extension}"):
        with open(filename, "r+", encoding="utf-8") as f:
            top_line = f.readline().replace("# ", "").replace("\n", "")
            old = f.read()
            f.seek(0)
            f.write(header.format(top_line))
            f.write(old)


add_header()
