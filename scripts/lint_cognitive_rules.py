#!/usr/bin/env python3
"""
KS Cognitive Engine — Code & Anti-Pattern Linter
Scans codebases and files for banned anti-patterns defined in the KS Cognitive Specification.
"""

import sys
import re
import os

PATTERNS = [
    (r':\s*any\b', "TypeScript: Explicit 'any' type detected. Use 'unknown', generics, or explicit interface.", "ERROR"),
    (r'except\s*:\s*pass\b|except\s+Exception\s*:\s*pass\b', "Python: Silent bare 'except: pass' detected. Log or handle explicitly.", "ERROR"),
    (r'SELECT\s+.*\s+FROM\s+.*WHERE.*[\'"]\s*\+\s*\w+|`SELECT\s+.*FROM\s+.*WHERE.*\$\{', "SQL: Possible SQL string concatenation detected. Use parameterized queries.", "ERROR"),
    (r'\.unwrap\(\)', "Rust: Production '.unwrap()' detected. Use '?' or explicit error handling.", "WARNING"),
    (r'_\s*=\s*err\b', "Go: Ignored error variable detected.", "WARNING"),
]

def lint_file(filepath):
    errors = 0
    warnings = 0

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return 1

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    print(f"🔍 Linting {filepath} against KS Cognitive Rules...")

    for i, line in enumerate(lines, 1):
        for pattern, message, severity in PATTERNS:
            if re.search(pattern, line):
                print(f"  [{severity}] Line {i}: {message}")
                print(f"    ➔ {line.strip()}")
                if severity == "ERROR":
                    errors += 1
                else:
                    warnings += 1

    if errors == 0 and warnings == 0:
        print("  ✅ 100% Compliant with KS Cognitive Rules. No anti-patterns found.")
        return 0
    else:
        print(f"\n  Total Issues: {errors} Errors, {warnings} Warnings.")
        return 1 if errors > 0 else 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 lint_cognitive_rules.py <path_to_file_or_dir>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isfile(target):
        sys.exit(lint_file(target))
    elif os.path.isdir(target):
        total_ret = 0
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith(('.ts', '.tsx', '.py', '.js', '.jsx', '.rs', '.go', '.sql')):
                    ret = lint_file(os.path.join(root, file))
                    if ret != 0:
                        total_ret = 1
        sys.exit(total_ret)
