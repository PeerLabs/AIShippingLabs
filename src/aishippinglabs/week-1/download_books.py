"""Download all PDFs listed in books.csv into a local books/ directory."""

import csv
import re
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIR / "books.csv"
BOOKS_DIR = SCRIPT_DIR / "books"


def slugify(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title).strip().lower()
    return re.sub(r"[\s_-]+", "-", slug)


def download(url: str, dest: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request) as response, open(dest, "wb") as f:
        f.write(response.read())


def main() -> None:
    BOOKS_DIR.mkdir(exist_ok=True)

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = (row.get("title") or "").strip()
            pdf_url = (row.get("pdf_url") or "").strip()
            if not title or not pdf_url:
                continue

            dest = BOOKS_DIR / f"{slugify(title)}.pdf"
            if dest.exists():
                print(f"Skipping (already exists): {dest.name}")
                continue

            print(f"Downloading {title} -> {dest.name}")
            try:
                download(pdf_url, dest)
            except Exception as exc:
                print(f"  Failed to download {title}: {exc}")


if __name__ == "__main__":
    main()
