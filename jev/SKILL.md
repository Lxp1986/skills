---
name: "jev"
description: "调用 TypeSafe Jev System-One 决策模型做结构化判断：Choice 选择、Score 打分、Noul 是非概率，附带置信度。用于消息分流、批量打分、Agent 工具路由等高频判断场景。"
---

# Jev 决策模型

## Purpose
Use Jev 决策模型 with the user-connected `custom.typesafe` credential.

## Tooling
`bin/jev.py` — call the Jev API with the stored credential (never a raw key):

    jev.py --state "message text" --preset urgency|triage [--model jev-1.13.0]
    jev.py --state "message text" --questions questions.json
    jev.py --state-file msg.txt --preset urgency

- `--preset urgency`: Score 0–3 (routine → critical) + Noul "needs Lin himself".
- `--preset triage`: Choice category (sales_lead/customer_service/finance/legal/internal/spam/other) + urgency Score + needs_human Noul.
- `--questions`: custom JSON. Each question: `{"type": "noul"|"choice"|"score", "instructions": "...", "criteria": ...}`.
  Choice criteria = map of option_id → description; Score criteria = ordered list of level descriptions; Noul criteria (optional) = `{"true": "...", "false": "..."}`.
- Preset instructions are in English (Jev is most accurate in English); `state` keeps the original language.
- Output: raw `answers` JSON plus a one-line summary per question with score/choice/probability and `confidence`.

Python CLIs must import `/opt/hatch/skills/skill-creator/bin/dynamic_credentials.py` and call `add_surrogate_to_request(...)`, `url_with_surrogate_query_param(...)`, or `url_with_surrogate_path_segment(...)` before authenticated requests, matching where the provider reads the key. If they use `urllib`, read JSON responses with `read_json_response(resp)` from the same helper instead of calling `resp.read()` directly. They must send only `hsurr:*` values, and only to the hosts below.

## Auth
The credential is already stored; nothing here collects one. Never ask the user to paste a raw key in chat, set a secret environment variable, pass a secret flag, or write an auth file.

A 401 or 403 is a question about the request before it is a question about the key. Check that the credential was attached at all: a request built without the helpers named under Tooling carries nothing, and that looks exactly like a wrong or under-scoped token. Only once a request that did carry the credential is still rejected, call `credentials.request_api_access` with `reconnect` to replace it. The connector is stored as `custom.typesafe`.

## Operating Rules
1. Use this skill when the user asks for Jev 决策模型 or this provider's API.
2. Restrict authenticated requests to: api.typesafe.ai.
3. Do not print, log, or persist raw credentials.
4. If auth is missing or rejected, follow the Auth section rather than asking for a key.
