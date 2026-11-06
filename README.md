# Crownscribe open data

Small, dependency-free building blocks for Clash Royale tools, taken from [Crownscribe](https://crownscribe.com), a free stats site that tracks Ladder and Ranked battles from the official API.

- **Card names in 5 languages** (`data/cards.json`, `data/cards.csv`): every card by API id, with rarity, elixir, type, whether it has an Evolution or Hero form, and names in English, Simplified Chinese, Japanese, Korean and German.
- **Deck identity spec** (`SPEC.md`): one stable id for "the same 8 cards", and one for the same deck played with a different Evo / Hero choice.
- **Reference code** in Python (`python/`) and JavaScript (`js/`): deck hash, variant hash, building and parsing in-game *Copy deck* links.
- **Test vectors** (`test-vectors.json`) so ports in other languages can check themselves.

## Use it

Python 3.9+, standard library only:

```python
from crownscribe_deck import deck_hash, variant_hash, copy_deck_url, parse_copy_link

cards = [26000000, 26000001, 26000010, 26000014, 26000021, 27000000, 28000000, 28000011]
deck_hash(cards)                                   # same for any order of the 8 ids
variant_hash(cards, evo=[26000010], hero=[26000021])
link = copy_deck_url(cards, evo=[26000010])        # opens Clash Royale and copies the deck
parse_copy_link(link)                              # back to the 8 ids, in slot order
```

JavaScript (Node 18+, ES module):

```js
import { deckHash, variantHash, copyDeckUrl, parseCopyLink } from "./js/crownscribe-deck.mjs";
```

Run the tests:

```bash
cd python && python3 -m unittest
cd js && node --test test.mjs
```

The ids match Crownscribe's own: `https://crownscribe.com/decks/<deck_hash>` is the page for that deck.

## Card names: how reliable

| Language | Cards covered | Source |
|---|---|---|
| English | all | Official API |
| Simplified Chinese | all | Official in-game names |
| Korean | all but one | Official in-game names |
| Japanese | most | In-game names; not yet reviewed by a native speaker |
| German | about half | In-game names; not yet reviewed by a native speaker |

A missing name means we haven't confirmed it, not that the card has none. Corrections and missing names are welcome as pull requests or issues. Data as of 2026-11-06; new cards are added after release.

## License

Code and spec: MIT (see `LICENSE`).

Card names, card ids and other game data belong to Supercell. They are included as fan content under [Supercell's Fan Content Policy](https://supercell.com/en/fan-content-policy/): free to use, not for sale.

*This material is unofficial and is not endorsed by Supercell. For more information see Supercell's Fan Content Policy: www.supercell.com/fan-content-policy.*
