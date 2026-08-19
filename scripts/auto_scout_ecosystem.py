#!/usr/bin/env python3
"""
KS Cognitive Engine — Autonomous Ecosystem Scout & Rule Evolution Engine
Fetches weekly agent intelligence from curated sources and updates the local evolution ledger.
"""

import urllib.request
import json
import re
import time
import os

SOURCES = [
    {
        "name": "Awesome LLM Agents",
        "url": "https://raw.githubusercontent.com/kaushikb11/awesome-llm-agents/main/README.md"
    }
]

CHANGELOG_FILE = "CHANGELOG_EVOLUTION.md"


def fetch_latest_discoveries():
    discoveries = []
    for src in SOURCES:
        try:
            req = urllib.request.Request(src["url"], headers={"User-Agent": "ks-cognitive-evolution-bot"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                content = resp.read().decode("utf-8")

            # Extract table items
            pattern = re.compile(r'\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([\d,]+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|')
            matches = pattern.findall(content)

            for name, url, stars, lang, lic, updated, desc in matches:
                updated_clean = updated.strip()
                if any(x in updated_clean for x in ["2026-08", "2026-07", "2026-09"]):
                    discoveries.append({
                        "name": name.strip(),
                        "url": url.strip(),
                        "stars": stars.strip(),
                        "desc": desc.strip(),
                        "updated": updated_clean
                    })
        except Exception as e:
            print(f"Error fetching from {src['name']}: {e}")

    return discoveries


def update_evolution_changelog(discoveries):
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S UTC")
    header = f"## 🛰️ Autonomous Evolution Cycle — {timestamp_str}\n\n"
    
    if not discoveries:
        body = "_Ecosistema estable: no se detectaron nuevos frameworks disruptivos en este ciclo._\n\n"
    else:
        body = "### 🌟 Nuevos Descubrimientos & Frameworks Activos:\n"
        for d in discoveries[:5]:
            body += f"- **[{d['name']}]({d['url']})** (`{d['stars']}★`): {d['desc']} *(Actualizado: {d['updated']})*\n"
        body += "\n"

    new_content = header + body

    if os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            old_content = f.read()
    else:
        old_content = "# KS Cognitive Engine — Autonomous Evolution Ledger\n\n"

    full_text = old_content.replace("# KS Cognitive Engine — Autonomous Evolution Ledger\n\n", "# KS Cognitive Engine — Autonomous Evolution Ledger\n\n" + new_content)
    if full_text == old_content:
        full_text = "# KS Cognitive Engine — Autonomous Evolution Ledger\n\n" + new_content + old_content

    with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ Evolution Ledger updated in {CHANGELOG_FILE} with {len(discoveries)} discoveries.")
    return len(discoveries)


def main():
    print("🚀 Running Autonomous Ecosystem Scout...")
    discoveries = fetch_latest_discoveries()
    count = update_evolution_changelog(discoveries)
    print(f"🎉 Scout cycle completed successfully with {count} items.")


if __name__ == '__main__':
    main()
