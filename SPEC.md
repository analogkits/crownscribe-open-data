# Deck identity spec

How Crownscribe turns a Clash Royale deck into a stable id. Any language that follows this spec gets the same ids; `test-vectors.json` checks it.

Card ids are the integers the official Clash Royale API uses (`26000000` = Knight). Troops start with `26`, buildings with `27`, spells with `28`; Tower Troops (`159…`) are never part of a deck.

## Deck hash

A deck is a set of **8 different cards**. Order does not matter.

```
payload   = the 8 card ids, sorted ascending as numbers, joined with ","
deck_hash = lowercase hex SHA-256 of payload (UTF-8)
```

Example payload: `26000000,26000001,26000010,26000014,26000021,27000000,28000000,28000011`.

Reject anything that is not exactly 8 different ids. Don't silently drop duplicates.

## Variant hash

Since the 2026-03 update a deck has an Evo slot, a Hero slot and a Wild slot (either). The same 8 cards with a different Evo / Hero choice are one deck but different **variants**.

```
payload      = "<8 ids, ascending, comma-joined>|evo:<evo ids, ascending, comma-joined>|hero:<hero ids, ascending, comma-joined>"
variant_hash = lowercase hex SHA-256 of payload (UTF-8)
```

- Empty lists keep their separator: `…|evo:|hero:`.
- It records **which cards are played as Evo or Hero**, not which slot holds them. An Evo in the Evo slot and the same Evo in the Wild slot are the same variant.
- The same card as Evo and as Hero gives different variants.
- Every Evo / Hero id must be one of the 8 cards.
- The Tower Troop is not part of the variant.

In the API, a card's `evolutionLevel` in a deck or battle says how it was played: bit 1 (`& 1`) = Evo, bit 2 (`& 2`) = Hero.

## Copy-to-game link

The game opens this link and offers to copy the deck:

```
https://link.clashroyale.com/en/?clashroyale://copyDeck?deck=<id>;<id>;…(8 ids)&l=Royals
```

The format is the one community tools have used for years. Supercell does not document it, so check it in the game after big updates.

Card order sets the slots: the first Evo goes first (Evo slot), the first Hero second (Hero slot), any further Evo / Hero next (Wild slot), then the remaining cards in their original order.
