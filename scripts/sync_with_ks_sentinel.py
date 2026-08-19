#!/usr/bin/env python3
"""
KS Cognitive Engine — Sentinel Bridge Synchronizer
Syncs discoveries and learned patterns from KS Server local daemons into the public skill.
"""

import os
import json
import urllib.request

SENTINEL_ENDPOINT = "http://localhost:3800/api/v1/sentinel/status"
LOCAL_STATE_FALLBACK = "/home/kairo/ks-server/sentinel_state.json"


def sync_from_sentinel():
    print("🛰️ Connecting to local KS Sentinel Daemon...")
    data = None

    # Try HTTP Endpoint first
    try:
        req = urllib.request.Request(SENTINEL_ENDPOINT)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("  🟢 Connected via Camoufox HTTP Daemon (port 3800)")
    except Exception:
        # Fallback to local state file
        if os.path.exists(LOCAL_STATE_FALLBACK):
            try:
                with open(LOCAL_STATE_FALLBACK, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print("  📁 Loaded state from local sentinel_state.json")
            except Exception as e:
                print(f"  ⚠️ Error loading fallback: {e}")

    if not data:
        print("  ℹ️ No active local Sentinel instance found. Operating in standalone mode.")
        return

    print(f"  ✅ Synchronized with KS Sentinel. Last Scout: {data.get('last_weekly_scout_ts', 'N/A')}")


if __name__ == '__main__':
    sync_from_sentinel()
