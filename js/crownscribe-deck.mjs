// Clash Royale deck helpers: deck hash, variant hash and in-game copy links.
// Spec: ../SPEC.md. Test vectors: ../test-vectors.json. Node 18+ (node:crypto), no dependencies.

import { createHash } from "node:crypto";

export const COPY_DECK_BASE = "https://link.clashroyale.com/en/?clashroyale://copyDeck";
const DECK_PARAM = /deck=((?:\d{8,9}(?:;|%3B))+\d{8,9})/i;

const sha256 = (text) => createHash("sha256").update(text, "utf8").digest("hex");
const ascending = (ids) => [...new Set(ids.map(Number))].sort((a, b) => a - b);

function deckIds(cards) {
  const ids = ascending(cards);
  if (cards.length !== 8 || ids.length !== 8) {
    throw new RangeError(`a deck needs exactly 8 different cards, got ${JSON.stringify(cards)}`);
  }
  return ids;
}

/** SHA-256 of the 8 card ids, sorted ascending and comma-joined. */
export function deckHash(cards) {
  return sha256(deckIds(cards).join(","));
}

/** SHA-256 of `<ids>|evo:<evo ids>|hero:<hero ids>`, every list sorted ascending. */
export function variantHash(cards, evo = [], hero = []) {
  const ids = deckIds(cards);
  const evoIds = ascending(evo);
  const heroIds = ascending(hero);
  const outside = [...evoIds, ...heroIds].filter((id) => !ids.includes(id));
  if (outside.length) throw new RangeError(`Evo / Hero ids not in the deck: ${outside}`);
  return sha256(`${ids.join(",")}|evo:${evoIds.join(",")}|hero:${heroIds.join(",")}`);
}

/**
 * Link that opens Clash Royale and offers to copy the deck. Card order sets the slots:
 * first Evo → slot 1, first Hero → slot 2, further Evo / Hero → slot 3 (Wild), then the rest.
 */
export function copyDeckUrl(cards, evo = [], hero = []) {
  deckIds(cards);
  const evoIds = evo.filter((id) => cards.includes(id));
  const heroIds = hero.filter((id) => cards.includes(id) && !evoIds.includes(id));
  const slotted = [evoIds[0], heroIds[0], ...evoIds.slice(1), ...heroIds.slice(1)].filter((id) => id != null);
  const ordered = [...slotted, ...cards.filter((id) => !slotted.includes(id))];
  return `${COPY_DECK_BASE}?deck=${ordered.join(";")}&l=Royals`;
}

/** Card ids from an in-game copy link, in link order; null if there is no valid deck. */
export function parseCopyLink(text) {
  const m = DECK_PARAM.exec(text);
  if (!m) return null;
  const cards = m[1].split(/;|%3B/i).map(Number);
  return cards.length === 8 && new Set(cards).size === 8 ? cards : null;
}
