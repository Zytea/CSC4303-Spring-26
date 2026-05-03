from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "exams" / "source_cache" / "filtered_snippets.md"
DEFAULT_OUTPUT = ROOT / "exams" / "exam_sources.md"


@dataclass
class SnippetEntry:
    ids: str
    pages: str = ""
    overlap: str = ""
    sources: list[str] = field(default_factory=list)
    text_blocks: list[str] = field(default_factory=list)


@dataclass
class ExamBlock:
    course: str
    title: str
    entries: list[SnippetEntry] = field(default_factory=list)


@dataclass
class RenderContext:
    major: str = ""
    emitted_contexts: set[str] = field(default_factory=set)
    parent_subpart: str = ""
    nested_counter: int = 0


def parse_filtered_snippets(md: str) -> list[ExamBlock]:
    blocks: list[ExamBlock] = []
    current_block: ExamBlock | None = None
    current_entry: SnippetEntry | None = None
    in_text = False
    text_lines: list[str] = []

    def finish_text_block() -> None:
        nonlocal text_lines
        if current_entry is not None:
            current_entry.text_blocks.append("\n".join(text_lines).strip())
        text_lines = []

    for raw in md.splitlines():
        line = raw.rstrip("\n")

        if in_text:
            if line.strip() == "```":
                finish_text_block()
                in_text = False
            else:
                text_lines.append(line)
            continue

        if line.strip() == "```text":
            in_text = True
            text_lines = []
            continue

        if line.startswith("## "):
            heading = line[3:].strip()
            if " / " not in heading:
                current_block = None
                current_entry = None
                continue
            course, title = heading.rsplit(" / ", 1)
            current_block = ExamBlock(course=course.strip(), title=title.strip())
            blocks.append(current_block)
            current_entry = None
            continue

        if line.startswith("### ") and current_block is not None:
            current_entry = SnippetEntry(ids=line[4:].strip())
            current_block.entries.append(current_entry)
            continue

        if current_entry is None:
            continue

        if line.startswith("- pages:"):
            current_entry.pages = line.split(":", 1)[1].strip()
        elif line.startswith("- overlap:"):
            current_entry.overlap = line.split(":", 1)[1].strip()
        elif line.startswith("- source:"):
            current_entry.sources.extend(re.findall(r"https?://[^\s>]+", line))

    if in_text:
        finish_text_block()

    return [block for block in blocks if block.entries]


def unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def markdown_cell(text: str) -> str:
    return text.replace("|", r"\|").strip()


def render_table(headers: list[str], rows: list[list[str]], align_right_first: bool = True) -> list[str]:
    escaped_rows = [[markdown_cell(cell) for cell in row] for row in rows]
    escaped_headers = [markdown_cell(header) for header in headers]
    widths = [len(header) for header in escaped_headers]
    for row in escaped_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def row_line(row: list[str]) -> str:
        cells = []
        for i, cell in enumerate(row):
            if i == 0 and align_right_first:
                cells.append(cell.rjust(widths[i]))
            else:
                cells.append(cell.ljust(widths[i]))
        return "| " + " | ".join(cells) + " |"

    separators = []
    for i, width in enumerate(widths):
        width = max(width, 3)
        if i == 0 and align_right_first:
            separators.append("-" * (width - 1) + ":")
        else:
            separators.append("-" * width)

    return [row_line(escaped_headers), "| " + " | ".join(separators) + " |"] + [
        row_line(row) for row in escaped_rows
    ]


