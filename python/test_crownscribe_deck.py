import json
import unittest
from pathlib import Path

from crownscribe_deck import copy_deck_url, deck_hash, parse_copy_link, variant_hash

VECTORS = json.loads((Path(__file__).parent.parent / "test-vectors.json").read_text())


class Vectors(unittest.TestCase):
    def test_deck_hash(self) -> None:
        for v in VECTORS["deck_hash"]:
            self.assertEqual(deck_hash(v["cards"]), v["expected"])

    def test_variant_hash(self) -> None:
        for v in VECTORS["variant_hash"]:
            self.assertEqual(variant_hash(v["cards"], v["evo"], v["hero"]), v["expected"])

    def test_copy_link_round_trip(self) -> None:
        for v in VECTORS["copy_deck_url"]:
            self.assertEqual(copy_deck_url(v["cards"], v["evo"], v["hero"]), v["expected"])
            self.assertEqual(sorted(parse_copy_link(v["expected"])), sorted(v["cards"]))

    def test_invalid_decks(self) -> None:
        for cards in VECTORS["invalid_decks"]:
            with self.assertRaises(ValueError):
                deck_hash(cards)


if __name__ == "__main__":
    unittest.main()
