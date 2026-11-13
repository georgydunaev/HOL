(* ===================================================================== *)
(* FILE          : ArithTactics.sig                                      *)
(* DESCRIPTION   : Centralized reusable arithmetic tactics and proof     *)
(*                 methods to eliminate duplicate proof scripts across   *)
(*                 formal HOL4 theories.                                 *)
(* ===================================================================== *)

signature ArithTactics =
sig
  include Abbrev

  val ARITH_DISCH_TAC     : tactic
  val LIN_ARITH_TAC       : tactic
  val ASM_LIN_ARITH_TAC   : tactic
  val DECIDE_TAC          : tactic
  val DECIDE              : conv
  val ARITH_SOLVE_TAC     : tactic
  val ARITH_BOUNDS_TAC    : tactic
  val FAST_ARITH_TAC      : tactic
  val PRESBURGER_TAC      : tactic
  val ARITH_REDUCE_TAC    : tactic

  val arith_ss            : simpLib.simpset
  val ARITH_ss            : simpLib.ssfrag
end
