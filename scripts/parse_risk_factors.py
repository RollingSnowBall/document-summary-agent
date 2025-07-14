import re
import json
from bs4 import BeautifulSoup


def extract_item_1a_section(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # Try to locate the start of Item 1A
    item_start = None
    item_heading_pattern = re.compile(r"Item\s*1A", re.I)

    for tag in soup.find_all(text=item_heading_pattern):
        text = tag.parent.get_text(" ", strip=True)
        if item_heading_pattern.search(text):
            item_start = tag.parent
            break

    if not item_start:
        return []

    # Collect elements until the next Item 1B or Item 2 heading
    end_heading_pattern = re.compile(r"Item\s*1B|Item\s*2", re.I)
    paragraphs = []
    for elem in item_start.next_elements:
        if getattr(elem, "get_text", None):
            text = elem.get_text(" ", strip=True)
            if end_heading_pattern.match(text):
                break
            if elem.name == "p" and text:
                paragraphs.append(text)

    return paragraphs


def chunk_paragraphs(paragraphs):
    chunks = []
    offset = 0
    for idx, text in enumerate(paragraphs):
        chunk = {
            "item": "Item 1A - Risk Factors",
            "index": idx,
            "start_pos": offset,
            "text": text,
        }
        chunks.append(chunk)
        offset += len(text)
    return chunks


def parse_file(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    paragraphs = extract_item_1a_section(html)
    return chunk_paragraphs(paragraphs)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse Item 1A section from a 10-K HTML file")
    parser.add_argument("input", help="Path to 10-K HTML file")
    parser.add_argument("output", help="Path to output JSON file")
    args = parser.parse_args()

    chunks = parse_file(args.input)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
