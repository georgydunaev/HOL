#!/usr/bin/env python3
"""
Automated Test Harness for HOL4 Infrastructure.

Verifies:
1. Theory script syntax (*Script.sml).
2. Import declarations and structured theory dependencies.
3. Tactic signatures and centralized reusable proof methods.
4. Absence of deprecated structures, duplicated tactics, and hallucinated dependencies.
"""

import os
import re
import unittest

HOLDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def check_balanced_delimiters(content, filename=""):
    """
    Check that parentheses, brackets, and comments are balanced in Standard ML code.
    Ignores delimiters inside string literals and comment blocks.
    """
    i = 0
    n = len(content)
    paren_depth = 0
    bracket_depth = 0
    brace_depth = 0
    comment_depth = 0
    in_string = False

    while i < n:
        c = content[i]
        next_c = content[i + 1] if i + 1 < n else ""

        if comment_depth > 0:
            if c == "*" and next_c == ")":
                comment_depth -= 1
                i += 2
                continue
            elif c == "(" and next_c == "*":
                comment_depth += 1
                i += 2
                continue
            i += 1
            continue

        if in_string:
            if c == "\\":
                i += 2
                continue
            elif c == '"':
                in_string = False
            i += 1
            continue

        # Outside comments and strings
        if c == '"':
            in_string = True
            i += 1
            continue

        if c == "(" and next_c == "*":
            comment_depth += 1
            i += 2
            continue

        if c == "(":
            paren_depth += 1
        elif c == ")":
            paren_depth -= 1
            if paren_depth < 0:
                return False, f"Unmatched closing parenthesis ')' at character {i} in {filename}"
        elif c == "[":
            bracket_depth += 1
        elif c == "]":
            bracket_depth -= 1
            if bracket_depth < 0:
                return False, f"Unmatched closing bracket ']' at character {i} in {filename}"
        elif c == "{":
            brace_depth += 1
        elif c == "}":
            brace_depth -= 1
            if brace_depth < 0:
                return False, f"Unmatched closing brace '}}' at character {i} in {filename}"

        i += 1

    if comment_depth != 0:
        return False, f"Unclosed comment block (depth {comment_depth}) in {filename}"
    if paren_depth != 0:
        return False, f"Unbalanced parentheses (depth {paren_depth}) in {filename}"
    if bracket_depth != 0:
        return False, f"Unbalanced brackets (depth {bracket_depth}) in {filename}"
    if brace_depth != 0:
        return False, f"Unbalanced braces (depth {brace_depth}) in {filename}"

    return True, "Balanced"


