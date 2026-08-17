# coding=utf-8

import unittest
from elifearticle import credit


class TestValidity(unittest.TestCase):
    "test CRediT terms used in mapping are valid"

    def test_credit_role_map_terms_are_list(self):
        "assert the terms in CREDIT_ROLE_MAP are a list"
        for phrase, terms in credit.CREDIT_ROLE_MAP.items():
            # assert terms is a list
            self.assertEqual(
                type(terms),
                list,
                f"in CREDIT_ROLE_MAP, terms for phrase '{phrase}' is not a list",
            )

    def test_valid_credit_role_map_terms(self):
        "assert the CRediT terms in CREDIT_ROLE_MAP are CRediT terms"
        for phrase, terms in credit.CREDIT_ROLE_MAP.items():
            # assert terms are all CRediT terms
            for term in terms:
                self.assertTrue(
                    term in credit.CREDIT_ROLES,
                    (
                        f"in CREDIT_ROLE_MAP, the term '{term}' for phrase '{phrase}'"
                        " does not match a value from CREDIT_ROLES"
                    ),
                )


class TestParseCreditRoles(unittest.TestCase):
    "tests for parse_credit_roles()"

    def test_parse_credit_roles(self):
        "test parsing contribution text for CRediT roles"
        passes = [
            {"text": "", "expected": set()},
            {
                "text": (
                    "YSJ, Conception and design, Acquisition of data, Analysis and"
                    " interpretation of data, Drafting or revising the article"
                ),
                "expected": set(),
            },
            {
                "text": ("Writing — review & editing"),
                "expected": set({"Writing - review & editing"}),
            },
            {
                "text": (
                    (
                        "Conceptualization, Resources, Data curation, Software, Formal analysis,"
                        " Supervision, Validation, Investigation, Visualization, Methodology,"
                        " Writing – original draft, Project administration, Writing – review and"
                        " editing, Wrote the code for the experimental setup, Funding acquisition"
                    )
                ),
                "expected": set(
                    {
                        "Conceptualization",
                        "Resources",
                        "Data curation",
                        "Software",
                        "Formal analysis",
                        "Supervision",
                        "Validation",
                        "Investigation",
                        "Visualization",
                        "Methodology",
                        "Writing - original draft",
                        "Project administration",
                        "Writing - review & editing",
                        "Funding acquisition",
                    }
                ),
            },
        ]
        for data in passes:
            result = credit.parse_credit_roles(data.get("text"))
            self.assertSetEqual(
                result,
                data.get("expected"),
                f"text '{data.get('text')}' did not matched expected value, got '{str(result)}'",
            )
