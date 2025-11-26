"""
UTF-PARC Example (Python)
=========================

Minimal example showing how to use the PARC core library:

- encode_text()   → turn free text into a (c, m, f, k) vector
- update_state()  → apply temporal update steps
- validate_parc() → sanity-check a vector

This script assumes the repo layout:

parc-protocol/
  src/
    python/
      parc.py
  examples/
    python/
      basic_usage.py

You can run it with:

    python examples/python/basic_usage.py
"""

import os
import sys
import json

# ---------------------------------------------------------------------
# Make sure we can import src/python/parc.py without installing a package
# ---------------------------------------------------------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_PYTHON_DIR = os.path.join(ROOT_DIR, "src", "python")

if SRC_PYTHON_DIR not in sys.path:
    sys.path.insert(0, SRC_PYTHON_DIR)

from parc import encode_text, update_state, validate_parc  # type: ignore


def pretty(obj) -> str:
    """Small helper for nicely formatted JSON output."""
    return json.dumps(obj, indent=2, sort_keys=True)


def main() -> None:
    print("=== UTF-PARC Python Example ===\n")

    # -----------------------------------------------------------------
    # 1. Encode a piece of text into a PARC vector
    # -----------------------------------------------------------------
    text = "Congress makes laws and the President signs them into law."

    print("Input text:")
    print(f"  {text}\n")

    state = encode_text(text)
    print("Initial PARC state (c, m, f, k):")
    print(pretty(state))
    print()

    # -----------------------------------------------------------------
    # 2. Validate the vector
    # -----------------------------------------------------------------
    validation = validate_parc(state)
    print("Validation result:")
    print(pretty(validation))
    print()

    # -----------------------------------------------------------------
    # 3. Apply temporal update steps (simulating learning over turns)
    # -----------------------------------------------------------------
    params = {
        "gamma": 0.3,   # learning rate for correctness
        "delta": 0.1,   # decay rate for misconceptions
        "beta": 0.5,    # interaction: correctness vs misconception
        "rho": 0.5,     # confidence growth rate
    }

    updated = update_state(state, steps=3, params=params)
    print("Updated PARC state after 3 steps:")
    print(pretty(updated))
    print()

    # -----------------------------------------------------------------
    # 4. Show key interpretations
    # -----------------------------------------------------------------
    c = updated["c"]
    m = updated["m"]
    f = updated["f"]
    k = updated["k"]

    print("Interpretation:")
    print(f"  correctness (c):   {c:.3f}")
    print(f"  misconception (m): {m:.3f}")
    print(f"  fog (f):           {f:.3f}")
    print(f"  confidence (k):    {k:.3f}")
    print()

    if m > 0.3 and k > 0.6:
        print("→ High-risk: confidently wrong (high m, high k).")
    elif f > 0.4:
        print("→ High fog: learner is uncertain / incomplete.")
    elif c > 0.7 and m < 0.2:
        print("→ Strong understanding with low misconception.")
    else:
        print("→ Mixed state: partial understanding with some noise.")

    print("\nDone.")


if __name__ == "__main__":
    main()
