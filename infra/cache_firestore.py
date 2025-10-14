# cache_firestore.py
import json, hashlib
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from google.cloud import firestore

class FirestoreCache:
    def __init__(self, collection: str, project='np-public-training'):
        self._col = firestore.Client(project=project).collection(collection)

    @staticmethod
    def make_key(prefix: str, payload: Dict[str, Any]) -> str:
        b = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return f"{prefix}:{hashlib.sha256(b).hexdigest()}"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        snap = self._col.document(key).get()
        if not snap.exists:
            return None
        d = snap.to_dict()
        exp = d.get("expireAt")
        if isinstance(exp, datetime) and exp.tzinfo and exp < datetime.now(timezone.utc):
            return None
        v = d.get("v")
        if not v:
            return None
        try:
            return json.loads(v)
        except Exception:
            return None

    def set(self, key: str, value: Dict[str, Any], ttl_days: int=5) -> None:
        self._col.document(key).set({
            "v": json.dumps(value, separators=(",", ":"), ensure_ascii=False),
            "expireAt": datetime.now(timezone.utc) + timedelta(days=max(ttl_days, 1)),
            "createdAt": firestore.SERVER_TIMESTAMP,
        })
