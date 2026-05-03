from __future__ import annotations

import argparse
import hashlib
import html
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import requests


ROOT = Path(__file__).resolve().parents[2]
EXAMS = ROOT / "exams"
SOURCE_MD = EXAMS / "exam_sources.md"
CACHE = EXAMS / "source_cache"
TEXT_CACHE = CACHE / "text"
FILE_CACHE = CACHE / "files"


@dataclass
class SourceBlock:
    course: str
    title: str
    urls: list[str] = field(default_factory=list)
    rows: list[tuple[str, str, str]] = field(default_factory=list)


def safe_name(url: str) -> str:
    parsed = urlparse(url)
    base = Path(parsed.path).name or "download"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    return f"{digest}-{base}"


def iter_urls(line: str) -> list[str]:
    return re.findall(r"https?://[^\s>)]+", line)


def parse_blocks(md: str) -> list[SourceBlock]:
    blocks: list[SourceBlock] = []
    course = ""
    current: SourceBlock | None = None
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            course = line[3:].strip()
            current = None
            continue
        if line.startswith("### "):
            title = line[4:].strip()
            current = SourceBlock(course=course, title=title)
            blocks.append(current)
            continue
        if current is None:
            continue
        urls = iter_urls(line)
        if urls:
            current.urls.extend(urls)
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            first = cells[0].lower() if cells else ""
            is_header = first.startswith(("pdf page", "page(s)")) or (
                first == "doc" and len(cells) > 1 and "problem" in cells[1].lower()
            )
            if len(cells) >= 3 and not is_header:
                current.rows.append((cells[0], cells[1], cells[2]))
    return blocks


def download(url: str, out: Path) -> None:
    if out.exists() and out.stat().st_size > 0:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 exam-source-extractor/1.0"}
    with requests.get(url, timeout=45, headers=headers) as r:
        r.raise_for_status()
        out.write_bytes(r.content)


def run_pdftotext(src: Path, dst: Path) -> bool:
    exe = shutil.which("pdftotext")
    if not exe:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [exe, "-layout", "-enc", "UTF-8", str(src), str(dst)]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode == 0 and dst.exists() and dst.stat().st_size > 0


def extract_pdf_with_pdfplumber(src: Path, dst: Path) -> bool:
    try:
        import pdfplumber
    except Exception:
        return False
    chunks: list[str] = []
    try:
        with pdfplumber.open(src) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
                chunks.append(f"\n\n--- page {i} ---\n{text}")
    except Exception:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(chunks), encoding="utf-8", errors="ignore")
    return bool("".join(chunks).strip())


def extract_doc_strings(src: Path, dst: Path) -> bool:
    # Old Word .doc files are OLE compound documents. This is not a perfect
    # Word parser, but it extracts enough text for manual review when Word or
    # LibreOffice is unavailable.
    try:
        import olefile
    except Exception:
        olefile = None
    data = src.read_bytes()
    chunks: list[str] = []
    if olefile is not None:
        try:
            ole = olefile.OleFileIO(str(src))
            for stream in ole.listdir(streams=True, storages=False):
                if stream[-1] in {"WordDocument", "1Table", "0Table"}:
                    raw = ole.openstream(stream).read()
                    chunks.append(raw.decode("utf-16le", errors="ignore"))
                    chunks.append(raw.decode("latin1", errors="ignore"))
        except Exception:
            pass
    # Fallback: pull printable ASCII-ish runs from the binary.
    ascii_runs = re.findall(rb"[\x09\x0a\x0d\x20-\x7e]{4,}", data)
    chunks.extend(run.decode("latin1", errors="ignore") for run in ascii_runs)
    text = "\n".join(chunks)
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8", errors="ignore")
    return bool(text.strip())


def extract_txt(src: Path, dst: Path) -> bool:
    data = src.read_bytes()
    for enc in ("utf-8", "latin1", "cp1252"):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = data.decode("utf-8", errors="ignore")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8", errors="ignore")
    return bool(text.strip())


