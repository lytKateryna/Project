import json
import os
import tempfile
import threading

CACHE_FILE = os.path.join(os.path.dirname(__file__), "poster_cache.json")
_lock = threading.Lock()
_cache: dict = {}


def _load_cache() -> None:
    global _cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                _cache = json.load(f)
        except Exception:
            _cache = {}
    else:
        _cache = {}


_load_cache()


def get(title: str) -> str | None:
    if not title:
        return None
    return _cache.get(title)


def set(title: str, url: str) -> None:
    if not title:
        return
    with _lock:
        _cache[title] = url
        try:
            dirpath = os.path.dirname(CACHE_FILE)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=dirpath)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(_cache, f, ensure_ascii=False, indent=2)
            os.replace(tmp, CACHE_FILE)
        except Exception as e:
            print("Poster cache write error:", e)
