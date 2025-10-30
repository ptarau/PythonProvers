# Focused prover for the implicational fragment (atoms, and implications as (A,B))

from formulas import iFormula


# ---------- Encoding ----------
def is_imp(F):
    return isinstance(F, tuple) and len(F) == 2


def key_of(F):
    if is_imp(F):
        return ("imp", key_of(F[0]), key_of(F[1]))
    else:
        return ("atm", F)


def add_ctx(Gamma_key, K):
    """Idempotent add: contexts are sets (contraction)."""
    if K in Gamma_key:
        return Gamma_key
    return frozenset((*Gamma_key, K))


# ---------- Tabling with 3 states ----------
# memo[(G_key, Gamma_key)] ∈ {"IP", True, False}
_memo = {}


def jprove(G):
    """Provability from the empty context."""
    _memo.clear()
    return _prove_async(key_of(G), frozenset())


def prove(G, Gamma=()):
    """Provability from explicit Γ."""
    _memo.clear()
    Gamma_key = frozenset(key_of(F) for F in Gamma)
    return _prove_async(key_of(G), Gamma_key)


def _lookup(G_key, Gamma_key):
    return _memo.get((G_key, Gamma_key), None)


def _store(G_key, Gamma_key, val):
    _memo[(G_key, Gamma_key)] = val


# ---------- Focused kernel ----------
def _prove_async(G_key, Gamma_key):
    # Tabling: loop check
    st = _lookup(G_key, Gamma_key)
    if st is True:
        return True
    if st is False:
        return False
    if st == "IP":
        # We re-entered the same sequent while it's being proved: cut the loop.
        return False
    _store(G_key, Gamma_key, "IP")

    # Async (right) phase: peel implications on the right
    if isinstance(G_key, tuple) and G_key and G_key[0] == "imp":
        A_key, B_key = G_key[1], G_key[2]
        ok = _prove_async(B_key, add_ctx(Gamma_key, A_key))
        _store(G_key, Gamma_key, ok)
        return ok

    # Atomic goal: init?
    if G_key in Gamma_key:
        _store(G_key, Gamma_key, True)
        return True

    # Focus on a left implication A->B in Γ
    for V_key in Gamma_key:
        if isinstance(V_key, tuple) and V_key and V_key[0] == "imp":
            A_key, B_key = V_key[1], V_key[2]

            # Cycle-cut: focusing on (G -> B) immediately asks to prove G again
            if A_key == G_key:
                # This focus cannot help unless init already closed (handled above),
                # so skip it to avoid an immediate self-loop.
                continue

            # First subgoal: Γ ⊢ A  (async)
            if _prove_async(A_key, Gamma_key):
                # Second subgoal: Γ∪{B} ⊢ G
                if _prove_async(G_key, add_ctx(Gamma_key, B_key)):
                    _store(G_key, Gamma_key, True)
                    return True

    _store(G_key, Gamma_key, False)
    return False


def jtest(n):
    yes = 0
    no = 0
    for f in iFormula(n):
        ok = jprove(f)
        if ok:
            yes += 1
        else:
            no += 1
    return (yes, no, yes + no)


# ---------- Quick sanity tests ----------
if __name__ == "__main__":
    A, B, C = "A", "B", "C"
    Imp = lambda X, Y: (X, Y)

    print("⊢ A→(B→A):", jprove(Imp(A, Imp(B, A))))  # True
    print("A, A→B ⊢ B:", prove(B, (A, Imp(A, B))))  # True
    print("⊢ ((A→B)→A)→A:", jprove(Imp(Imp(Imp(A, B), A), A)))  # False (Peirce)
    print("⊢ A→((A→B)→B):", jprove(Imp(A, Imp(Imp(A, B), B))))  # True
    print(
        "⊢ A→((B→C)→((A→B)→C)):", jprove(Imp(A, Imp(Imp(B, C), Imp(Imp(A, B), C))))
    )  # True

    # A few tricky cycles that used to blow the stack:
    # Γ = {G -> B}, goal = G  should be False unless Γ already contains G
    G = "G"
    print("{G→B} ⊢ G:", prove(G, ((G, B),)))  # False
    print("{G} ⊢ G:", prove(G, (G,)))  # True
