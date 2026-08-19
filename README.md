# KS Cognitive Engine 🧠⚡

<p align="center">
  <img src="https://raw.githubusercontent.com/rbgroupsolutionsllc-eng/ks-cognitive-engine/master/assets/banner.png" alt="KS Cognitive Engine Banner" width="650" onerror="this.style.display='none'"/>
</p>

<p align="center">
  <a href="https://github.com/rbgroupsolutionsllc-eng/ks-cognitive-engine/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://github.com/rbgroupsolutionsllc-eng/ks-cognitive-engine"><img src="https://img.shields.io/badge/Version-3.5-green.svg" alt="Version 3.5"></a>
  <a href="https://github.com/rbgroupsolutionsllc-eng/ks-cognitive-engine"><img src="https://img.shields.io/badge/Skill-Universal%20Agent-purple.svg" alt="Universal Agent Skill"></a>
  <a href="https://github.com/rbgroupsolutionsllc-eng/ks-cognitive-engine/stargazers"><img src="https://img.shields.io/github/stars/rbgroupsolutionsllc-eng/ks-cognitive-engine?style=social" alt="Stars"></a>
</p>

<p align="center">
  <b>Universal Cognitive Engineering Protocol for AI Coding Agents.</b><br>
  Enforces OODA Loops, Strict Anti-Pattern Exclusions, Skeleton/Graph-of-Thoughts (DAG), Ambiguity Resolution, Polar Attention Anchors, and Reflexion Syntax Self-Healing natively inside any LLM.
</p>

---

## 🌟 Why KS Cognitive Engine?

Most AI coding assistants suffer from 5 chronic production defects:
1. **Sloppy Code & Anti-Patterns:** Spitting out `any` types in TypeScript, `except: pass` in Python, or mutating state in React.
2. **Analysis Paralysis / Rhetorical Stalling:** Asking 5 obvious questions before writing a single line of code for a simple prompt.
3. **Lost-in-the-Middle Context Amnesia:** Forgetting critical architectural constraints halfway through a long conversation.
4. **Truncated Code & Lazy Placeholders:** Leaving comments like `// TODO: implement rest` instead of working code.
5. **Conversational Fluff & Token Bloat:** Wasting context window budget on polite preamble instead of direct technical execution.

**KS Cognitive Engine** eliminates these failure modes by embedding proven **Cognitive Engineering Protocols** directly into the agent's reasoning loop—**without requiring external web scrapers or cloud proxies**.

---

## 🏛️ The 6 Cognitive Pillars