def source_label(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name.lower()
    suffix = Path(parsed.path).suffix.lower()
    if suffix == ".pdf":
        return "PDF"
    if suffix in {".txt", ".text"}:
        return "Model solution TXT" if "sol" in name or "answer" in name else "TXT"
    if suffix == ".doc":
        return "Answer DOC" if "answer" in name else "DOC"
    return "Source"


def source_lines(block: ExamBlock) -> list[str]:
    urls = unique_in_order([url for entry in block.entries for url in entry.sources])
    lines: list[str] = []
    for url in urls:
        lines.append(f"{source_label(url)}: <{url}>")
    return lines


def table_page_header(block: ExamBlock) -> str:
    urls = unique_in_order([url for entry in block.entries for url in entry.sources])
    all_pdf = urls and all(Path(urlparse(url).path).suffix.lower() == ".pdf" for url in urls)
    any_doc_page = any(entry.pages.strip().upper() == "DOC" for entry in block.entries)
    return "PDF page(s)" if all_pdf and not any_doc_page else "Page(s)"


def normalize_text_block(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    kept = []
    for line in text.splitlines():
        if re.fullmatch(r"\s*\[page\s+\d+\]\s*", line, flags=re.I):
            continue
        kept.append(line.rstrip())
    text = "\n".join(kept)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def infer_major(ids: str, text: str = "") -> str:
    hit = re.search(r"\b(?:Question|Problem)\s+([0-9]+(?:\.[0-9]+)?)", ids, flags=re.I)
    if hit:
        return hit.group(1)
    hit = re.search(r"(?m)^\s*([0-9]+(?:\.[0-9]+)?)\.\s+", text)
    return hit.group(1) if hit else ""


BOUNDARY_RE = re.compile(
    r"(?m)^[ \t]*(?:"
    r"\([A-Za-z0-9.]+\)\s+|"
    r"[A-Za-z]\.\s+|"
    r"\d+(?:\.\d+)?[.)]\s+|"
    r"(?:Question|Problem)\s+\d+(?:\.\d+)?\b"
    r")"
)
SOLUTION_RE = re.compile(r"\bSolution:\s*", flags=re.I)


def find_next_question_boundary(text: str) -> int | None:
    for match in BOUNDARY_RE.finditer(text):
        prefix = text[: match.start()]
        # Avoid treating an answer's first sentence as a new question.
        if "\n\n" in prefix or not prefix.strip():
            return match.start()
    return None


def split_solution_pairs(text: str) -> list[tuple[str, str]]:
    solutions = list(SOLUTION_RE.finditer(text))
    if not solutions:
        return []

    pairs: list[tuple[str, str]] = []
    cursor = 0
    for index, solution in enumerate(solutions):
        question = text[cursor : solution.start()].strip()
        next_solution_start = solutions[index + 1].start() if index + 1 < len(solutions) else len(text)
        between = text[solution.end() : next_solution_start]

        boundary = find_next_question_boundary(between) if index + 1 < len(solutions) else None
        if boundary is None:
            answer = between.strip()
            cursor = next_solution_start
        else:
            answer = between[:boundary].strip()
            cursor = solution.end() + boundary

        if question or answer:
            pairs.append((question, answer))

    return pairs


SUBPART_RE = re.compile(r"(?m)^[ \t]*(\([A-Za-z0-9.]+\)|[A-Za-z]\.)\s+")


def normalize_key(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def clean_points(text: str) -> str:
    text = re.sub(r"\s*\(\s*\d+(?:\.\d+)?\s*points?\s*\)", "", text, flags=re.I)
    text = re.sub(r"\s*\(\s*\d+\s*pts?\s*\)", "", text, flags=re.I)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def repair_identifier_breaks(text: str) -> str:
    return re.sub(r"\b([A-Za-z][A-Za-z0-9]*)-\s+([A-Za-z][A-Za-z0-9_]*)\(", r"\1_\2(", text)


def add_inline_code_for_functions(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        value = match.group(0)
        if value.startswith("`") or value.endswith("`"):
            return value
        if "_" in value.split("(", 1)[0] or "*" in value:
            return f"`{value}`"
        return value

    return re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\([^()\n]*\)", repl, text)


def normalize_question_text(text: str) -> tuple[str, bool]:
    has_tf = bool(
        re.search(r"\[(?:True,\s*False|False,\s*True)\]", text, flags=re.I)
        or re.search(r"(?:^|\s)True\s+False(?:\s|$)", text, flags=re.I)
        or re.search(r"True\s*/\s*False", text, flags=re.I)
    )
    text = text.replace("√", "")
    text = re.sub(r"\[(?:True,\s*False|False,\s*True)\]\s*", "", text, flags=re.I)
    text = re.sub(r"\bTrue\s*/\s*False:?\s*", "", text, flags=re.I)
    text = re.sub(r"\bTrue\s+False\b\s*", "", text, flags=re.I)
    text = repair_identifier_breaks(text)
    text = clean_points(text)
    text = re.sub(r"\s+([,.?!;:])", r"\1", text)
    text = add_inline_code_for_functions(text)
    return text.strip(), has_tf


def normalize_answer_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^(?:Ans(?:wer)?\.?:)\s*", "", text, flags=re.I)
    text = re.sub(r"^(True|False)\s*[-:]\s*", r"\1. ", text, flags=re.I)
    text = re.sub(r"^(TRUE|FALSE)\s*[-:]\s*", r"\1. ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() or "[Solution missing in source snippet.]"


def is_instruction_context(text: str) -> bool:
    compact = normalize_key(text)
    if not compact:
        return True
    instruction_phrases = [
        "keep your answers brief",
        "circle whether each statement",
        "each correct answer is worth",
        "grading is",
        "mark which category",
        "you will be graded",
        "no explanation is necessary",
    ]
    return any(phrase in compact for phrase in instruction_phrases) and "?" not in compact


def detect_parent_subpart(context: str) -> str:
    matches = list(re.finditer(r"(?m)^[ \t]*\(([A-Za-z0-9.]+)\)\s+", context))
    if matches:
        return matches[-1].group(1)
    return ""


def strip_leading_marker(text: str) -> tuple[str, str, str]:
    text = text.strip()
    hit = re.match(r"^\(([A-Za-z0-9.]+)\)\s*(.*)", text, flags=re.S)
    if hit:
        return "paren", hit.group(1), hit.group(2).strip()
    hit = re.match(r"^([A-Za-z])\.\s*(.*)", text, flags=re.S)
    if hit:
        return "letter", hit.group(1), hit.group(2).strip()
    hit = re.match(r"^([0-9]+(?:\.[0-9]+)?)[.)]\s*(.*)", text, flags=re.S)
    if hit:
        return "number", hit.group(1), hit.group(2).strip()
    hit = re.match(r"^(Question|Problem)\s+([0-9]+(?:\.[0-9]+)?)\.?\s*(.*)", text, flags=re.S | re.I)
    if hit:
        return "number", hit.group(2), hit.group(3).strip()
    return "", "", text


def render_context(context: str, ctx: RenderContext) -> list[str]:
    context = context.strip()
    if not context or is_instruction_context(context):
        return []

    key = normalize_key(context)
    if key in ctx.emitted_contexts:
        return []
    ctx.emitted_contexts.add(key)

    parent = detect_parent_subpart(context)
    if parent:
        ctx.parent_subpart = parent
        ctx.nested_counter = 0

    kind, marker, body = strip_leading_marker(context)
    if kind == "paren":
        body, has_tf = normalize_question_text(body)
        line = f"({marker}) {body}"
        if has_tf:
            line += " (✅/❌ )"
        return [line]
    if kind == "number":
        body, has_tf = normalize_question_text(body)
        line = f"{marker}. {body}" if body else f"{marker}."
        if has_tf:
            line += " (✅/❌ )"
        return [line]

    body, has_tf = normalize_question_text(context)
    if has_tf:
        body += " (✅/❌ )"
    return [body] if body else []


def render_question(question: str, ctx: RenderContext) -> list[str]:
    question = normalize_text_block(question)
    if not question:
        return []

    matches = list(SUBPART_RE.finditer(question))
    context = ""
    body = question
    if matches:
        last = matches[-1]
        context = question[: last.start()].strip()
        body = question[last.start() :].strip()

    lines = render_context(context, ctx)
    if lines:
        lines.append("")

    kind, marker, body_text = strip_leading_marker(body)
    body_text, has_tf = normalize_question_text(body_text)

    if kind in {"paren", "letter"}:
        if ctx.parent_subpart:
            ctx.nested_counter += 1
            prefix = f"{ctx.nested_counter}."
        elif ctx.major:
            prefix = f"{ctx.major}({marker})"
        else:
            prefix = f"({marker})" if kind == "paren" else f"{marker}."
        line = f"{prefix} {body_text}".strip()
    elif kind == "number":
        ctx.parent_subpart = ""
        ctx.nested_counter = 0
        prefix = f"{marker}."
        line = f"{prefix} {body_text}".strip()
    else:
        line = body_text

    if has_tf and "(✅/❌" not in line:
        line += " (✅/❌ )"
    return lines + ([line] if line else [])


def quote_answer(answer: str) -> list[str]:
    answer = normalize_answer_text(answer)
    lines = []
    for raw in answer.splitlines():
        line = raw.rstrip()
        lines.append(">" if not line else f"> {line}")
    return lines


def render_raw_block(text: str) -> list[str]:
    text = normalize_text_block(text)
    if not text:
        return []
    return ["```text", text, "```"]


def render_text_block(text: str, entry: SnippetEntry) -> list[str]:
    text = normalize_text_block(text)
    if not text:
        return []

    pairs = split_solution_pairs(text)
    if not pairs:
        return render_raw_block(text)

    ctx = RenderContext(major=infer_major(entry.ids, text))
    lines: list[str] = []
    for question, answer in pairs:
        question_lines = render_question(question, ctx)
        if question_lines:
            if lines and lines[-1] != "":
                lines.append("")
            lines.extend(question_lines)
            lines.append("")
        lines.extend(quote_answer(answer))
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    return lines


def render_block(block: ExamBlock) -> list[str]:
    lines = [f"### {block.title}", ""]
    lines.extend(source_lines(block))
    lines.append("")

    rows = [[entry.pages, entry.ids, entry.overlap] for entry in block.entries]
    lines.extend(
        render_table(
            [table_page_header(block), "Problem / subpart ID(s) retained", "CSC4303 overlap"],
            rows,
        )
    )

    for entry in block.entries:
        for text_block in entry.text_blocks:
            rendered = render_text_block(text_block, entry)
            if rendered:
                lines.append("")
                lines.extend(rendered)

    return lines


def render_document(blocks: list[ExamBlock]) -> str:
    lines = ["# CSC4303 Exam Source", ""]
    current_course = ""
    for block in blocks:
        if block.course != current_course:
            if current_course:
                lines.append("")
            lines.append(f"## {block.course}")
            lines.append("")
            current_course = block.course
        lines.extend(render_block(block))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def find_heading(text: str, heading: str, level: int, start: int = 0) -> int:
    hashes = "#" * level
    pattern = re.compile(rf"(?m)^{re.escape(hashes)}\s+{re.escape(heading)}\s*$")
    hit = pattern.search(text, start)
    return hit.start() if hit else -1


def merge_with_existing(existing: str, generated: str, blocks: list[ExamBlock]) -> str:
    if not blocks:
        return existing

    first = blocks[0]
    existing_course = find_heading(existing, first.course, 2)
    if existing_course < 0:
        return generated
    existing_title = find_heading(existing, first.title, 3, existing_course)
    if existing_title < 0:
        return generated

    generated_course = find_heading(generated, first.course, 2)
    generated_title = find_heading(generated, first.title, 3, generated_course)
    if generated_title < 0:
        return generated

    topic_suffix = ""
    suffix_match = re.search(r"(?m)^## Topic filter used\s*$", existing[existing_title:])
    if suffix_match:
        topic_suffix = existing[existing_title + suffix_match.start() :].strip()

    prefix = existing[:existing_title].rstrip()
    body = generated[generated_title:].rstrip()
    parts = [prefix, body]
    if topic_suffix:
        parts.append(topic_suffix)
    return "\n\n".join(part for part in parts if part) + "\n"


SELF_TEST_INPUT = """# Filtered Exam Source Snippets

## CMU 15-440/640 Distributed Systems / Mid Fall 2019

### Question 1(b)
- pages: 2
- overlap: VoIP transport choice
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Midterm-I-WithSolutions.pdf>

```text
1. Circle whether each statement below is true or false. ***ALSO***, give a one to two sentence reason for your answer. Each correct answer is worth 3 points (1pt for the T/F and 2pts for the reason).

(b) (3 points) [True, False] Over a wide area network it is better to use TCP to implement Voice-over-IP telephony rather than UDP given the potential for packet losses.

Solution: False - UDP is still going to be better for the VoIP app since VoIP is real time and the delays caused with TCP retransmision would make things worse. What’s more, VoIP is loss-tolerant.
```

### Question 2(a), 2(b)
- pages: 3
- overlap: RPC over UDP; RPC marshalling of pointer/linked data structures
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Midterm-I-WithSolutions.pdf>

```text
2. In the following, keep your answers brief and to the point (i.e., 2-3 sentences).

(a) (4 points) Can you implement an RPC system using UDP connections, instead of TCP? Answer yes/no and explain why or why not in at most two sentences.

Solution: Yes. It doesnt matter what transport layer protocol you choose for the RPC system. You can choose to implement over an unreliable network connection and rely on RPC system to detect and tolerate the failures.

(b) (4 points) A developer decides to use RPCs to remotely invoke the function Sum- LinkedList(ListItem *head). What problem might they encounter?

Solution: RPC systems don’t handle pointer structures well. The marshalling system would need to figure out how to follow the linked list structure and include all the needed memory locations.
```

### Question 2(f)(a), 2(f)(b)
- pages: 4
- overlap: Cristian-style time synchronization with asymmetric delays
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Midterm-I-WithSolutions.pdf>

```text
[page 4]

(f) (6 points) Nodes A and B wish to time synchronize. The link from A to B takes 40ms, and the link from B to A takes 20ms but these numbers are not known to the computers. They synchronize using Cristian’s algorithm in one round. Node A’s time is 500 and Node B’s time is 632. Node A starts the protocol.

(a) At the completion of the protocol what time does Node A believe it is?

Solution: It takes 40ms for the packet to reach B, so B timestamps it as 632+40 = 672. The response reaches node A with an RTT of 60ms, so node A sets its time to 672+60/2=702.

(b) What, if any, error is in this value and why?

Solution: At the end of the protocol Node B will think it is 692. The error is 10ms. It arose because of the asymmetry in the links.
```
"""


def run_self_test() -> None:
    blocks = parse_filtered_snippets(SELF_TEST_INPUT)
    rendered = render_document(blocks)
    required = [
        "### Mid Fall 2019",
        "| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap",
        "|           2 | Question 1(b)",
        "1(b) Over a wide area network it is better to use TCP to implement Voice-over-IP telephony rather than UDP given the potential for packet losses. (✅/❌ )",
        "> False. UDP is still going to be better for the VoIP app since VoIP is real time",
        "2(b) A developer decides to use RPCs to remotely invoke the function `Sum_LinkedList(ListItem *head)`. What problem might they encounter?",
        "(f) Nodes A and B wish to time synchronize.",
        "1. At the completion of the protocol what time does Node A believe it is?",
        "> At the end of the protocol Node B will think it is 692.",
    ]
    missing = [snippet for snippet in required if snippet not in rendered]
    if missing:
        raise AssertionError("self-test failed; missing snippets:\n" + "\n".join(missing))
    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert filtered exam snippets into exam_sources.md format.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dry-run", action="store_true", help="Print converted Markdown instead of writing it.")
    parser.add_argument("--no-merge", action="store_true", help="Do not preserve existing manual prefix/suffix.")
    parser.add_argument("--self-test", action="store_true", help="Run the built-in conversion test.")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return 0

    if not args.input.exists():
        raise SystemExit(f"input file not found: {args.input}")

    blocks = parse_filtered_snippets(args.input.read_text(encoding="utf-8"))
    if not blocks:
        raise SystemExit(f"no snippet blocks found in {args.input}")

    generated = render_document(blocks)
    if not args.no_merge and args.output.exists():
        generated = merge_with_existing(args.output.read_text(encoding="utf-8"), generated, blocks)

    if args.dry_run:
        print(generated, end="")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(generated, encoding="utf-8", newline="\n")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
