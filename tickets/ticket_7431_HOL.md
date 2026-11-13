# [HOL] Ticket 7431 -- HOL: Extract Reusable Arithmetic Tactics from Proof Blocks

**Repository:** `HOL`  
**Status:** `RESOLVED`  
**Resolved:** `2026-11-13T23:35:00Z`  
**Created:** `2026-10-27T22:48:44Z`  

## Task Description
Refactor repeated manual linear arithmetic tactic calls into centralized proof methods.

## Resolution Log
1. Extracted centralized arithmetic tactics and proof methods into `ArithTactics` module:
   - `src/num/arith/src/ArithTactics.sig`: Formal signature declaring reusable tactic and conversion identifiers (`ARITH_DISCH_TAC`, `LIN_ARITH_TAC`, `ASM_LIN_ARITH_TAC`, `DECIDE_TAC`, `DECIDE`, `ARITH_SOLVE_TAC`, `ARITH_BOUNDS_TAC`, `FAST_ARITH_TAC`, `PRESBURGER_TAC`, `ARITH_REDUCE_TAC`, `arith_ss`, `ARITH_ss`).
   - `src/num/arith/src/ArithTactics.sml`: Implemented robust proof methods for discharging arithmetic hypotheses, executing linear arithmetic decision procedures with propositional fallbacks, simplification with assumptions, and unified solver pipelines.
   - `src/num/arith/src/arithTacticsLib.sig` and `src/num/arith/src/arithTacticsLib.sml`: Added library wrappers for convenient structured theory imports.
2. Refactored repeated manual tactic definitions across formal theories:
   - Eliminated duplicated `fun DECIDE_TAC` blocks in `src/num/extra_theories/logrootScript.sml`, `src/num/extra_theories/gcdScript.sml`, and `src/bag/primeFactorScript.sml`.
   - Theories now use centralized arithmetic proof methods from `numLib` / `ArithTactics`.
3. Created automated test harness in `tests/test_hol_infrastructure.py` to verify tactic signatures, exported types, and absence of duplicated tactics across formal theories.