def normalize_text(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def text_for_url(url: str) -> Path:
    file_path = FILE_CACHE / safe_name(url)
    suffix = file_path.suffix.lower()
    txt_path = TEXT_CACHE / f"{file_path.name}.txt"
    if txt_path.exists() and txt_path.stat().st_size > 0:
        return txt_path
    if suffix == ".pdf":
        ok = run_pdftotext(file_path, txt_path)
        if not ok:
            ok = extract_pdf_with_pdfplumber(file_path, txt_path)
        if ok:
            txt_path.write_text(normalize_text(txt_path.read_text(encoding="utf-8", errors="ignore")), encoding="utf-8")
            return txt_path
    if suffix in {".txt", ".text"}:
        if extract_txt(file_path, txt_path):
            txt_path.write_text(normalize_text(txt_path.read_text(encoding="utf-8", errors="ignore")), encoding="utf-8")
            return txt_path
    if suffix == ".doc":
        if extract_doc_strings(file_path, txt_path):
            txt_path.write_text(normalize_text(txt_path.read_text(encoding="utf-8", errors="ignore")), encoding="utf-8")
            return txt_path
    # Unknown type: make a best-effort text file.
    extract_txt(file_path, txt_path)
    txt_path.write_text(normalize_text(txt_path.read_text(encoding="utf-8", errors="ignore")), encoding="utf-8")
    return txt_path


def extract_questions_hint(text: str, ids: str, max_chars: int = 2600) -> str:
    # Heuristic snippets around question/problem labels. The generated file is
    # still reviewed by hand; these snippets just remove repetitive copying.
    wanted = re.split(r";|,", ids)
    snippets: list[str] = []
    for raw in wanted:
        raw = raw.strip()
        if not raw:
            continue
        candidates: list[str] = []
        candidates.append(re.escape(raw))
        m = re.search(r"(Question|Problem)\s+([0-9]+)", raw, re.I)
        if m:
            candidates.append(rf"\b{re.escape(m.group(2))}\b")
        m = re.search(r"(?:Question|Problem)\s+([0-9]+)\(([a-zA-Z0-9.]+)\)", raw, re.I)
        if m:
            candidates.append(rf"{re.escape(m.group(1))}\s*[\(\.]?\s*{re.escape(m.group(2))}")
        pattern = re.compile("|".join(candidates), re.I)
        hit = pattern.search(text)
        if not hit:
            continue
        start = max(0, hit.start() - 300)
        end = min(len(text), hit.end() + max_chars)
        snippets.append(text[start:end].strip())
    if not snippets:
        return text[:max_chars].strip()
    seen = set()
    unique = []
    for s in snippets:
        key = s[:200]
        if key not in seen:
            seen.add(key)
            unique.append(s)
    return "\n\n---\n\n".join(unique)


def write_index(blocks: list[SourceBlock]) -> None:
    index = CACHE / "source_index.md"
    lines = ["# Extracted Source Index", ""]
    for b in blocks:
        if not b.rows:
            continue
        lines.append(f"## {b.course} / {b.title}")
        for u in b.urls:
            f = FILE_CACHE / safe_name(u)
            t = TEXT_CACHE / f"{f.name}.txt"
            lines.append(f"- {u}")
            lines.append(f"  - file: `{f.relative_to(ROOT)}`")
            lines.append(f"  - text: `{t.relative_to(ROOT)}`")
        for pages, ids, overlap in b.rows:
            lines.append(f"- retained: pages `{pages}`, ids `{ids}`, overlap: {overlap}")
        lines.append("")
    index.write_text("\n".join(lines), encoding="utf-8")


def write_snippets(blocks: list[SourceBlock]) -> None:
    out = CACHE / "candidate_snippets.md"
    lines = ["# Candidate Snippets", ""]
    for b in blocks:
        if not b.rows:
            continue
        lines.append(f"## {b.course} / {b.title}")
        text_parts = []
        for u in b.urls:
            txt = text_for_url(u)
            text_parts.append(txt.read_text(encoding="utf-8", errors="ignore"))
        text = "\n\n".join(text_parts)
        for pages, ids, overlap in b.rows:
            lines.append(f"### {ids}")
            lines.append(f"- pages: {pages}")
            lines.append(f"- overlap: {overlap}")
            lines.append("")
            lines.append("```text")
            lines.append(extract_questions_hint(text, ids))
            lines.append("```")
            lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--extract", action="store_true")
    parser.add_argument("--snippets", action="store_true")
    args = parser.parse_args()
    if not any((args.download, args.extract, args.snippets)):
        args.download = args.extract = args.snippets = True

    CACHE.mkdir(parents=True, exist_ok=True)
    FILE_CACHE.mkdir(parents=True, exist_ok=True)
    TEXT_CACHE.mkdir(parents=True, exist_ok=True)

    md = SOURCE_MD.read_text(encoding="utf-8")
    blocks = parse_blocks(md)
    urls = []
    for b in blocks:
        for u in b.urls:
            if u not in urls:
                urls.append(u)

    if args.download:
        for i, url in enumerate(urls, start=1):
            out = FILE_CACHE / safe_name(url)
            print(f"[{i}/{len(urls)}] download {url}", flush=True)
            download(url, out)

    if args.extract:
        for i, url in enumerate(urls, start=1):
            print(f"[{i}/{len(urls)}] extract {url}", flush=True)
            text_for_url(url)

    write_index(blocks)
    if args.snippets:
        write_snippets(blocks)
    print(f"wrote {CACHE / 'source_index.md'}")
    print(f"wrote {CACHE / 'candidate_snippets.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
