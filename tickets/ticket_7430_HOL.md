# [HOL] Ticket 7430 -- HOL: Modernize HOL Theory Imports and Signature Hierarchies

**Repository:** `HOL`  
**Status:** `RESOLVED`  
**Resolved:** `2026-11-13T23:35:00Z`  
**Created:** `2026-10-27T22:48:44Z`  

## Task Description
Update legacy HOL4 theory script dependencies to use structured theory imports in *Script.sml and eliminate deprecated theorem bindings.

## Resolution Log
1. Modernized theory script imports and dependencies across core and extra theory scripts:
   - `src/num/extra_theories/logrootScript.sml`: Cleaned header imports, removed duplicate `open Parse`, eliminated deprecated `numSimps.old_ARITH_ss` in favor of `numSimps.ARITH_ss`, and imported centralized arithmetic procedures via `numLib`.
   - `src/num/extra_theories/gcdScript.sml`: Restructured theory dependencies to declare `new_theory "gcd"` at the top of the specification block and replaced inline tactic copies with centralized `numLib.DECIDE` and `numLib.DECIDE_TAC`.
   - `src/bag/primeFactorScript.sml`: Modernized structured imports to include `numLib`, eliminating manual reimplementations of `DECIDE_TAC`.
   - `src/datatype/ind_typeScript.sml`: Modernized simpset declarations, replacing deprecated `numSimps.old_ARITH_ss` with `numSimps.ARITH_ss`.
   - `src/integer/int_arithScript.sml`: Upgraded `arith_ss` binding from deprecated `old_ARITH_ss` to modern `ARITH_ss`.
   - `src/tactictoe/examples/ttt_demoScript.sml`: Replaced deprecated `old_ARITH_ss` with `ARITH_ss` and resolved unmatched delimiter syntax error in list tactic application.
2. Verified all modernized scripts preserve clean Standard ML syntax and lifecycle invariants (`new_theory` and `export_theory`).
3. Automated test harness in `tests/test_hol_infrastructure.py` validates theory script syntax, import declarations, and absence of deprecated structures.
