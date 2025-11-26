"""
PARC Reference Engine (Python)
UTF-PARC 1.0 Compatible
Author: Your Name
License: MIT

This file provides:
- parc_vector(text): produce a UTF-PARC cognitive state vector
- clamp(x): ensure values fall in [0, 1]
- normalize(c, m, f, k): enforce UTF-PARC constraints
- parc_update(c, m, f, k): optional iterative update (PARC dynamics)

This implementation intentionally uses a simple heuristic model so that it
runs anywhere with zero dependencies. You can replace encode_text() with
an embedding model, classifier, or domain-specific logic.
"""

import math
import random


# -----------------------------
# Utility Functions
# -----------------------------
def clamp(x: float) -> float:
    """Clamp a float to [0, 1]."""
    return max(0.0, min(1.0, float(x)))


# -----------------------------
# Heuristic Encoding Layer
# -----------------------------
def encode_text(text: str):
    """
    Convert text into initial (c0, m0, f0, k0) seeds.
    This is the only part you'd swap out for a real model.

    Current heuristic:
    - correctness increases with definitional markers ("is", "means", "because")
    - misconception increases with negation or contradiction markers
    - confidence is partly random but anchored
    - fog is derived during normalization (UTF-PARC rule)
    """

    t = text.lower().strip()

    # word lists (simple placeholders)
    correct_words = ["is", "are", "means", "because"]
    mis_words = ["not", "never", "wrong", "unless"]

    tokens = t.split()
    length = max(1, len(tokens))

    # Very rough signals
    c0 = sum(1 for w in tokens if w in correct_words) / length
    m0 = sum(1 for w in tokens if w in mis_words) / length

    # raw fog (will be replaced later by UTF-PARC rule)
    f0 = 1 - max(c0, m0)

    # semi-randomized confidence with meaningful drift
    k0 = 0.3 + 0.7 * random.random()

    return float(c0), float(m0), float(f0), float(k0)


# -----------------------------
# UTF-PARC Normalization
# -----------------------------
def normalize(c0, m0, f0, k0):
    """
    Enforce UTF-PARC 1.0 constraints:
      - clamp all values
      - normalize c + m ≤ 1
      - recompute f = 1 - max(c, m)
      - return (c, m, f, k)
    """

    # clamp first
    c = clamp(c0)
    m = clamp(m0)
    k = clamp(k0)

    # enforce c + m ≤ 1
    total = c + m
    if total > 1.0:
        c = c / total
        m = m / total

    # UTF-PARC fog rule
    f = 1.0 - max(c, m)

    return c, m, f, k


# -----------------------------
# Optional: PARC Temporal Update
# -----------------------------
def parc_update(c, m, f, k, gamma=0.3, delta=0.1, beta=0.5, rho=0.5, steps=3):
    """
    Apply PARC dynamical update equations.
    Used when tracking learner reasoning over time.
    """

    for _ in range(steps):

        gamma_eff = gamma * (1 - m)
        delta_eff = delta + beta * c

        # update correctness + misconception
        c_new = c + gamma_eff * (1 - c - m)
        m_new = m * (1 - delta_eff)

        # renormalize if needed
        if c_new + m_new > 1:
            total = c_new + m_new
            c_new /= total
            m_new /= total
            f_new = 0.0
        else:
            f_new = 1.0 - max(c_new, m_new)

        # confidence follows c - m
        k_new = k + rho * (c_new - m_new - k)

        c, m, f, k = c_new, m_new, f_new, k_new

    return c, m, f, k


# -----------------------------
# Public API
# -----------------------------
def parc_vector(text: str, apply_updates=True):
    """
    Produce the final UTF-PARC 1.0 vector for a given text.
    Steps:
      1. Encode via heuristic (or custom model)
      2. Normalize per UTF-PARC spec
      3. Optionally apply PARC update equations
    """

    c0, m0, f0, k0 = encode_text(text)
    c, m, f, k = normalize(c0, m0, f0, k0)

    if apply_updates:
        c, m, f, k = parc_update(c, m, f, k)

    return {
        "c": round(float(c), 4),
        "m": round(float(m), 4),
        "f": round(float(f), 4),
        "k": round(float(k), 4),
    }


# -----------------------------
# Command Line Usage
# -----------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        print(parc_vector(text))
    else:
        print("Usage: python parc.py \"your text here\"")
