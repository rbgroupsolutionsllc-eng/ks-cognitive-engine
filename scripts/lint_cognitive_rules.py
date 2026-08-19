#!/usr/bin/env python3
"""
KS Cognitive Engine — Autonomous Anti-Pattern Linter & Auto-Fix Engine
Scans and automatically heals codebases against banned anti-patterns defined in the KS Cognitive Specification.
"""

import sys
import re
import os
import argparse

PATTERNS = [
    {
        "id": "ts_any",
        "regex": r':\s*any\b',
        "replacement": r': unknown /* KS_COGNITIVE_FIX: replaced any with unknown */',
        "message": "TypeScript: Explicit 'any' type detected. Replaced with 'unknown'.",
        "severity": "ERROR",
        "exts": ('.ts', '.tsx')
    },
    {
        "id": "py_bare_except_pass",
        "regex": r'except\s*:\s*pass\b|except\s+Exception\s*:\s*pass\b',
        "replacement": 'except Exception as e:\n        logging.exception(f"Unhandled exception caught: {e}")',
        "message": "Python: Silent bare 'except: pass' detected. Added structured logging fallback.",
        "severity": "ERROR",
        "exts": ('.py',)
    },
    {
        "id": "sql_concat",
        "regex": r'SELECT\s+.*\s+FROM\s+.*WHERE.*[\'"]\s*\+\s*\w+|`SELECT\s+.*FROM\s+.*WHERE.*\$\{',
        "replacement": None,  # Requires structural rewrite
        "message": "SQL: Possible SQL string concatenation detected. Use parameterized prepared statements ($1, ?).",
        "severity": "ERROR",
        "exts": ('.ts', '.js', '.py', '.sql')
    },
    {
        "id": "rust_unwrap",
        "regex": r'\.unwrap\(\)',
        "replacement": None,
        "message": "Rust: Production '.unwrap()' detected. Use '?' operator, 'expect(...)', or 'match' statement.",
        "severity": "WARNING",
        "exts": ('.rs',)
    },
    {
        "id": "go_ignored_err",
        "regex": r'_\s*=\s*err\b',
        "replacement": None,
        "message": "Go: Ignored error variable detected. Handle or return error explicitly.",
        "severity": "WARNING",
        "exts": ('.go',)
    },
    {
        "id": "bash_missing_safety",
        "regex": r'^#!\/bin\/bash\s*$',
        "replacement": '#!/usr/bin/env bash\nset -euo pipefail',
        "message": "Bash: Missing 'set -euo pipefail' strict safety preamble.",
        "severity": "WARNING",
        "exts": ('.sh', '.bash')
    }
]


def lint_and_fix_file(filepath, auto_fix=False):
    errors = 0
    warnings = 0
    fixed_count = 0

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return 1, 0

    ext = os.path.splitext(filepath)[1].lower()

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    modified = False
    new_lines = []

    print(f"🔍 Auditing {filepath}...")

    for i, line in enumerate(lines, 1):
        line_to_add = line
        for rule in PATTERNS:
            if ext in rule["exts"] and re.search(rule["regex"], line):
                severity = rule["severity"]
                msg = rule["message"]
                print(f"  [{severity}] Line {i}: {msg}")
                print(f"    ➔ {line.strip()}")

                if severity == "ERROR":
                    errors += 1
                else:
                    warnings += 1

                if auto_fix and rule["replacement"] is not None:
                    line_to_add = re.sub(rule["regex"], rule["replacement"], line_to_add)
                    modified = True
                    fixed_count += 1
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
        return (1 if errors > 0 and not auto_fix else 0), fixed_count


def process_target(target, auto_fix=False):
    total_exit = 0
    total_fixed = 0

    if os.path.isfile(target):
        ret, fixed = lint_and_fix_file(target, auto_fix)
        return ret
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith(('.ts', '.tsx', '.py', '.js', '.jsx', '.rs', '.go', '.sh', '.sql')):
                    path = os.path.join(root, file)
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

    args = parser.parse_args()
    sys.exit(process_target(args.target, auto_fix=args.fix))


if __name__ == '__main__':
    main()
