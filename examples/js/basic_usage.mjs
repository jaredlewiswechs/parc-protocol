/**
 * UTF-PARC Example (JavaScript / Node.js)
 * =======================================
 *
 * Demonstrates how to use the JS PARC module:
 *
 *   import { encodeText, updateState, validateParc } from "../../src/js/parc.mjs";
 *
 * Run with:
 *
 *     node examples/js/basic_usage.mjs
 */

import { dirname, resolve } from "path";
import { fileURLToPath } from "url";

// ---------------------------------------------------------
// Resolve path to src/js/parc.mjs so we can import locally
// ---------------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PARC_PATH = resolve(__dirname, "../../src/js/parc.mjs");

// Dynamic import (works everywhere)
const { encodeText, updateState, validateParc } = await import(PARC_PATH);

// ---------------------------------------------------------
// Helper for nicer JSON printing
// ---------------------------------------------------------
function pretty(obj) {
  return JSON.stringify(obj, null, 2);
}

// ---------------------------------------------------------
// Main Example
// ---------------------------------------------------------
console.log("=== UTF-PARC JS Example ===\n");

// 1. Encode text
const text = "Photosynthesis converts light energy into chemical energy.";
console.log("Input text:");
console.log(" ", text, "\n");

const state = encodeText(text);
console.log("Initial PARC state (c, m, f, k):");
console.log(pretty(state), "\n");

// 2. Validate the vector
const validation = validateParc(state);
console.log("Validation:");
console.log(pretty(validation), "\n");

// 3. Apply temporal update steps
const params = {
  gamma: 0.3,
  delta: 0.1,
  beta: 0.5,
  rho: 0.5
};

const updated = updateState(state, 3, params);
console.log("Updated PARC state after 3 steps:");
console.log(pretty(updated), "\n");

// 4. Interpretation
const { c, m, f, k } = updated;

console.log("Interpretation:");

if (m > 0.3 && k > 0.6) {
  console.log(" → High-risk: confidently wrong (high m, high k).");
} else if (f > 0.4) {
  console.log(" → High fog: uncertainty or incomplete reasoning.");
} else if (c > 0.7 && m < 0.2) {
  console.log(" → Strong understanding with low misconception.");
} else {
  console.log(" → Mixed state.");
}

console.log("\nDone.");
