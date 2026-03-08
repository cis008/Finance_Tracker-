"""Anthropic-backed AI helpers with safe fallbacks.

All functions return fallback outputs when:
- `ANTHROPIC_API_KEY` is not configured
- `anthropic` package is not installed
- Anthropic API call fails
"""

from __future__ import annotations

import json
import os
import re
from typing import Optional


ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


def _get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        from anthropic import Anthropic
    except Exception:
        return None

    return Anthropic(api_key=api_key)


def anthropic_enabled() -> bool:
    return _get_client() is not None


def ai_categorize_description(description: str) -> Optional[dict]:
    """Categorize a transaction description via Anthropic.

    Returns dict with keys: category, icon, color, confidence
    or None if unavailable/failure.
    """
    if not description or len(description.strip()) < 3:
        return None

    client = _get_client()
    if client is None:
        return None

    prompt = (
        "Classify this finance transaction description into one concise category. "
        "Return STRICT JSON only with keys: category, icon, color, confidence. "
        "Use a relevant emoji icon and a hex color. "
        "Confidence must be a number between 0 and 1. "
        f"Description: {description.strip()}"
    )

    try:
        resp = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=220,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text if resp.content else ""
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                return None
            parsed = json.loads(match.group(0))

        category = str(parsed.get("category", "")).strip() or "Other"
        icon = str(parsed.get("icon", "📦")).strip() or "📦"
        color = str(parsed.get("color", "#94a3b8")).strip() or "#94a3b8"

        raw_conf = parsed.get("confidence", 0.5)
        try:
            confidence = float(raw_conf)
        except (TypeError, ValueError):
            confidence = 0.5
        confidence = max(0.0, min(1.0, confidence))

        return {
            "category": category,
            "icon": icon,
            "color": color,
            "confidence": round(confidence, 2),
        }
    except Exception:
        return None


def ai_financial_advice(question: str, summary: dict, breakdown: list, trend: list) -> Optional[str]:
    """Generate concise personal finance advice from current data.

    Returns markdown/plain text advice or None if unavailable/failure.
    """
    client = _get_client()
    if client is None:
        return None

    compact_context = {
        "summary": summary,
        "top_categories": breakdown[:6],
        "trend": trend,
    }

    prompt = (
        "You are a practical personal finance assistant. "
        "Use ONLY the provided data context. "
        "Give concise and actionable advice in 4-6 bullets. "
        "Mention specific numbers when useful. "
        "Do not invent data.\n\n"
        f"User question: {question or 'How can I improve my spending this month?'}\n\n"
        f"Data context (JSON): {json.dumps(compact_context)}"
    )

    try:
        resp = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=500,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text.strip() if resp.content else ""
        return text or None
    except Exception:
        return None
