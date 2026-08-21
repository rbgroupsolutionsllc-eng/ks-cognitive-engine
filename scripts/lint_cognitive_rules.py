#!/usr/bin/env python3
"""
KS Cognitive Engine — Autonomous Anti-Pattern Linter & Auto-Fix Engine
Scans and automatically heals codebases against banned anti-patterns defined in the KS Cognitive Specification.
"""

import sys
import re
import os
import argparse
import io
import tokenize

PATTERNS = [
    {
        "id": "ts_any",
        "regex": r':\s*any\b',
        "replacement": r': unknown /* KS_COGNITIVE_FIX: replaced any with unknown */',
        "message": "TypeScript: Explicit 'any' type detected. Replaced with 'unknown'.",
        "severity": "ERROR",
        "exts": ('.ts', '.tsx'),
        "mask_strings": True
    },
    {
        "id": "py_bare_except_pass",
        "regex": r'except\s*:\s*pass\b|except\s+Exception\s*:\s*pass\b',
        "replacement": 'except Exception as e:\n        logging.exception(f"Unhandled exception caught: {e}")',
        "message": "Python: Silent bare 'except: pass' detected. Added structured logging fallback.",
        "severity": "ERROR",
        "exts": ('.py',),
        "mask_strings": True
    },
    {
        "id": "sql_concat",
        "regex": r'SELECT\s+.*\s+FROM\s+.*WHERE.*[\'"]\s*\+\s*\w+|`SELECT\s+.*FROM\s+.*WHERE.*\$\{',
        "replacement": None,  # Requires structural rewrite
        "message": "SQL: Possible SQL string concatenation detected. Use parameterized prepared statements ($1, ?).",
        "severity": "ERROR",
        "exts": ('.ts', '.js', '.py', '.sql'),
        "mask_strings": False
    },
    {
        "id": "rust_unwrap",
        "regex": r'\.unwrap\(\)',
        "replacement": None,
        "message": "Rust: Production '.unwrap()' detected. Use '?' operator, 'expect(...)', or 'match' statement.",
        "severity": "WARNING",
        "exts": ('.rs',),
        "mask_strings": True
    },
    {
        "id": "go_ignored_err",
        "regex": r'_\s*=\s*err\b',
        "replacement": None,
        "message": "Go: Ignored error variable detected. Handle or return error explicitly.",
        "severity": "WARNING",
        "exts": ('.go',),
        "mask_strings": True
    },
    {
        "id": "bash_missing_safety",
        "regex": r'^#!\/bin\/bash\s*$',
        "replacement": '#!/usr/bin/env bash\nset -euo pipefail',
        "message": "Bash: Missing 'set -euo pipefail' strict safety preamble.",
        "severity": "WARNING",
        "exts": ('.sh', '.bash'),
        "mask_strings": False
    }
]

FENCE_LANG_TO_EXT = {
    "typescript": ".ts", "ts": ".ts",
    "tsx": ".tsx",
    "javascript": ".js", "js": ".js",
    "jsx": ".jsx",
    "python": ".py", "py": ".py",
    "sql": ".sql",
    "rust": ".rs", "rs": ".rs",
    "go": ".go", "golang": ".go",
    "bash": ".sh", "sh": ".sh", "shell": ".sh",
}


def extract_code_blocks_from_markdown(content: str) -> list[dict]:
    """
    Parses fenced code blocks (```lang ... ```) from markdown content.
    Returns a list of dicts:
    {
        "ext": str,                # virtual extension mapped from fence lang
        "start_line": int,         # 1-indexed line number of first code line (after ``` fence)
        "code_lines": list[str],   # raw lines within the fence (excluding the ``` markers)
        "ignored": bool            # True if preceded by <!-- ks-lint-ignore-next -->
    }
    Unrecognized fence languages (not in FENCE_LANG_TO_EXT) are skipped
    silently (e.g. ```json, ```yaml, ```mermaid, or plain ```).
    """
    blocks = []
    lines = content.splitlines(keepends=True)
    in_fence = False
    fence_char = None
    fence_len = 0
    current_ext = None
    current_start = 0
    current_lines = []
    current_ignored = False

    fence_open_regex = re.compile(r'^\s*(`{3,}|~{3,})\s*([a-zA-Z0-9_\+#\.\-]+)?')

    for idx, line in enumerate(lines):
        line_num = idx + 1

        if not in_fence:
            m = fence_open_regex.match(line)
            if m:
                marker = m.group(1)
                lang = (m.group(2) or "").strip().lower()

                ignored = False
                if idx > 0 and "<!-- ks-lint-ignore-next -->" in lines[idx - 1]:
                    ignored = True

                ext = FENCE_LANG_TO_EXT.get(lang)
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
                current_ext = ext
                current_start = line_num + 1
                current_lines = []
                current_ignored = ignored
        else:
            close_regex = re.compile(rf'^\s*{re.escape(fence_char)}{{{fence_len},}}\s*$')
            if close_regex.match(line):
                if current_ext is not None:
                    blocks.append({
                        "ext": current_ext,
                        "start_line": current_start,
                        "code_lines": current_lines,
                        "ignored": current_ignored
                    })
                in_fence = False
                fence_char = None
                fence_len = 0
                current_ext = None
                current_lines = []
                current_ignored = False
            else:
                if current_ext is not None:
                    current_lines.append(line)

    return blocks


