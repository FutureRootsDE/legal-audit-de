"""Offline tests for citation_check.classify."""
from __future__ import annotations

import unittest

import support  # noqa: F401  (puts scripts/ on sys.path)
from citation_check import classify, models


def make_citation(az="I ZR 159/24", court="BGH", covered=True, date=None, pending=False):
    return models.Citation(file="knowledge/themen/x.md", line=1, az=az, court=court,
                       covered=covered, date=date, pending=pending, context="")


def lookup_ok(*hits):
    return models.LookupResult(state="ok", hits=list(hits))


HIT = {"ecli": "ECLI:DE:BGH:2025:091025UIZR159.24.0", "date": "2025-10-09",
       "type": "Urteil", "document_number": "KORE726702025"}


class ClassificationTests(unittest.TestCase):
    def test_verified_when_date_matches(self):
        self.assertEqual(classify.classify(make_citation(date="2025-10-09"), lookup_ok(HIT)), "VERIFIED")

    def test_verified_when_kb_has_no_date(self):
        self.assertEqual(classify.classify(make_citation(), lookup_ok(HIT)), "VERIFIED")

    def test_date_mismatch(self):
        self.assertEqual(classify.classify(make_citation(date="2025-10-10"), lookup_ok(HIT)), "DATE_MISMATCH")

    def test_verified_if_date_matches_any_of_several_hits(self):
        beschluss = dict(HIT, date="2024-10-31", type="Beschluss", ecli="ECLI:X")
        self.assertEqual(
            classify.classify(make_citation(date="2024-10-31"), lookup_ok(HIT, beschluss)), "VERIFIED")

    def test_not_in_dataset(self):
        self.assertEqual(classify.classify(make_citation(), lookup_ok()), "NOT_IN_DATASET")

    def test_not_covered_never_needs_lookup(self):
        self.assertEqual(classify.classify(make_citation(court="OLG Hamburg", covered=False), None),
                         "NOT_COVERED")

    def test_error(self):
        res = models.LookupResult(state="error", hits=[], detail="HTTP 503")
        self.assertEqual(classify.classify(make_citation(), res), "ERROR")

    def test_unchecked_offline(self):
        res = models.LookupResult(state="unchecked", hits=[])
        self.assertEqual(classify.classify(make_citation(), res), "UNCHECKED")


if __name__ == "__main__":
    unittest.main()
