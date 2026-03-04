from __future__ import annotations

import json
from typing import Iterable, Optional

from .controller import SelfCheckResult


def write_jsonl(path: str, ids: Iterable[str], results: Iterable[SelfCheckResult], ok: Optional[Iterable] = None) -> None:
    ok_list = list(ok) if ok is not None else None
    with open(path, "w", encoding="utf-8") as f:
        for i, (ex_id, r) in enumerate(zip(ids, results)):
            row = {
                "id": ex_id,
                "status": r.status,
                "action": r.action,
                "license_score": r.license_score,
                "meta": r.meta,
                "ok": ok_list[i] if ok_list is not None else "na",
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
