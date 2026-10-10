/-!
# The kernel-evaluated part of the certificate check (Lean core only, no Mathlib)

The certificate vector `V` is a ternary trie (`VTree`) indexed by the base-3 digits of the residue, least
significant first, so a lookup of a residue mod `3^r` takes exactly `r` steps. `classOk` tests one residue and
`allRange f n lo` tests `f lo, …, f (lo + n - 1)`. Everything is written with recursors (`VTree.rec`, `Nat.rec`,
`Bool.rec`) and the primitive operations `Nat.add`, `Nat.mul`, `Nat.div`, `Nat.mod`, `Nat.beq`, `Nat.ble`, which the
kernel evaluates on literals with GMP. Typeclass arithmetic and `cond`/`&&`/`||` would cost several unfoldings per
operation, and these choices make the kernel check roughly 6× faster. Soundness is in `PreimageBound.Check`.
-/

namespace PreimageBound

/-- Ternary trie of natural numbers. -/
inductive VTree where
  | leaf : Nat → VTree
  | node : VTree → VTree → VTree → VTree

/-- Lookup by base-3 digits, least significant first; a leaf answers every index that reaches it.
(`Bool.rec y x b` is `if b then x else y`.) -/
noncomputable def VTree.get (t : VTree) : Nat → Nat :=
  VTree.rec (motive := fun _ => Nat → Nat) (fun v _ => v)
    (fun _ _ _ f0 f1 f2 i =>
      Bool.rec (Bool.rec (f2 (Nat.div i 3)) (f1 (Nat.div i 3)) (Nat.beq (Nat.mod i 3) 1))
        (f0 (Nat.div i 3)) (Nat.beq (Nat.mod i 3) 0)) t

/-! Boolean connectives and `min` as single recursor applications. -/

noncomputable def bcond {α : Sort _} (b : Bool) (x y : α) : α := Bool.rec y x b
noncomputable def band (a b : Bool) : Bool := Bool.rec false b a
noncomputable def bor (a b : Bool) : Bool := Bool.rec b true a
noncomputable def bmin (a b : Nat) : Nat := Bool.rec b a (Nat.ble a b)

/-- The test for one residue `c`, with `M = 3^r` and `t = 3^(r-1)`: either `3 ∣ c`, or `Vmin ≤ V c ≤ Vmax` and
`P·V(c) ≤ Q·(V(2c mod M) + β(c)·min_u V(((2c-1)/3 + u·t) mod M))`, `β(c) = [c ≡ 2, 8 (mod 9)]`. -/
noncomputable def classOk (M t P Q Vmin Vmax : Nat) (V : Nat → Nat) (c : Nat) : Bool :=
  bcond (Nat.beq (Nat.mod c 3) 0) true
    (band (band (Nat.ble Vmin (V c)) (Nat.ble (V c) Vmax))
      (Nat.ble (Nat.mul P (V c))
        (Nat.mul Q (Nat.add (V (Nat.mod (Nat.mul 2 c) M))
          (bcond (bor (Nat.beq (Nat.mod c 9) 2) (Nat.beq (Nat.mod c 9) 8))
            (bmin (V (Nat.mod (Nat.div (Nat.sub (Nat.mul 2 c) 1) 3) M))
              (bmin (V (Nat.mod (Nat.add (Nat.div (Nat.sub (Nat.mul 2 c) 1) 3) t) M))
                (V (Nat.mod (Nat.add (Nat.div (Nat.sub (Nat.mul 2 c) 1) 3) (Nat.mul 2 t)) M))))
            0)))))

/-- `allRange f n lo = f lo && f (lo+1) && … && f (lo+n-1)`. -/
noncomputable def allRange (f : Nat → Bool) (n : Nat) : Nat → Bool :=
  Nat.rec (motive := fun _ => Nat → Bool) (fun _ => true)
    (fun _ ih lo => band (f lo) (ih (Nat.add lo 1))) n

end PreimageBound