```
┌────────────────────────────────────────────────────────────────────────┐
│                      KS COGNITIVE REASONING PIPELINE                   │
├──────────────────────────────────┬─────────────────────────────────────┤
│ 1. OODA Loop & RED_FIRST         │ Observe context ➔ Orient with DSP ➔ │
│                                  │ Decide via DAG ➔ Act with Reflexion │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 2. Negative Prompting & Anti-Pat │ Strict stack-specific prohibitions  │
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

## 📦 Quick Installation

### Option 1: One-Line Install Script (Universal)
```bash
curl -fsSL https://raw.githubusercontent.com/rbgroupsolutionsllc-eng/ks-cognitive-engine/master/install.sh | bash
```

### Option 2: For Antigravity & Claude Code
Clone or link the skill into your global agents directory:
```bash
mkdir -p ~/.agents/skills/ks-cognitive-engine
curl -s https://raw.githubusercontent.com/rbgroupsolutionsllc-eng/ks-cognitive-engine/master/SKILL.md > ~/.agents/skills/ks-cognitive-engine/SKILL.md
```

### Option 3: For Cursor, Windsurf, Copilot or OpenCode
Include the skill rules in your project's `.cursorrules`, `AGENTS.md`, or System Prompt:
```markdown
# Load KS Cognitive Engine
Always adhere to the operational discipline and negative prompting rules defined in:
https://github.com/rbgroupsolutionsllc-eng/ks-cognitive-engine
```

---

## 🛠️ Stack-Specific Negative Prompting Filter

Whenever generating code, the agent enforces these strict prohibitions:

| Tech Stack | ❌ Strict Prohibitions (Negative Prompting) | ✅ Mandatory Clean Code Standard |
| :--- | :--- | :--- |
| **TypeScript / JS** | • No `any` types<br>• No unhandled promises<br>• No mutable state in React<br>• No synchronous I/O in Node | • Use `unknown`, generics, or strict Zod interfaces<br>• Explicit `try/catch` and error boundaries<br>• Immutable state updates (`useState`, `useReducer`)<br>• Async streams and non-blocking I/O |
| **Python** | • No `except: pass`<br>• No mutable default arguments (`items=[]`)<br>• No naked global state | • Structured logging (`logging.exception`)<br>• Default to `None` with internal initialization<br>• Clean encapsulation and dependency injection |
| **SQL / Databases** | • No string concatenation in queries (SQLi)<br>• No unconstrained `SELECT *` | • Parameterized queries / Prepared statements<br>• Explicit column projections with `LIMIT` |
| **Rust & Go** | • No `.unwrap()` in production paths<br>• No ignored errors (`_ = err`) | • Safe `Result` / `?` propagation<br>• Explicit error logging and bubbling |
| **Bash / Shell** | • No unquoted variables (`$VAR`)<br>• No scripts without safety headers | • Always quote expansions (`"$VAR"`)<br>• Mandatory `set -euo pipefail` |

---

## 📂 Repository Structure

```
ks-cognitive-engine/
├── .github/workflows/
│   └── auto_evolve_scout.yml         # Weekly GitHub Actions Self-Evolution Workflow
├── SKILL.md                          # Main Skill Definition (YAML Frontmatter + Directives)
├── README.md                         # Comprehensive Open-Source Documentation
├── CHANGELOG_EVOLUTION.md            # Autonomous Ecosystem Evolution Ledger
├── LICENSE                           # MIT License
├── install.sh                        # Automated Cross-Platform Installer
├── references/
│   ├── anti-patterns-catalog.md      # In-depth breakdown of banned anti-patterns
│   ├── cognitive-frameworks.md       # OODA, RED_FIRST, RED_TEAM, SoT & GoT guide
│   └── polar-anchors.md              # Lost-in-the-Middle and Token Economy guide
├── examples/
│   ├── typescript-antipatterns.md    # TypeScript Before vs After comparisons
│   ├── python-antipatterns.md        # Python Before vs After comparisons
│   ├── sql-antipatterns.md           # SQL Before vs After comparisons
│   ├── ambiguity-resolver.md         # Production default inference on short prompts
│   └── sot-got-architecture.md       # Full DAG decomposition of complex systems
└── scripts/
    ├── lint_cognitive_rules.py       # Anti-Pattern Linter & Auto-Fix Healing Engine
    ├── auto_scout_ecosystem.py       # Autonomous Weekly Ecosystem Scout
    └── sync_with_ks_sentinel.py      # Local KS Sentinel Bridge Synchronizer
```

---

## 🧬 Self-Evolution & Autonomous Healing Suite

Unlike static text prompts, **KS Cognitive Engine** is a **living, self-evolving intelligence protocol**:

### 1. 🛠️ Auto-Fix & Code Self-Healing (`--fix`)
Scan your workspace and automatically heal banned anti-patterns in place:
```bash
# Audit and auto-repair anti-patterns across your project
python3 scripts/lint_cognitive_rules.py ./src --fix
```

### 2. 🛰️ Autonomous Weekly Ecosystem Scout (GitHub Actions)
Every Sunday, our GitHub Actions workflow scans trending agent frameworks (`kaushikb11/awesome-llm-agents`) and updates [`CHANGELOG_EVOLUTION.md`](CHANGELOG_EVOLUTION.md) with newly discovered patterns.

### 3. 🔄 Run Evolution Scout Manually
```bash
python3 scripts/auto_scout_ecosystem.py
```

---

## 📄 License

This project is open-source under the **[MIT License](LICENSE)**.  
Crafted with precision by **RB Group Solutions LLC** & the **KS Server Engineering Team**.
