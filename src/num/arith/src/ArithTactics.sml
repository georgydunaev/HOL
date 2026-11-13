(* ===================================================================== *)
(* FILE          : ArithTactics.sml                                      *)
(* DESCRIPTION   : Centralized reusable arithmetic tactics and proof     *)
(*                 methods for linear arithmetic, decision procedures,   *)
(*                 and bounds reasoning in HOL4 theories.                *)
(* ===================================================================== *)

structure ArithTactics :> ArithTactics =
struct

  open HolKernel Parse boolLib simpLib boolSimps numSimps;

  val ARITH_ss = numSimps.ARITH_ss;
  val arith_ss = boolSimps.bool_ss ++ numSimps.ARITH_ss;

  (* Discharge all arithmetic hypotheses from assumption list into the goal *)
  fun ARITH_DISCH_TAC (g as (asl, _)) =
    MAP_EVERY UNDISCH_TAC (List.filter numSimps.is_arith_asm asl) g;

  (* Pure linear arithmetic decision tactic *)
  val LIN_ARITH_TAC : tactic =
    ARITH_DISCH_TAC THEN CONV_TAC Arith.ARITH_CONV;

  (* Linear arithmetic decision procedure with propositional fallback *)
  fun DECIDE_TAC (g as (asl, _)) =
    ((ARITH_DISCH_TAC THEN CONV_TAC Arith.ARITH_CONV)
     ORELSE tautLib.TAUT_TAC) g;

  (* Linear arithmetic conversion for deciding equalities and relations *)
  val DECIDE : conv = Drule.EQT_ELIM o Arith.ARITH_CONV;

  (* Linear arithmetic simplification incorporating goal assumptions *)
  val ASM_LIN_ARITH_TAC : tactic =
    FULL_SIMP_TAC (srw_ss() ++ numSimps.ARITH_ss) [] THEN DECIDE_TAC;

  (* Fast arithmetic decision tactic *)
  val FAST_ARITH_TAC : tactic =
    CONV_TAC Arith.ARITH_CONV ORELSE DECIDE_TAC;

  (* Arithmetic inequality bounds solver *)
  val ARITH_BOUNDS_TAC : tactic =
    ARITH_DISCH_TAC THEN
    REWRITE_TAC [arithmeticTheory.LESS_EQ_ADD, arithmeticTheory.LESS_EQ_0] THEN
    DECIDE_TAC;

  (* Presburger arithmetic decision procedure *)
  val PRESBURGER_TAC : tactic =
    DECIDE_TAC;

  (* Ground arithmetic reduction tactic *)
  val ARITH_REDUCE_TAC : tactic =
    CONV_TAC (simpLib.SIMP_CONV (boolSimps.bool_ss ++ numSimps.REDUCE_ss) []);

  (* Combined solver trying multiple centralized arithmetic proof methods *)
  val ARITH_SOLVE_TAC : tactic =
    FIRST [DECIDE_TAC, LIN_ARITH_TAC, FAST_ARITH_TAC, ASM_LIN_ARITH_TAC, ARITH_REDUCE_TAC];

end;
