#!/usr/bin/env python3
"""Call the TypeSafe Jev System-One decision model.

Reads the stored `custom.typesafe` credential through the authd surrogate
exchange -- the raw key never appears in this process.

Usage:
    jev.py --state "message text" --preset urgency
    jev.py --state "message text" --preset triage
    jev.py --state "message text" --questions questions.json
    jev.py --state-file msg.txt --preset urgency [--model jev-1.13.0]

questions.json format (per https://docs.typesafe.ai/primitives):
    {
      "qid": {"type": "noul", "instructions": "Is ...?"},
      "qid2": {"type": "choice", "instructions": "...",
               "criteria": {"opt_a": "description", "opt_b": "description"}},
      "qid3": {"type": "score", "instructions": "...",
               "criteria": ["level 0: ...", "level 1: ...", "level 2: ..."]}
    }

Output: the raw `answers` object as JSON, plus a one-line summary per question.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import (  # noqa: E402
    add_surrogate_to_request,
    read_json_response,
    DynamicCredentialError,
)

API_URL = "https://api.typesafe.ai/v1/systemone"
ALLOWED_HOSTS = ["api.typesafe.ai"]
CREDENTIAL_NAME = "custom.typesafe"
DEFAULT_MODEL = "jev-1.13.0"  # pinned; jev-latest floats between versions

URGENCY_LEVELS = [
    "0 - routine: greeting, FYI, or general inquiry. No action needed today.",
    "1 - follow-up: something to handle within a few days, no hard deadline.",
    "2 - important and time-bound: must be handled today or tomorrow.",
    "3 - critical: involves money loss, legal risk, or losing a key client/partner. Needs immediate attention.",
]

PRESETS = {
    "urgency": {
        "urgency": {
            "type": "score",
            "instructions": "How urgently does this message need handling?",
            "criteria": URGENCY_LEVELS,
        },
        "needs_human": {
            "type": "noul",
            "instructions": "Does this message need Lin himself to personally handle or reply, rather than an assistant or team member?",
        },
    },
    "triage": {
        "category": {
            "type": "choice",
            "instructions": "Which category does this message belong to?",
            "criteria": {
                "sales_lead": "a potential customer or business opportunity",
                "customer_service": "an existing customer needing help",
                "finance": "payments, invoices, debts, or money matters",
                "legal": "disputes, lawyers, courts, or contracts",
                "internal": "team members or internal operations",
                "spam": "advertising, scam, or irrelevant bulk message",
                "other": "none of the above",
            },
        },
        "urgency": {
            "type": "score",
            "instructions": "How urgently does this message need handling?",
            "criteria": URGENCY_LEVELS,
        },
        "needs_human": {
            "type": "noul",
            "instructions": "Does this message need Lin himself to personally handle or reply, rather than an assistant or team member?",
        },
    },
}


def call_jev(state, questions, model):
    payload = {"state": state, "model": model, "questions": questions}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    add_surrogate_to_request(
        req, CREDENTIAL_NAME, allowed_hosts=ALLOWED_HOSTS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", "replace")
        except Exception:
            body = "<unreadable>"
        raise SystemExit(f"Jev API error {exc.code}: {body[:500]}")


def summarize(answers):
    lines = []
    for qid, ans in answers.items():
        t = ans.get("type")
        if t == "noul":
            lines.append(f"[{qid}] noul={ans.get('noul')}")
        elif t == "choice":
            lines.append(
                f"[{qid}] choice={ans.get('choice')} "
                f"confidence={ans.get('confidence')}")
        elif t == "score":
            lines.append(
                f"[{qid}] score={ans.get('score')} "
                f"confidence={ans.get('confidence')}")
        else:
            lines.append(f"[{qid}] {json.dumps(ans, ensure_ascii=False)}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Call the Jev decision model.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--state", help="text to evaluate")
    src.add_argument("--state-file", help="file containing text to evaluate")
    q = ap.add_mutually_exclusive_group(required=True)
    q.add_argument("--questions", help="JSON file with questions object")
    q.add_argument("--preset", choices=list(PRESETS),
                   help="built-in question set")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    state = args.state
    if args.state_file:
        with open(args.state_file, encoding="utf-8") as f:
            state = f.read()

    if args.preset:
        questions = PRESETS[args.preset]
    else:
        with open(args.questions, encoding="utf-8") as f:
            questions = json.load(f)

    try:
        result = call_jev(state, questions, args.model)
    except DynamicCredentialError as exc:
        raise SystemExit(f"credential error: {exc}")

    answers = result.get("answers", result)
    print(json.dumps(answers, ensure_ascii=False, indent=2))
    print("---")
    print(summarize(answers))


if __name__ == "__main__":
    main()
