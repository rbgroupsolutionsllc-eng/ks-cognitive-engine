"""
Regression test suite for KS Cognitive Engine Anti-Pattern Linter & Auto-Fixer.
Verifies self-exclusion, comment/string awareness, and accurate fix counting.
"""

import os
import sys
import subprocess
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LINTER_SCRIPT = os.path.join(REPO_ROOT, "scripts", "lint_cognitive_rules.py")

# Ensure scripts directory is in sys.path to allow direct imports if needed
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
from lint_cognitive_rules import lint_and_fix_file, process_target


def test_self_exclusion_default():
    """
    Test 1: Scanning the repository root by default must exclude lint_cognitive_rules.py
    and must not report false positives from its internal message strings.
    """
    res = subprocess.run(
        [sys.executable, LINTER_SCRIPT, "."],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True
    )
    assert res.returncode == 0
    assert "Auditing ./scripts/lint_cognitive_rules.py" not in res.stdout
    assert "except: pass" not in res.stdout


def test_self_inclusion_flag():
    """
    Test 2: When --include-self flag is provided, lint_cognitive_rules.py is audited.
    With comment/string masking active, it should be parsed without false positives.
    """
    res = subprocess.run(
        [sys.executable, LINTER_SCRIPT, ".", "--include-self"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True
    )
    assert res.returncode == 0
    assert "Auditing ./scripts/lint_cognitive_rules.py" in res.stdout


def test_ignores_any_in_comment(tmp_path):
    """
    Test 3: TypeScript single-line and inline block comments containing ': any'
    must be ignored and must not produce errors.
    """
    ts_file = tmp_path / "comment_test.ts"
    ts_file.write_text("// comment: any type mentioned here\n/* block: any */\nconst a: number = 42;\n")

    exit_code, fixed_count = lint_and_fix_file(str(ts_file), auto_fix=False)
    assert exit_code == 0
    assert fixed_count == 0


def test_ignores_any_in_string(tmp_path):
    """
    Test 4: TypeScript strings (double, single, template literals) containing ': any'
    must not trigger false positive errors.
    """
    ts_file = tmp_path / "string_test.ts"
    content = (
        'const s1 = "has : any inside double quotes";\n'
        "const s2 = 'has : any inside single quotes';\n"
        "const s3 = `has : any inside template literal`;\n"
    )
    ts_file.write_text(content)

    exit_code, fixed_count = lint_and_fix_file(str(ts_file), auto_fix=False)
    assert exit_code == 0
    assert fixed_count == 0


def test_still_detects_real_any(tmp_path):
    """
    Test 5: Real TypeScript ': any' type annotations in code must still be detected as errors.
    """
    ts_file = tmp_path / "real_any.ts"
    ts_file.write_text("const x: any = {};\n")

    exit_code, fixed_count = lint_and_fix_file(str(ts_file), auto_fix=False)
    assert exit_code == 1
    assert fixed_count == 0


def test_fix_count_matches_occurrences(tmp_path):
    """
    Test 6: A line with multiple ': any' occurrences must report fixed_count matching
    the exact number of substitutions applied (e.g. 3, not 1).
    """
    ts_file = tmp_path / "multi_any.ts"
    ts_file.write_text("function calculate(x: any, y: any): any {\n  return x + y;\n}\n")

    exit_code, fixed_count = lint_and_fix_file(str(ts_file), auto_fix=True)
    assert exit_code == 0
    assert fixed_count == 3

    fixed_content = ts_file.read_text()
    assert fixed_content.count("unknown /* KS_COGNITIVE_FIX: replaced any with unknown */") == 3
    assert ": any" not in fixed_content


def test_ignores_except_pass_in_python_string_and_comment(tmp_path):
    """
    Test 7: Python strings and comments containing 'except: pass' must not generate false positives.
    """
    py_file = tmp_path / "py_comment_string.py"
    content = (
        '# This is a comment mentioning except: pass\n'
        'error_msg = "Python: Silent bare \'except: pass\' detected."\n'
        'try:\n'
        '    do_something()\n'
        'except ValueError:\n'
        '    pass\n'
    )
    py_file.write_text(content)

    exit_code, fixed_count = lint_and_fix_file(str(py_file), auto_fix=False)
    assert exit_code == 0
    assert fixed_count == 0


def test_still_detects_real_python_bare_except(tmp_path):
    """
    Test 8: Real Python bare except: pass must be detected and auto-repaired.
    """
    py_file = tmp_path / "py_bare_except.py"
    content = (
        'try:\n'
        '    do_something()\n'
        'except: pass\n'
    )
    py_file.write_text(content)

    exit_code, fixed_count = lint_and_fix_file(str(py_file), auto_fix=True)
    assert exit_code == 0
    assert fixed_count == 1
    fixed_content = py_file.read_text()
    assert "logging.exception" in fixed_content
    assert "except: pass" not in fixed_content


def test_exit_code_1_when_unfixable_error_remains(tmp_path):
    """
    Bug #1 regression: sql_concat has no auto-fix. Running --fix on a file
    with ONLY this violation must still exit 1, not silently report success.
    """
    ts_file = tmp_path / "sqli.ts"
    stmt = "SELECT * " "FROM users " "WHERE id = " "${userId}"
    ts_file.write_text(f"const q = `{stmt}`;\n")
    exit_code, fixed_count = lint_and_fix_file(str(ts_file), auto_fix=True)
    assert exit_code == 1
    assert fixed_count == 0  # nothing was auto-fixed


def test_exit_code_0_when_all_errors_fixed(tmp_path):
    """
    Regression guard: fixable errors resolved via --fix must still exit 0.
    """
    ts_file = tmp_path / "fixable.ts"
    ts_file.write_text('const x: any = {};\n')
    exit_code, fixed_count = lint_and_fix_file(str(ts_file), auto_fix=True)
    assert exit_code == 0
    assert fixed_count == 1


def test_exit_code_1_without_fix_flag_unchanged(tmp_path):
    """
    Regression guard: pre-existing behavior (no --fix at all) must be unchanged.
    """
    ts_file = tmp_path / "no_fix.ts"
    ts_file.write_text('const x: any = {};\n')
    exit_code, fixed_count = lint_and_fix_file(str(ts_file), auto_fix=False)
    assert exit_code == 1
    assert fixed_count == 0


def test_multi_rule_same_extension_does_not_corrupt_line(tmp_path, monkeypatch):
    """
    Bug #2 regression: if two auto-fixable rules apply to the same extension
    on the same line, the second rule's replacement must land at correct
    positions relative to the ALREADY modified line, not the original.
    """
    import lint_cognitive_rules as lcr

    # Temporarily inject a second synthetic rule for .ts to force the
    # multi-rule-same-extension scenario without touching production PATTERNS.
    synthetic_rule = {
        "id": "test_synthetic_foo",
        "regex": r'\bfoo\b',
        "replacement": "BAR",
        "message": "Test: synthetic rule for regression coverage.",
        "severity": "ERROR",
        "exts": ('.ts',),
        "mask_strings": True
    }
    original_patterns = lcr.PATTERNS.copy()
    monkeypatch.setattr(lcr, "PATTERNS", original_patterns + [synthetic_rule])

    ts_file = tmp_path / "multi_rule.ts"
    ts_file.write_text("const x: any = foo;\n")

    exit_code, fixed_count = lcr.lint_and_fix_file(str(ts_file), auto_fix=True)
    fixed_content = ts_file.read_text()

    assert "unknown /* KS_COGNITIVE_FIX: replaced any with unknown */" in fixed_content
    assert "BAR" in fixed_content
    assert fixed_count == 2
    # Critical: content must not be corrupted/truncated/duplicated
    assert fixed_content.count(";") == 1


def test_markdown_scan_disabled_by_default(tmp_path):
    """
    Feature must be strictly opt-in: scanning a directory without
    --include-markdown must not touch .md files at all, even if they
    contain real violations.
    """
    md_file = tmp_path / "bad_examples.md"
    md_file.write_text("```typescript\nconst x: any = {};\n```\n")
    exit_code = process_target(str(tmp_path), include_markdown=False)
    assert exit_code == 0


def test_markdown_extracts_and_detects_real_violation(tmp_path, capsys):
    """
    With markdown scanning enabled, a real violation inside a fenced
    ```typescript block must be detected, with correct line number
    reporting relative to the full .md file (not renumbered from 1).
    """
    md_content = (
        "# Some Doc\n"
        "\n"
        "Some prose here.\n"
        "\n"
        "```typescript\n"
        "const x: any = {};\n"
        "```\n"
    )
    md_file = tmp_path / "doc.md"
    md_file.write_text(md_content)
    exit_code, fixed_count = lint_and_fix_file(str(md_file), auto_fix=False)
    assert exit_code == 1
    assert fixed_count == 0
    captured = capsys.readouterr()
    assert "Line 6:" in captured.out


def test_markdown_ignore_marker_skips_block(tmp_path):
    """
    A fence preceded by <!-- ks-lint-ignore-next --> must be completely
    skipped, even though it contains a real, unambiguous violation.
    """
    md_content = (
        "<!-- ks-lint-ignore-next -->\n"
        "```typescript\n"
        "const x: any = {}; // intentional bad example for docs\n"
        "```\n"
    )
    md_file = tmp_path / "pedagogical.md"
    md_file.write_text(md_content)
    exit_code, fixed_count = lint_and_fix_file(str(md_file), auto_fix=False)
    assert exit_code == 0
    assert fixed_count == 0


def test_markdown_unknown_fence_lang_is_skipped(tmp_path):
    """
    Fences with unrecognized languages (e.g. ```json, ```yaml, ```mermaid)
    must not be analyzed and must not raise errors.
    """
    md_content = (
        "```json\n"
        '{"key": "value with : any inside a string"}\n'
        "```\n"
    )
    md_file = tmp_path / "json_block.md"
    md_file.write_text(md_content)
    exit_code, fixed_count = lint_and_fix_file(str(md_file), auto_fix=False)
    assert exit_code == 0
    assert fixed_count == 0


def test_markdown_autofix_preserves_surrounding_prose(tmp_path):
    """
    Running --fix on a .md file must only modify the code inside the
    fence, leaving all surrounding markdown prose, headers, and fence
    markers themselves completely untouched.
    """
    md_content = (
        "# Title\n"
        "\n"
        "Some explanation text.\n"
        "\n"
        "```typescript\n"
        "const x: any = {};\n"
        "```\n"
        "\n"
        "More text after.\n"
    )
    md_file = tmp_path / "autofix_doc.md"
    md_file.write_text(md_content)
    exit_code, fixed_count = lint_and_fix_file(str(md_file), auto_fix=True)
    assert exit_code == 0
    assert fixed_count == 1
    fixed_content = md_file.read_text()
    assert "# Title\n\nSome explanation text.\n\n```typescript\n" in fixed_content
    assert "const x: unknown /* KS_COGNITIVE_FIX: replaced any with unknown */ = {};\n" in fixed_content
    assert "```\n\nMore text after.\n" in fixed_content



