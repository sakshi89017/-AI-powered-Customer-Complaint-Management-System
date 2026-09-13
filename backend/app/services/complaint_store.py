"""
In-memory placeholder store for complaints.

Phase 1 uses a simple process-local dict so the API is fully functional
without a database. The public functions below (`list_all`, `get`,
`create`, `update`) are the seam the API layer depends on -- in the next
phase, replace the internals of this file with real PostgreSQL queries
(via app/db/session.py + app/models/complaint.py) and nothing in
app/api/complaints.py will need to change.
"""
from datetime import datetime
from itertools import count
from typing import Optional

from app.schemas.complaint import ComplaintCreate, ComplaintUpdate

_complaints: dict[int, dict] = {}
_id_counter = count(1)


def list_all() -> list[dict]:
    return list(_complaints.values())


def get(complaint_id: int) -> Optional[dict]:
    return _complaints.get(complaint_id)


def create(payload: ComplaintCreate) -> dict:
    new_id = next(_id_counter)
    now = datetime.utcnow()
    record = {
        "id": new_id,
        **payload.model_dump(),
        "createdAt": now,
        "updatedAt": now,
    }
    _complaints[new_id] = record
    return record


def update(complaint_id: int, payload: ComplaintUpdate) -> Optional[dict]:
    record = _complaints.get(complaint_id)
    if record is None:
        return None
    updates = payload.model_dump(exclude_unset=True)
    record.update(updates)
    record["updatedAt"] = datetime.utcnow()
    return record
