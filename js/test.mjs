import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { copyDeckUrl, deckHash, parseCopyLink, variantHash } from "./crownscribe-deck.mjs";

const vectors = JSON.parse(readFileSync(new URL("../test-vectors.json", import.meta.url)));

test("deck hash vectors", () => {
  for (const v of vectors.deck_hash) assert.equal(deckHash(v.cards), v.expected);
});

test("variant hash vectors", () => {
  for (const v of vectors.variant_hash) assert.equal(variantHash(v.cards, v.evo, v.hero), v.expected);
});

test("copy link vectors round-trip", () => {
  for (const v of vectors.copy_deck_url) {
    assert.equal(copyDeckUrl(v.cards, v.evo, v.hero), v.expected);
    assert.deepEqual([...parseCopyLink(v.expected)].sort(), [...v.cards].sort());
  }
});

test("invalid decks are rejected", () => {
  for (const cards of vectors.invalid_decks) assert.throws(() => deckHash(cards), RangeError);
});