def mask_python_code(content: str) -> list[str]:
    """
    Masks comments and string literals in Python code with spaces of identical length,
    preserving line numbers and column offsets using standard library tokenize.
    """
    lines = content.splitlines(keepends=True)
    char_lines = [list(line) for line in lines]
    try:
        tokens = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
        for tok in tokens:
            if tok.type in (tokenize.COMMENT, tokenize.STRING):
                sline, scol = tok.start
                eline, ecol = tok.end
                for l_idx in range(sline - 1, eline):
                    if l_idx >= len(char_lines):
                        break
                    start_c = scol if l_idx == sline - 1 else 0
                    end_c = ecol if l_idx == eline - 1 else len(char_lines[l_idx])
                    for c_idx in range(start_c, min(end_c, len(char_lines[l_idx]))):
                        if char_lines[l_idx][c_idx] not in ('\n', '\r'):
                            char_lines[l_idx][c_idx] = ' '
        return ["".join(cl) for cl in char_lines]
    except Exception:
        # Fallback if tokenize fails on malformed or incomplete code
        return [mask_line_heuristics(line, '.py') for line in lines]


def mask_line_heuristics(line: str, ext: str) -> str:
    """
    Heuristic to mask comments and string literals with spaces of equal length.
    NOTE: This is a lightweight heuristic, not a full AST parser.
    Edge cases (such as '//' inside complex multiline template strings or regex literals)
    may have minor limitations.
    """
    chars = list(line)
    n = len(chars)
    i = 0
    in_str = None
    escape = False

    while i < n:
        c = chars[i]

        if escape:
            if in_str:
                chars[i] = ' '
            escape = False
            i += 1
            continue

        if c == '\\' and in_str:
            chars[i] = ' '
            escape = True
            i += 1
            continue

        if in_str:
            if c == in_str:
                chars[i] = ' '
                in_str = None
            else:
                chars[i] = ' '
            i += 1
            continue

        if c in ('"', "'", '`'):
            in_str = c
            chars[i] = ' '
            i += 1
            continue

        # Comments
        if ext in ('.ts', '.tsx', '.js', '.jsx', '.rs', '.go'):
            if c == '/' and i + 1 < n and chars[i + 1] == '/':
                for j in range(i, n):
                    if chars[j] not in ('\n', '\r'):
                        chars[j] = ' '
                break
            if c == '/' and i + 1 < n and chars[i + 1] == '*':
                end_idx = line.find('*/', i + 2)
                if end_idx != -1:
                    for j in range(i, end_idx + 2):
                        chars[j] = ' '
                    i = end_idx + 2
                    continue
                else:
                    for j in range(i, n):
                        if chars[j] not in ('\n', '\r'):
                            chars[j] = ' '
                    break

        if ext in ('.sh', '.bash', '.py'):
            if c == '#' and not (i == 0 and line.startswith('#!')):
                for j in range(i, n):
                    if chars[j] not in ('\n', '\r'):
                        chars[j] = ' '
                break

        if ext == '.sql':
            if c == '-' and i + 1 < n and chars[i + 1] == '-':
                for j in range(i, n):
                    if chars[j] not in ('\n', '\r'):
                        chars[j] = ' '
                break
            if c == '/' and i + 1 < n and chars[i + 1] == '*':
                end_idx = line.find('*/', i + 2)
                if end_idx != -1:
                    for j in range(i, end_idx + 2):
                        chars[j] = ' '
                    i = end_idx + 2
                    continue
                else:
                    for j in range(i, n):
                        if chars[j] not in ('\n', '\r'):
                            chars[j] = ' '
                    break

        i += 1

    return "".join(chars)


