from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from extract_exam_sources import CACHE, ROOT, parse_blocks, safe_name, text_for_url


SOURCE_MD = ROOT / "exams" / "exam_sources.md"
OUT = CACHE / "filtered_snippets.md"
TEXT_CACHE = CACHE / "text"
FILE_CACHE = CACHE / "files"


@dataclass
class Selector:
    kind: str = ""
    number: str = ""
    subparts: list[str] = field(default_factory=list)
    items: list[str] = field(default_factory=list)
    raw: str = ""


def parse_page_numbers(pages: str) -> list[int] | None:
    if pages.strip().upper() == "DOC":
        return None
    nums: list[int] = []
    for part in re.split(r",\s*", pages):
        part = part.strip()
        if not part:
            continue
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if m:
            nums.extend(range(int(m.group(1)), int(m.group(2)) + 1))
            continue
        m = re.fullmatch(r"\d+", part)
        if m:
            nums.append(int(part))
    return nums or None


def split_pages(text: str) -> list[str]:
    if "\f" in text:
        return text.split("\f")
    matches = list(re.finditer(r"(?m)^--- page (\d+) ---\s*$", text))
    if matches:
        pages = []
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            pages.append(text[m.end():end])
        return pages
    return [text]


def select_pages(text: str, pages: str) -> str:
    page_nums = parse_page_numbers(pages)
    if not page_nums:
        return text
    split = split_pages(text)
    chunks = []
    for n in page_nums:
        idx = n - 1
        if 0 <= idx < len(split):
            chunks.append(f"[page {n}]\n{split[idx]}")
    return "\n\n".join(chunks) if chunks else text


def normalize_ids(ids: str) -> str:
    return re.sub(r"\s+", " ", ids.strip())


def parse_selectors(ids: str) -> list[Selector]:
    ids = normalize_ids(ids)
    if ids.lower().startswith("practice problems"):
        return [Selector(kind="Practice", raw=ids)]

    selectors: list[Selector] = []
    current_kind = ""
    current_number = ""

    pieces = [p.strip() for p in re.split(r";|,", ids) if p.strip()]
    for piece in pieces:
        raw = piece
        item_match = re.search(r"\bitem\s+([A-Za-z0-9.]+)", piece, re.I)

        m = re.search(r"\b(Question|Problem)\s+([0-9]+(?:\.[0-9]+)?)", piece, re.I)
        if m:
            current_kind = m.group(1)
            current_number = m.group(2)
        else:
            m = re.match(r"([0-9]+(?:\.[0-9]+)?)\b", piece)
            if m and current_kind:
                current_number = m.group(1)

        if not current_kind and not current_number:
            selectors.append(Selector(raw=raw))
            continue

        subparts = []
        for sub in re.findall(r"\(([A-Za-z0-9.]+)\)", piece):
            if not sub.isdigit():
                subparts.append(sub)
        dotted = re.search(r"\b[0-9]+(?:\.[0-9]+)?\(([A-Za-z0-9.]+)\)", piece)
        if dotted and dotted.group(1) not in subparts:
            subparts.append(dotted.group(1))

        sel = Selector(kind=current_kind, number=current_number, subparts=subparts, raw=raw)
        if item_match:
            sel.items.append(item_match.group(1))
        selectors.append(sel)

    # Merge repeated question/problem selectors so "Question 2(a), 2(b)" keeps
    # both subparts under one number.
    merged: dict[tuple[str, str], Selector] = {}
    ordered: list[Selector] = []
    for sel in selectors:
        key = (sel.kind.lower(), sel.number)
        if sel.kind and sel.number:
            if key not in merged:
                merged[key] = Selector(kind=sel.kind, number=sel.number, raw=ids)
                ordered.append(merged[key])
            merged[key].subparts.extend(x for x in sel.subparts if x not in merged[key].subparts)
            merged[key].items.extend(x for x in sel.items if x not in merged[key].items)
        else:
            ordered.append(sel)
    return ordered


def heading_pattern(number: str) -> re.Pattern[str]:
    n = re.escape(number)
    patterns = [
        rf"^\s*(?:QUESTION|Question)\s+{n}\b",
        rf"^\s*(?:PROBLEM|Problem)\s+{n}\b",
        rf"^\s*{n}\.\s+",
        rf"^\s*{n}\s*\(",
    ]
    return re.compile("|".join(patterns), re.I | re.M)


