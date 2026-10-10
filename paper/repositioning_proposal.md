# Proposal: repositioning the preprint after the verified positive-density theorem (2026-10-10)

Status: proposal only. `paper/draft.md` is unchanged in its framing apart from the new §2.4, and this file is for
you to accept, change or reject.

## Why
`draft.md` leads with "we carry the computation to k = 22 and obtain π_a(x) ≥ x^γ, γ < 0.92509". Mazur's
formalisation of positive lower density (`notes/m2_audit.md`, verified overnight by a cold rebuild and
`leanchecker --fresh`) gives π_a(x) ≥ c_a x. As a statement about π_a for a fixed a, the x^γ record is therefore no
longer news, and a referee would say so.

Three things in the draft are not superseded, and they make a stronger paper:
1. **Theorem A** (structure of L^NT_k: attained, tight, unique, strictly increasing; machine-checked). It solves
   problems that Krasikov–Lagarias and Applegate–Lagarias left open.
2. **Uniform, explicit bounds.** Mazur's c_a is ineffective, and nothing in his argument is uniform in a. The K–L
   bounds hold for all a in a residue class at once, with explicit constants and small cutoffs. These are the best
   explicit lower bounds for π_a at any height one can write down:
   - 0.7146 (x/a)^{0.848} for x ≥ 2^{6.25} a;
   - 0.5681 (x/a)^{0.864} up to 2^{251};
   - then k = 22.
3. **The method's own limit.** The structure theorem makes λ_k an exact increasing sequence. The question
   lim λ_k = 2 is the *uniform* exponent question, since inf over a in a class of π*_a(2^y a), and that is still
   open. §6's analysis (ρ_k, mean-field, spectrum, 5x+1) is about exactly that.

## Suggested structure (title, abstract, sections)
**Title.** "The Krasikov–Lagarias method for 3x+1 predecessor counts: exact structure, certified computation to
k = 22, and explicit uniform bounds".

**Abstract.**
1. Theorem A, with Lean.
2. Certified λ_k brackets for k ≤ 22.
3. Explicit uniform bounds.
4. Analysis of the finite-level loss.
5. One sentence placing it relative to positive density: Mazur's ineffective result for each fixed a versus our
   explicit uniform-in-a bounds.

**Sections.**
- **§1 Introduction.** Rewrite the opening to state the landscape honestly:
  - K–L 2003;
  - formal positive density (Mazur 2026), with its constants and its lack of uniformity;
  - what remains: uniform exponents, explicit constants, the method's capacity.
- **§2 The system.** As now, with §2.4 (Theorem A) promoted to a main result, maybe its own section §3.
- **§3 Computation** and **§4 Certificates.** Unchanged, but present the γ values as "λ_k to 5 digits, certified
  brackets" rather than as records.
- **§5 Explicit uniform bounds** (new). Theorem 2.2 for all y ≥ 0, the lifted base case, and the envelope table
  from RESULTS.md. Correct the earlier 0.865 to the rigorous 0.8435 and add the k = 14/15 bounds.
- **§6 Formal verification.** Theorem A in Lean (no certificates); then the k = 18–20 native_decide instances, which
  are now mainly a demonstration of certificate checking at scale.
- **§7 The finite-level loss.** As now, framed as "does the method attain the uniform exponent 1?".
- **§8 What is established.** Update: Conjecture A (non-uniform) holds by Mazur; Collatz ⇔ P(1) has upper density 1
  (his Cor. 1.2); our results concern uniformity and the method.

## Alternative
Split the work:
1. Submit the short note `paper/monotone.md` (Theorem A + Lean) on its own. It is self-contained and clearly new.
2. Keep the long preprint as a technical report.

The short note is the fastest route to a publishable, uncontested result.
