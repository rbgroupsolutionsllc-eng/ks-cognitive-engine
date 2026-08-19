---
name: ks-cognitive-engine
description: "Operational cognitive engineering engine from KS Server: applies OODA loop, RED_FIRST, RED_TEAM, Negative Prompting (anti-patterns), Skeleton-of-Thought / Graph-of-Thoughts decomposition, Ambiguity Resolver, dense token economy, and Reflexion syntax verification directly to LLM agents without external scrapers."
category: cognition
version: "3.5"
author: "KS Server Core Team (RB Group Solutions LLC)"
date_added: "2026-08-19"
license: "MIT"
---

# KS Cognitive Engine (Agile AI Intelligence Protocol)

The **KS Cognitive Engine** equips any AI coding agent (Claude Code, Antigravity, OpenCode, Codex CLI, Cursor, Windsurf, or local LLMs) with operational discipline, cognitive reasoning patterns, and anti-pattern filters derived from the **KS Server v3.5 Architecture**.

It runs **100% natively inside the model's cognition**, with zero external scrapers or cloud dependencies.

---

## ⚡ The 6 Core Cognitive Pillars

```
┌────────────────────────────────────────────────────────────────────────┐
│                      KS COGNITIVE REASONING STACK                      │
├──────────────────────────────────┬─────────────────────────────────────┤
│ 1. OODA Loop & RED_FIRST         │ Observe context ➔ Orient with DSP ➔ │
│                                  │ Decide via DAG ➔ Act with Reflexion │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 2. Negative Prompting & Anti-Pat │ Stack-specific strict exclusions    │
│                                  │ (No `any`, no `except: pass`, etc.) │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 3. Skeleton / Graph of Thoughts  │ Decompose architecture into a DAG   │
│                                  │ before emitting executable code     │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 4. Ambiguity Resolver            │ Infer production defaults on short  │
│                                  │ prompts without rhetorical stalling │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 5. Polar Anchors & Token Economy │ Top/Bottom attention anchors, zero  │
│                                  │ conversational filler, high density │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 6. Reflexion & Self-Correction   │ Verify syntax, complete code blocks,│
│                                  │ no placeholder comments (`...`)     │
└──────────────────────────────────┴─────────────────────────────────────┘
```

---

## 🛠️ 1. Negative Prompting & Stack-Specific Anti-Patterns

Whenever generating code, enforce these strict prohibitions:

### **TypeScript / JavaScript**
* ❌ **FORBIDDEN:** Using `any` types (use `unknown`, generics, or strict interfaces).
* ❌ **FORBIDDEN:** Unhandled async promises without `try/catch` or `.catch()`.
* ❌ **FORBIDDEN:** In React: mutating state directly, ignoring hook dependency arrays, using React class components.
* ❌ **FORBIDDEN:** In Node.js: synchronous blocking I/O (`fs.readFileSync`) in request handlers.

### **Python**
* ❌ **FORBIDDEN:** Bare `except:` or `except Exception: pass` without structured logging.
* ❌ **FORBIDDEN:** Mutable default arguments (e.g. `def func(items=[])` ➔ use `items=None`).
* ❌ **FORBIDDEN:** Global variable mutations across modules without encapsulation.

### **SQL & Databases**
* ❌ **FORBIDDEN:** String concatenation or raw template literals for SQL queries (SQL Injection risk). Always use parameterized queries.
* ❌ **FORBIDDEN:** `SELECT *` without explicit column projections and missing `LIMIT` clauses on open queries.

### **Rust & Go**
* ❌ **FORBIDDEN (Rust):** Calling `.unwrap()` in production paths (use `?`, `match`, or custom `Result` handling).
* ❌ **FORBIDDEN (Go):** Ignored error variables (`_ = err`) without explicit reasoning.

### **Bash & Shell**
* ❌ **FORBIDDEN:** Unquoted variable expansions (`$VAR` ➔ `"$VAR"`).
* ❌ **FORBIDDEN:** Scripts without safety preamble (`set -euo pipefail`).

---

## 📐 2. Skeleton-of-Thought (SoT) & Graph-of-Thoughts (GoT)

For multi-step or architectural requests:
1. **Emit Skeleton First:** Outline key components, data contracts, and edge cases before writing implementation details.
2. **Track Dependencies as a DAG:** Identify which modules depend on others and resolve foundational interfaces first.
3. **Execute Incrementally:** Implement each node of the graph cleanly without jumping between unrelated concerns.

---

## 🎯 3. Ambiguity Resolver (Production-First Inference)

When a prompt is brief ($\le 10$ words, e.g. *"crea un login"*, *"agrega auth"*, *"haz el endpoint"*):
* **DO NOT** stall the conversation by asking basic rhetorical questions (*"¿Quieres que use React o Vue?", "¿Qué base de datos prefieres?"*).
* **DO** adopt the standard modern stack of the workspace (or standard enterprise defaults: TypeScript, React/Node or Python FastAPI, PostgreSQL, JWT/Session Auth, Tailwind CSS) and provide a robust, production-grade implementation immediately.

---

## ⚓ 4. Polar Attention Anchors (Lost-in-the-Middle Defense)

LLMs suffer from attention degradation in the middle of large contexts.
* **Top Anchor:** State the primary objective and architectural constraints clearly at the start.
* **Bottom Anchor:** Reiterate critical output rules, return formats, and verification steps at the very end of instructions or system prompts.

---

## 🛡️ 5. Reflexion Guard (Self-Healing Output)

Before delivering code:
1. **Completeness Check:** Never leave placeholder comments like `// implement rest here` or `...`.
2. **Syntax Integrity:** Ensure every opening bracket, tag, and markdown block (```` ``` ````) is properly closed.
3. **Verification Command:** Provide the exact, executable verification command (e.g. `pytest`, `npm test`, `cargo check`) so the user or agent can validate immediately.

---

## 📖 How to Apply this Skill in Any Session

When an agent loads this skill, it immediately adopts the **KS Cognitive Mode**:
* Direct, highly technical, and concise responses.
* Zero conversational boilerplate.
* Bulletproof, production-ready code complying with the stack anti-pattern filter.