def any_major_heading_pattern() -> re.Pattern[str]:
    return re.compile(
        r"^\s*(?:QUESTION|Question|PROBLEM|Problem)\s+[0-9]+(?:\.[0-9]+)?\b|"
        r"^\s*[0-9]+(?:\.[0-9]+)?\.\s+",
        re.I | re.M,
    )


def extract_major_block(text: str, selector: Selector) -> str:
    if not selector.number:
        return text
    pat = heading_pattern(selector.number)
    hit = pat.search(text)
    if not hit:
        return text
    next_hit = None
    for m in any_major_heading_pattern().finditer(text, hit.end()):
        if m.start() > hit.start() + 20:
            next_hit = m
            break
    end = next_hit.start() if next_hit else len(text)
    return text[hit.start():end]


def subpart_start_pattern(number: str, sub: str) -> re.Pattern[str]:
    n = re.escape(number)
    s = re.escape(sub)
    # Covers "(a)", "2(a)", "(2a)", "2A", "1.1", and nested "2(f)(a)" style
    # labels as they appear after pdftotext/doc extraction.
    return re.compile(
        rf"^\s*\({s}\)\s+|"
        rf"^\s*{n}\s*\({s}\)\s+|"
        rf"^\s*\({n}{s}\)\s+|"
        rf"^\s*{n}{s}\b|"
        rf"^\s*{re.escape(number + '.' + sub)}\b",
        re.I | re.M,
    )


def any_subpart_pattern(number: str) -> re.Pattern[str]:
    n = re.escape(number)
    return re.compile(
        rf"^\s*\([a-zA-Z][a-zA-Z0-9.]*\)\s+|"
        rf"^\s*{n}\s*\([a-zA-Z0-9.]+\)\s+|"
        rf"^\s*\({n}[a-zA-Z]\)\s+|"
        rf"^\s*{n}[A-Za-z]\b|"
        rf"^\s*{n}\.[0-9]+\b",
        re.I | re.M,
    )


def extract_subparts(block: str, selector: Selector) -> str:
    targets = selector.subparts + selector.items
    if not targets:
        return block
    starts: list[tuple[int, str]] = []
    for target in targets:
        hit = subpart_start_pattern(selector.number, target).search(block)
        if hit:
            starts.append((hit.start(), target))
    if not starts:
        return block
    starts.sort()
    all_bounds = [m.start() for m in any_subpart_pattern(selector.number).finditer(block)]
    pieces = []
    earlier_bounds = [b for b in all_bounds if b < starts[0][0]]
    intro_end = min(earlier_bounds) if earlier_bounds else starts[0][0]
    intro = block[:intro_end].strip()
    if intro:
        pieces.append(intro[-900:])
    for start, _target in starts:
        end = len(block)
        for b in all_bounds:
            if b > start + 5:
                end = b
                break
        pieces.append(block[start:end].strip())
    return "\n\n".join(p for p in pieces if p)


def extract_by_selectors(text: str, ids: str) -> str:
    selectors = parse_selectors(ids)
    pieces = []
    for selector in selectors:
        block = extract_major_block(text, selector)
        block = extract_subparts(block, selector)
        if block.strip():
            pieces.append(block.strip())
    if not pieces:
        return text
    deduped = []
    seen = set()
    for piece in pieces:
        key = re.sub(r"\s+", " ", piece[:300])
        if key not in seen:
            seen.add(key)
            deduped.append(piece)
    return "\n\n---\n\n".join(deduped)


STRUCTURAL_LINE = re.compile(
    r"^(?:"
    r"\[page\s+\d+\]$|"
    r"---$|"
    r"(?:QUESTION|Question|PROBLEM|Problem)\s+\d+(?:\.\d+)?\b|"
    r"\d+(?:\.\d+)*[.)]\s+|"
    r"\([A-Za-z0-9](?:\.[0-9]+)?\)\s+|"
    r"[A-Za-z]?\d+(?:\.\d+)*\)\s+|"
    r"(?:Solution|Answer|Answers|Explanation):\b"
    r")"
)


def join_wrapped_line(left: str, right: str) -> str:
    right = right.lstrip()
    if not left:
        return right
    if re.search(r"[A-Za-z]-$", left) and re.match(r"[a-z]", right):
        return left[:-1] + right
    if re.match(r"^[,.;:!?%\])]", right):
        return left.rstrip() + right
    return left.rstrip() + " " + right


