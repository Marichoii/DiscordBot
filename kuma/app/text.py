# -*- coding: utf-8 -*-
import re
from typing import List


_WHITESPACE_RE = re.compile(r"\s+")
_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9']+")


def normalize(text: str) -> str:
    cleaned = text.strip().lower()
    return _WHITESPACE_RE.sub(" ", cleaned)


def tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall(text.lower())