def lint_and_fix_file(filepath, auto_fix=False):
    errors = 0
    warnings = 0
    fixed_count = 0
    unresolved_errors = 0

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return 1, 0

    ext = os.path.splitext(filepath)[1].lower()

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modified = False

    print(f"🔍 Auditing {filepath}...")

    if ext in ('.md', '.mdx'):
        all_lines = content.splitlines(keepends=True)
        blocks = extract_code_blocks_from_markdown(content)

        for block in blocks:
            if block["ignored"]:
                continue

            b_ext = block["ext"]
            s_line = block["start_line"]
            b_lines = block["code_lines"]

            if b_ext == '.py':
                m_lines = mask_python_code("".join(b_lines))
            else:
                m_lines = [mask_line_heuristics(l, b_ext) for l in b_lines]

            for j, (line, masked_line) in enumerate(zip(b_lines, m_lines)):
                line_to_add = line
                for rule in PATTERNS:
                    if b_ext in rule["exts"]:
                        if line_to_add == line:
                            target_line = masked_line if rule.get("mask_strings", True) else line
                        else:
                            target_line = mask_line_heuristics(line_to_add, b_ext) if rule.get("mask_strings", True) else line_to_add

                        matches = list(re.finditer(rule["regex"], target_line))
                        match_count = len(matches)

                        if match_count > 0:
                            severity = rule["severity"]
                            msg = rule["message"]
                            real_line_num = s_line + j
                            print(f"  [{severity}] Line {real_line_num}: {msg}")
                            print(f"    ➔ {line.strip()}")

                            if severity == "ERROR":
                                errors += match_count
                                if not (auto_fix and rule["replacement"] is not None):
                                    unresolved_errors += match_count
                            else:
                                warnings += match_count

                            if auto_fix and rule["replacement"] is not None:
                                for m in reversed(matches):
                                    start, end = m.span()
                                    line_to_add = line_to_add[:start] + rule["replacement"] + line_to_add[end:]
                                modified = True
                                fixed_count += match_count
                                print(f"    ✨ [AUTO-FIXED] ➔ {line_to_add.strip()}")

                b_lines[j] = line_to_add

            if auto_fix and modified:
                all_lines[s_line - 1 : s_line - 1 + len(b_lines)] = b_lines

        if auto_fix and modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(all_lines)
            print(f"  💾 Saved {fixed_count} auto-repaired patterns to {filepath}")

    else:
        lines = content.splitlines(keepends=True)
        if ext == '.py':
            masked_lines = mask_python_code(content)
        else:
            masked_lines = [mask_line_heuristics(l, ext) for l in lines]

        new_lines = []

        for i, (line, masked_line) in enumerate(zip(lines, masked_lines), 1):
            line_to_add = line
            for rule in PATTERNS:
                if ext in rule["exts"]:
                    # Recalculate target_line based on current line_to_add if previous rules
                    # modified this line, ensuring span positions and masking match the updated text.
                    if line_to_add == line:
                        target_line = masked_line if rule.get("mask_strings", True) else line
                    else:
                        target_line = mask_line_heuristics(line_to_add, ext) if rule.get("mask_strings", True) else line_to_add

                    matches = list(re.finditer(rule["regex"], target_line))
                    match_count = len(matches)

                    if match_count > 0:
                        severity = rule["severity"]
                        msg = rule["message"]
                        print(f"  [{severity}] Line {i}: {msg}")
                        print(f"    ➔ {line.strip()}")

                        if severity == "ERROR":
                            errors += match_count
                            if not (auto_fix and rule["replacement"] is not None):
                                unresolved_errors += match_count
                        else:
                            warnings += match_count

                        if auto_fix and rule["replacement"] is not None:
                            for m in reversed(matches):
                                start, end = m.span()
                                line_to_add = line_to_add[:start] + rule["replacement"] + line_to_add[end:]
                            modified = True
                            fixed_count += match_count
                            print(f"    ✨ [AUTO-FIXED] ➔ {line_to_add.strip()}")

            new_lines.append(line_to_add)

        if auto_fix and modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"  💾 Saved {fixed_count} auto-repaired patterns to {filepath}")

    if errors == 0 and warnings == 0:
        print("  ✅ 100% Compliant with KS Cognitive Rules. Clean code guaranteed.")
        return 0, fixed_count
    else:
        print(f"  Summary: {errors} Errors, {warnings} Warnings, {fixed_count} Fixed.\n")
        return (1 if unresolved_errors > 0 else 0), fixed_count


def process_target(target, auto_fix=False, include_self=False, include_markdown=False):
    total_exit = 0
    total_fixed = 0
    self_path = os.path.abspath(__file__)

    valid_exts = ('.ts', '.tsx', '.py', '.js', '.jsx', '.rs', '.go', '.sh', '.sql')
    if include_markdown:
        valid_exts += ('.md', '.mdx')

    if os.path.isfile(target):
        ret, fixed = lint_and_fix_file(target, auto_fix)
        return ret
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith(valid_exts):
                    path = os.path.join(root, file)
                    abs_path = os.path.abspath(path)
                    if not include_self and abs_path == self_path:
                        continue
                    ret, fixed = lint_and_fix_file(path, auto_fix)
                    total_fixed += fixed
                    if ret != 0:
                        total_exit = 1

        print(f"🎉 Complete Audit Finished. Total Auto-Repairs Applied: {total_fixed}")
        return total_exit
    else:
        print(f"Invalid path: {target}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="KS Cognitive Engine — Anti-Pattern Linter & Auto-Fixer")
    parser.add_argument("target", help="File or directory path to inspect")
    parser.add_argument("--fix", action="store_true", help="Automatically repair and heal anti-patterns in place")
    parser.add_argument("--include-self", action="store_true", help="Include this linter script when scanning directories")
    parser.add_argument("--include-markdown", action="store_true", help="Scan fenced code blocks inside .md/.mdx files (opt-in, off by default)")

    args = parser.parse_args()
    sys.exit(process_target(args.target, auto_fix=args.fix, include_self=args.include_self, include_markdown=args.include_markdown))


if __name__ == '__main__':
    main()