class TestTheoryScriptSyntax(unittest.TestCase):
    """Verify syntax and structural completeness of HOL theory scripts."""

    def test_modernized_scripts_exist_and_balanced(self):
        scripts = [
            os.path.join(HOLDIR, "src", "num", "extra_theories", "logrootScript.sml"),
            os.path.join(HOLDIR, "src", "num", "extra_theories", "gcdScript.sml"),
            os.path.join(HOLDIR, "src", "bag", "primeFactorScript.sml"),
            os.path.join(HOLDIR, "src", "datatype", "ind_typeScript.sml"),
            os.path.join(HOLDIR, "src", "integer", "int_arithScript.sml"),
            os.path.join(HOLDIR, "src", "tactictoe", "examples", "ttt_demoScript.sml"),
            os.path.join(HOLDIR, "src", "num", "theories", "arithmeticScript.sml"),
            os.path.join(HOLDIR, "src", "boss", "bool_defsScript.sml"),
        ]
        for script_path in scripts:
            self.assertTrue(os.path.isfile(script_path), f"Script missing: {script_path}")
            with open(script_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            ok, msg = check_balanced_delimiters(content, script_path)
            self.assertTrue(ok, msg)

    def test_theory_lifecycle_markers(self):
        """Verify that theory scripts contain proper new_theory and export_theory calls."""
        scripts_to_check = [
            ("src/num/extra_theories/logrootScript.sml", "logroot"),
            ("src/num/extra_theories/gcdScript.sml", "gcd"),
            ("src/bag/primeFactorScript.sml", "primeFactor"),
            ("src/datatype/ind_typeScript.sml", "ind_type"),
            ("src/integer/int_arithScript.sml", "int_arith"),
            ("src/tactictoe/examples/ttt_demoScript.sml", "ttt_demo"),
        ]
        for rel_path, theory_name in scripts_to_check:
            path = os.path.join(HOLDIR, rel_path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(f'new_theory "{theory_name}"', content,
                          f"Expected new_theory \"{theory_name}\" in {rel_path}")
            self.assertIn("export_theory", content,
                          f"Expected export_theory in {rel_path}")


class TestImportDeclarations(unittest.TestCase):
    """Verify clean, structured theory dependencies and import declarations."""

    def test_logroot_imports(self):
        path = os.path.join(HOLDIR, "src", "num", "extra_theories", "logrootScript.sml")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check structured imports
        self.assertIn("open HolKernel Parse boolLib", content)
        self.assertIn("numLib", content)
        self.assertIn("arithmeticTheory", content)

        # Check absence of redundant duplicate open Parse
        lines = [line.strip() for line in content.splitlines()[:10]]
        parse_opens = [line for line in lines if line.startswith("open Parse")]
        self.assertEqual(len(parse_opens), 0, "Redundant 'open Parse' found in logrootScript.sml header")

    def test_gcd_imports_and_order(self):
        path = os.path.join(HOLDIR, "src", "num", "extra_theories", "gcdScript.sml")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("open HolKernel Parse boolLib", content)
        self.assertIn("numLib", content)
        self.assertIn("arithmeticTheory", content)

        # Ensure new_theory is declared before theorem stores or local tactics
        new_theory_pos = content.find('new_theory "gcd"')
        self.assertGreater(new_theory_pos, 0)
        self.assertLess(new_theory_pos, content.find("val arith_ss"))

    def test_prime_factor_imports(self):
        path = os.path.join(HOLDIR, "src", "bag", "primeFactorScript.sml")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("open HolKernel Parse boolLib bossLib", content)
        self.assertIn("numLib", content)
        self.assertIn("bagTheory", content)


class TestTacticSignatures(unittest.TestCase):
    """Verify signatures and centralized reusable arithmetic tactics."""

    def test_arith_tactics_signature_file(self):
        sig_path = os.path.join(HOLDIR, "src", "num", "arith", "src", "ArithTactics.sig")
        self.assertTrue(os.path.isfile(sig_path), f"ArithTactics.sig missing at {sig_path}")
        with open(sig_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("signature ArithTactics =", content)
        self.assertIn("val ARITH_DISCH_TAC     : tactic", content)
        self.assertIn("val LIN_ARITH_TAC       : tactic", content)
        self.assertIn("val ASM_LIN_ARITH_TAC   : tactic", content)
        self.assertIn("val DECIDE_TAC          : tactic", content)
        self.assertIn("val DECIDE              : conv", content)
        self.assertIn("val ARITH_SOLVE_TAC     : tactic", content)
        self.assertIn("val ARITH_BOUNDS_TAC    : tactic", content)
        self.assertIn("val FAST_ARITH_TAC      : tactic", content)
        self.assertIn("val PRESBURGER_TAC      : tactic", content)
        self.assertIn("val ARITH_REDUCE_TAC    : tactic", content)
        self.assertIn("val arith_ss            : simpLib.simpset", content)
        self.assertIn("val ARITH_ss            : simpLib.ssfrag", content)

    def test_arith_tactics_structure_file(self):
        sml_path = os.path.join(HOLDIR, "src", "num", "arith", "src", "ArithTactics.sml")
        self.assertTrue(os.path.isfile(sml_path), f"ArithTactics.sml missing at {sml_path}")
        with open(sml_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("structure ArithTactics :> ArithTactics =", content)
        self.assertIn("fun ARITH_DISCH_TAC", content)
        self.assertIn("val LIN_ARITH_TAC : tactic", content)
        self.assertIn("fun DECIDE_TAC", content)
        self.assertIn("val DECIDE : conv", content)
        self.assertIn("val ASM_LIN_ARITH_TAC : tactic", content)
        self.assertIn("val ARITH_SOLVE_TAC : tactic", content)
        self.assertIn("val ARITH_ss = numSimps.ARITH_ss", content)

        ok, msg = check_balanced_delimiters(content, sml_path)
        self.assertTrue(ok, msg)

    def test_arith_tactics_lib_wrappers(self):
        sig_path = os.path.join(HOLDIR, "src", "num", "arith", "src", "arithTacticsLib.sig")
        sml_path = os.path.join(HOLDIR, "src", "num", "arith", "src", "arithTacticsLib.sml")
        self.assertTrue(os.path.isfile(sig_path))
        self.assertTrue(os.path.isfile(sml_path))

        with open(sig_path, "r", encoding="utf-8") as f:
            self.assertIn("signature arithTacticsLib =", f.read())
        with open(sml_path, "r", encoding="utf-8") as f:
            self.assertIn("structure arithTacticsLib :> arithTacticsLib =", f.read())


class TestAbsenceOfDeprecatedStructures(unittest.TestCase):
    """Verify absence of deprecated theorem bindings, duplicated tactics, and invalid structures."""

    def test_absence_of_old_arith_ss_in_modernized_scripts(self):
        modernized = [
            "src/num/extra_theories/logrootScript.sml",
            "src/datatype/ind_typeScript.sml",
            "src/integer/int_arithScript.sml",
            "src/tactictoe/examples/ttt_demoScript.sml",
            "src/num/arith/src/ArithTactics.sml",
        ]
        for rel_path in modernized:
            path = os.path.join(HOLDIR, rel_path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("old_ARITH_ss", content,
                             f"Deprecated 'old_ARITH_ss' found in modernized script: {rel_path}")

    def test_absence_of_duplicated_decide_tac(self):
        modernized = [
            "src/num/extra_theories/logrootScript.sml",
            "src/num/extra_theories/gcdScript.sml",
            "src/bag/primeFactorScript.sml",
        ]
        for rel_path in modernized:
            path = os.path.join(HOLDIR, rel_path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("fun DECIDE_TAC", content,
                             f"Duplicated manual 'fun DECIDE_TAC' found in {rel_path}")

    def test_no_isabelle_dependencies_or_thy_files_in_tests(self):
        """Ensure adherence to Ticket 7807: HOL4 is SML, not Isabelle."""
        for root, dirs, files in os.walk(os.path.join(HOLDIR, "tests")):
            for file in files:
                self.assertFalse(file.endswith(".thy"),
                                 f"Found hallucinated Isabelle .thy file: {file}")

    def test_no_emojis_in_source_or_tests(self):
        """Absolute prohibition of emojis across modified and created infrastructure."""
        emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
            "\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
            "\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
            "\U00002702-\U000027B0\U000024C2-\U0001F251]"
        )
        files_to_check = [
            "src/num/arith/src/ArithTactics.sig",
            "src/num/arith/src/ArithTactics.sml",
            "src/num/arith/src/arithTacticsLib.sig",
            "src/num/arith/src/arithTacticsLib.sml",
            "src/num/extra_theories/logrootScript.sml",
            "src/num/extra_theories/gcdScript.sml",
            "src/bag/primeFactorScript.sml",
            "src/datatype/ind_typeScript.sml",
            "src/integer/int_arithScript.sml",
            "src/tactictoe/examples/ttt_demoScript.sml",
            "tests/test_hol_infrastructure.py",
        ]
        for rel_path in files_to_check:
            path = os.path.join(HOLDIR, rel_path)
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            match = emoji_pattern.search(content)
            self.assertIsNone(match, f"Forbidden emoji found in {rel_path}: {match.group(0) if match else ''}")


if __name__ == "__main__":
    unittest.main()
