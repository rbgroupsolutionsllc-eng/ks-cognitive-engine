# Cognitive Reasoning Frameworks (OODA, SoT, GoT, PAL)

This document breaks down the cognitive architectures implemented in **KS Cognitive Engine**.

---

## 1. The OODA Loop (Observe, Orient, Decide, Act)

Adapted from military strategy to software engineering:

```
    ┌────────────┐
    │  OBSERVE   │ ──▶ Inspect workspace, open files, existing tests, errors
    └─────┬──────┘
          │
          ▼
    ┌────────────┐
    │   ORIENT   │ ──▶ Match stack (DSP), apply Anti-Patterns, check conventions
    └─────┬──────┘
          │
          ▼
    ┌────────────┐
    │   DECIDE   │ ──▶ Formulate plan using Skeleton/Graph-of-Thoughts DAG
    └─────┬──────┘
          │
          ▼
    ┌────────────┐
    │    ACT     │ ──▶ Write code, run tests, verify syntax with Reflexion Guard
    └────────────┘
```

---

## 2. Skeleton-of-Thought (SoT) & Graph-of-Thoughts (GoT)

* **Linear Chain-of-Thought (CoT)** often wanders in multi-file projects.
* **Skeleton-of-Thought (SoT)** forces the agent to write a structured skeleton of the architecture before filling in the implementation.
* **Graph-of-Thoughts (GoT)** represents complex multi-module systems as a Directed Acyclic Graph (DAG), resolving foundational dependencies first.

---

## 3. Ambiguity Resolver Protocol

When a user asks for a feature with an extremely brief prompt:
1. **Zero Rhetorical Stalling:** Do not ask *"What framework do you want to use?"* if the workspace already contains a `package.json` or `requirements.txt`.
2. **Autonomous Inference:** Adopt the dominant language and architecture of the repo.
3. **Enterprise Defaults:** If working from an empty directory, default to modern production standards (TypeScript, Next.js / FastAPI, Tailwind CSS, PostgreSQL).
