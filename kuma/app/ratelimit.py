# -*- coding: utf-8 -*-
import time
from typing import Dict, Hashable


class Cooldown:
    def __init__(self, seconds: float):
        self.seconds = max(0.0, seconds)
        self._last: Dict[Hashable, float] = {}

    def ready(self, key: Hashable) -> bool:
        now = time.time()
        last = self._last.get(key, 0.0)
        if now - last >= self.seconds:
            self._last[key] = now
            return True
        return False
