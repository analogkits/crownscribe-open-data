"""Clash Royale deck helpers: deck hash, variant hash and in-game copy links.

Spec: ../SPEC.md. Test vectors: ../test-vectors.json. Standard library only.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

__all__ = ["deck_hash", "variant_hash", "copy_deck_url", "parse_copy_link"]

COPY_DECK_BASE = "https://link.clashroyale.com/en/?clashroyale://copyDeck"
_DECK_PARAM = re.compile(r"deck=((?:\d{8,9}(?:;|%3B))+\d{8,9})", re.IGNORECASE)


def _deck_ids(card_ids: Iterable[int]) -> list[int]:
    raw = [int(c) for c in card_ids]
    ids = sorted(set(raw))
    if len(raw) != 8 or len(ids) != 8:
        raise ValueError(f"a deck needs exactly 8 different cards, got {raw}")
    return ids


def deck_hash(card_ids: Iterable[int]) -> str:
    """SHA-256 of the 8 card ids, sorted ascending and comma-joined."""
    payload = ",".join(map(str, _deck_ids(card_ids)))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def variant_hash(card_ids: Iterable[int], evo: Iterable[int] = (), hero: Iterable[int] = ()) -> str:
    """SHA-256 of `<ids>|evo:<evo ids>|hero:<hero ids>`, every list sorted ascending."""
    ids = _deck_ids(card_ids)
    evo_ids = sorted({int(c) for c in evo})
    hero_ids = sorted({int(c) for c in hero})
    outside = set(evo_ids + hero_ids) - set(ids)
    if outside:
        raise ValueError(f"Evo / Hero ids not in the deck: {sorted(outside)}")
    payload = (
        ",".join(map(str, ids))
        + "|evo:" + ",".join(map(str, evo_ids))
        + "|hero:" + ",".join(map(str, hero_ids))
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def copy_deck_url(card_ids: Iterable[int], evo: Iterable[int] = (), hero: Iterable[int] = ()) -> str:
    """Link that opens Clash Royale and offers to copy the deck.

    Card order sets the slots: the first Evo goes to slot 1, the first Hero to slot 2,
    any further Evo / Hero to slot 3 (the Wild slot), then the rest in the given order.
    """
    cards = [int(c) for c in card_ids]
    _deck_ids(cards)
    evo_ids = [int(c) for c in evo if int(c) in cards]
    hero_ids = [int(c) for c in hero if int(c) in cards and int(c) not in evo_ids]
    slotted = [*evo_ids[:1], *hero_ids[:1], *evo_ids[1:], *hero_ids[1:]]
    ordered = slotted + [c for c in cards if c not in slotted]
    return f"{COPY_DECK_BASE}?deck={';'.join(map(str, ordered))}&l=Royals"


def parse_copy_link(text: str) -> list[int] | None:
    """Card ids from an in-game copy link, in link order; None if there is no valid deck."""
    m = _DECK_PARAM.search(text)
    if not m:
        return None
    cards = [int(x) for x in re.split(r";|%3B", m.group(1), flags=re.IGNORECASE)]
    return cards if len(cards) == 8 and len(set(cards)) == 8 else None
