"""Rewrite the README badge section as fixed-size HTML images.

Runs inside the pemtajo/badge-readme container (see .github/workflows/main.yml)
and reuses its Credly scraper, but writes <img width=...> tags instead of
Markdown images. Markdown cannot set an image size, so the badges were only as
small as Credly's resized image happened to be.
"""
import html
import os
import re
import sys

START = "<!--START_SECTION:badges-->"
END = "<!--END_SECTION:badges-->"
MD_BADGE = re.compile(r"^\[!\[(?P<title>.*)\]\((?P<img>\S+)\)\]\((?P<href>\S+)\)$")
SIZE_IN_URL = re.compile(r"(images\.credly\.com/size/)\d+x\d+/")


def to_html(md_badges, size):
    lines = []
    for line in md_badges.splitlines():
        m = MD_BADGE.match(line.strip())
        if not m:
            continue
        title = html.escape(m["title"].replace('\\"', '"'), quote=True)
        img = SIZE_IN_URL.sub(rf"\g<1>{size}x{size}/", m["img"])
        lines.append(
            f'<a href="{html.escape(m["href"], quote=True)}">'
            f'<img src="{html.escape(img, quote=True)}" alt="{title}" title="{title}" width="{size}">'
            "</a>"
        )
    return "\n".join(lines)


def replace_section(readme, badges_html):
    start, end = readme.index(START), readme.index(END)
    return readme[: start + len(START)] + "\n" + badges_html + "\n" + readme[end:]


def main():
    size = int(os.environ.get("BADGE_SIZE", "80"))
    readme_path = os.path.join(os.environ.get("GITHUB_WORKSPACE", "."), "README.md")

    sys.path.insert(0, "/app")  # where the action's code lives in its image
    from credly import Credly

    badges_html = to_html(Credly().get_markdown() or "", size)
    if not badges_html:
        sys.exit("No badges found on Credly; leaving README untouched.")

    with open(readme_path, encoding="utf-8") as f:
        readme = f.read()
    new_readme = replace_section(readme, badges_html)
    if new_readme != readme:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_readme)
        print(f"README badge section updated ({badges_html.count('<img ')} badges).")
    else:
        print("README badge section already up to date.")


if __name__ == "__main__":
    main()