def reflow_soft_wraps(text: str) -> str:
    out: list[str] = []
    current = ""
    last_blank = False

    def flush() -> None:
        nonlocal current
        if current:
            out.append(current.strip())
            current = ""

    for raw in text.splitlines():
        line = raw.strip().replace("\u00a0", " ").strip()
        if not line:
            flush()
            if out and not last_blank:
                out.append("")
                last_blank = True
            continue

        if re.fullmatch(r"\[page\s+\d+\]|---", line):
            flush()
            if out and out[-1] != "":
                out.append("")
            out.extend([line, ""])
            last_blank = True
            continue

        if current and STRUCTURAL_LINE.match(line):
            flush()

        current = join_wrapped_line(current, line)
        last_blank = False

    flush()
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


def clean_noise(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    for marker in (r"\n\s*PAGE\s+", r"\n\s*Login name\s*:"):
        hit = re.search(marker, text, flags=re.I)
        if hit:
            text = text[:hit.start()]
    text = "".join(ch if ch == "\n" or ch == "\t" or ord(ch) >= 32 else " " for ch in text)
    text = re.sub(r"\n\s*(Name|Andrew ID|UW Net ID)\s*:.*", "", text, flags=re.I)
    text = re.sub(r"\n\s*Page\s+\d+\s*", "\n", text, flags=re.I)
    text = re.sub(r"\n\s*\d+\s*$", "", text)
    text = re.sub(r"\n\s*Question\s+Points\s+Score(?:.|\n)*?Total:\s*\d+\s*", "\n", text, flags=re.I)
    text = re.sub(r"\n\s*This exam has .*?\n", "\n", text, flags=re.I)
    text = re.sub(r"\n\s*Please write .*?\n", "\n", text, flags=re.I)
    text = re.sub(r"[ \t]{2,}", " ", text)
    kept_lines = []
    for line in text.splitlines():
        visible = [ch for ch in line if not ch.isspace()]
        if len(visible) >= 20:
            asciiish = sum(1 for ch in visible if ch.isalnum() or ch in ".,;:!?()[]{}<>+-=*/'\"_`%$#@&|\\~")
            if asciiish / len(visible) < 0.35:
                continue
        kept_lines.append(line)
    text = "\n".join(kept_lines)
    text = re.sub(r"\n\s*PAGE\s*\n[\s\S]*$", "", text, flags=re.I)
    text = re.sub(r"\n\s*Login name\s*:[\s\S]*$", "", text, flags=re.I)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return reflow_soft_wraps(text).strip()


def choose_urls(urls: list[str]) -> list[str]:
    if len(urls) <= 1:
        return urls
    parsed = [(u, Path(urlparse(u).path).suffix.lower(), Path(urlparse(u).path).name.lower()) for u in urls]
    # Princeton DOC answer files usually contain both question wording and key.
    doc_answers = [u for u, suffix, name in parsed if suffix == ".doc" and ("answer" in name or "answers" in name)]
    if doc_answers:
        return doc_answers
    return urls


def filtered_snippet_for(url: str, pages: str, ids: str) -> str:
    txt = text_for_url(url)
    text = txt.read_text(encoding="utf-8", errors="ignore")
    scoped = select_pages(text, pages)
    scoped = extract_by_selectors(scoped, ids)
    scoped = clean_noise(scoped)
    return scoped


def write_filtered() -> None:
    md = SOURCE_MD.read_text(encoding="utf-8")
    blocks = parse_blocks(md)
    lines = ["# Filtered Exam Source Snippets", ""]
    for block in blocks:
        if not block.rows:
            continue
        lines.append(f"## {block.course} / {block.title}")
        for pages, ids, overlap in block.rows:
            lines.append("")
            lines.append(f"### {ids}")
            lines.append(f"- pages: {pages}")
            lines.append(f"- overlap: {overlap}")
            for url in choose_urls(block.urls):
                lines.append(f"- source: <{url}>")
                snippet = filtered_snippet_for(url, pages, ids)
                if snippet:
                    lines.append("")
                    lines.append("```text")
                    lines.append(snippet)
                    lines.append("```")
                else:
                    lines.append("")
                    lines.append("```text")
                    lines.append("[NO MATCH]")
                    lines.append("```")
        lines.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    write_filtered()
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
