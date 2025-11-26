// src/js/parc.mjs
// PARC Reference Engine (JavaScript / ES Module)
// UTF-PARC 1.0 Compatible
// License: MIT

// -----------------------------
// Utility
// -----------------------------

/**
 * Clamp a number into [0, 1].
 * @param {number} x
 * @returns {number}
 */
export function clamp(x) {
  const n = Number(x);
  if (Number.isNaN(n)) return 0;
  return Math.max(0, Math.min(1, n));
}

/**
 * Simple seeded-ish random wrapper if you ever want determinism.
 * For now, we just expose Math.random().
 */
function rand() {
  return Math.random();
}

// -----------------------------
// Heuristic Encoding Layer
// -----------------------------

/**
 * Convert text into initial (c0, m0, f0, k0) seeds.
 * This mirrors the Python encode_text() function.
 *
 * Heuristic:
 *  - correctness (c0) bumps on definitional markers: "is", "are", "means", "because"
 *  - misconception (m0) bumps on negation-like markers: "not", "never", "wrong", "unless"
 *  - fog (f0) is 1 - max(c0, m0) (will be recomputed later anyway)
 *  - confidence (k0) is 0.3–1.0 with a random drift
 *
 * @param {string} text
 * @returns {[number, number, number, number]} tuple [c0, m0, f0, k0]
 */
export function encodeText(text) {
  const t = String(text).toLowerCase().trim();
  const tokens = t.split(/\s+/).filter(Boolean);
  const len = Math.max(1, tokens.length);

  const correctWords = ["is", "are", "means", "because"];
  const misWords = ["not", "never", "wrong", "unless"];

  let c0 = 0;
  let m0 = 0;

  for (const w of tokens) {
    if (correctWords.includes(w)) c0 += 1;
    if (misWords.includes(w)) m0 += 1;
  }

  c0 = c0 / len;
  m0 = m0 / len;

  const f0 = 1 - Math.max(c0, m0);
  const k0 = 0.3 + 0.7 * rand();

  return [c0, m0, f0, k0];
}

// -----------------------------
// UTF-PARC Normalization
// -----------------------------

/**
 * Enforce UTF-PARC 1.0 rules:
 *  - clamp all values to [0,1]
 *  - ensure c + m ≤ 1
 *  - recompute fog as f = 1 - max(c, m)
 *
 * @param {number} c0
 * @param {number} m0
 * @param {number} f0   (ignored except for debugging)
 * @param {number} k0
 * @returns {[number, number, number, number]} [c, m, f, k]
 */
export function normalize(c0, m0, f0, k0) {
  let c = clamp(c0);
  let m = clamp(m0);
  let k = clamp(k0);

  const total = c + m;
  if (total > 1) {
    c = c / total;
    m = m / total;
  }

  const f = 1 - Math.max(c, m);

  return [c, m, f, k];
}

// -----------------------------
// PARC Temporal Update
// -----------------------------

/**
 * Apply PARC dynamical update equations (optional).
 * Used when tracking reasoning over time.
 *
 * Mirrors Python parc_update().
 *
 * @param {number} c
 * @param {number} m
 * @param {number} f
 * @param {number} k
 * @param {object}  [opts]
 * @param {number}  [opts.gamma=0.3]
 * @param {number}  [opts.delta=0.1]
 * @param {number}  [opts.beta=0.5]
 * @param {number}  [opts.rho=0.5]
 * @param {number}  [opts.steps=3]
 * @returns {[number, number, number, number]} [c, m, f, k]
 */
export function parcUpdate(
  c,
  m,
  f,
  k,
  opts = {}
) {
  let {
    gamma = 0.3,
    delta = 0.1,
    beta = 0.5,
    rho = 0.5,
    steps = 3,
  } = opts;

  for (let i = 0; i < steps; i++) {
    const gammaEff = gamma * (1 - m);
    const deltaEff = delta + beta * c;

    let cNew = c + gammaEff * (1 - c - m);
    let mNew = m * (1 - deltaEff);

    let fNew;
    if (cNew + mNew > 1) {
      const total = cNew + mNew;
      cNew = cNew / total;
      mNew = mNew / total;
      fNew = 0;
    } else {
      fNew = 1 - Math.max(cNew, mNew);
    }

    const kNew = k + rho * (cNew - mNew - k);

    c = cNew;
    m = mNew;
    f = fNew;
    k = kNew;
  }

  return [c, m, f, k];
}

// -----------------------------
// Public API
// -----------------------------

/**
 * Produce the final UTF-PARC 1.0 vector for a given text.
 *
 * @param {string} text
 * @param {object} [opts]
 * @param {boolean} [opts.applyUpdates=true]
 * @returns {{c:number, m:number, f:number, k:number}}
 */
export function parcVector(text, opts = {}) {
  const { applyUpdates = true } = opts;

  const [c0, m0, f0, k0] = encodeText(text);
  let [c, m, f, k] = normalize(c0, m0, f0, k0);

  if (applyUpdates) {
    [c, m, f, k] = parcUpdate(c, m, f, k);
  }

  return {
    c: Number(c.toFixed(4)),
    m: Number(m.toFixed(4)),
    f: Number(f.toFixed(4)),
    k: Number(k.toFixed(4)),
  };
}

// Default export for convenience
export default {
  clamp,
  encodeText,
  normalize,
  parcUpdate,
  parcVector,
};
