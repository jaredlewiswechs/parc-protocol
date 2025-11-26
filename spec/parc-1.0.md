# UTF-PARC 1.0 Specification  
**Universal Cognitive State Encoding Standard**  
Version: 1.0  
Status: Open Standard Draft  

---

# 1. Purpose

UTF-PARC defines a universal, model-agnostic encoding for representing cognitive states produced by any reasoning system — including LLMs, agents, symbolic solvers, humans (via annotation), or hybrid systems.

Its purpose is to standardize the representation of:
- correctness  
- misconception  
- uncertainty  
- confidence  

…into a **4-dimensional normalized vector** that can be understood, compared, logged, transmitted, or audited across models, domains, and platforms.

UTF-PARC plays the same role for *cognitive state* that UTF-8 plays for *text*.

---

# 2. Cognitive Vector Definition

A UTF-PARC vector is a 4-tuple: S = (c, m, f, k)

Where each element satisfies: 
c ∈ [0, 1]
m ∈ [0, 1]
f ∈ [0, 1]
k ∈ [0, 1]

Each dimension:

| Symbol | Name | Meaning |
|--------|------|---------|
| **c** | correctness | Probability or degree of alignment with correct meaning |
| **m** | misconception | Strength of an identifiable wrong pattern |
| **f** | fog | Uncertainty, ambiguity, or lack of clarity |
| **k** | confidence | Self-reported or inferred confidence level |

Constraints:

1. **Normalization rule**  c + m ≤ 1
2. **Fog rule**  f = 1 − max(c, m)
3. **Confidence stability constraint**  k should covary with c − m

These constraints ensure consistency and interpretability.

---

# 3. Conceptual Semantics

UTF-PARC encodes **epistemic state**, not linguistic meaning.

Examples:

- High-c, low-m → likely correct  
- Low-c, high-m → confidently wrong  
- Low-c, low-m, high-f → unclear  
- High-k, low-c → dangerous hallucination  
- Medium-c, medium-m → mixed or contradictory answer  

**This structure is universal across disciplines** (law, medicine, math, coding, etc).

---

# 4. Encoding Algorithm (Reference Method)

This section defines a reference approach.  
Implementations MAY differ so long as output remains compliant.

## 4.1 Base Interpretation Stage

Input text is segmented into its meaningful components.

An implementation MAY use:
- transformer embeddings  
- rule-based patterns  
- token-level confidence  
- symbolic logic checks  
- domain models  
- hybrid systems  

The key requirement is to eventually produce estimates of:
- correctness likelihood  
- misconception likelihood  
- uncertainty indicators  
- confidence indicators  

## 4.2 Normalization Stage (Required)

Given raw values: c0, m0, f0?, k0

Apply: 
c = clamp(c0)
m = clamp(m0)
if c + m > 1:
norm = c + m
c /= norm
m /= norm

f = 1 - max(c, m)
k = clamp(k0)

This converts multiple model-dependent signals into a single, universal format.

## 4.3 Optional: Temporal Update Equation

For systems tracking reasoning over time:
c_{t+1} = c_t + γ (1 − c_t − m_t)
m_{t+1} = m_t (1 − δ − β c_t)
k_{t+1} = k_t + ρ (c_t − m_t − k_t)
f_{t+1} = 1 − max(c_{t+1}, m_{t+1})

This is the PARC update equation used in simulations and educational contexts.

It is **not required** for UTF-PARC compliance.

---

# 5. UTF-PARC Object Format

Standard JSON encoding:

```json
{
  "c": 0.72,
  "m": 0.08,
  "f": 0.18,
  "k": 0.63
}
```
Valid ranges:
	•	floats in [0, 1]
	•	at least 3 decimal places recommended


6. Transmission Protocol (UTF-PARC-TP)

UTF-PARC vectors may be transmitted over any channel.

A UTF-PARC-TP packet:
{
  "text": "The sky is blue because of Rayleigh scattering.",
  "parc": {
    "c": 0.81,
    "m": 0.02,
    "f": 0.17,
    "k": 0.71
  },
  "timestamp": "2025-11-25T12:00:00Z",
  "model": "gemini-3-pro",
  "version": "utf-parc-1.0"
}
Metadata fields are optional but recommended.


7. Validation Rules

A UTF-PARC vector is valid if:
	1.	All keys exist
	2.	All values ∈ [0, 1]
	3.	c + m ≤ 1
	4.	f = 1 − max(c, m)
	5.	No NaN or INF values
	6.	Keys use lowercase ASCII

8. Cross-Model Compatibility

UTF-PARC does not define how reasoning is extracted — only how it is represented.

This allows any system to provide cognitive state readings:
	•	GPT-4
	•	Gemini
	•	Claude
	•	Llama
	•	Symbolic solvers
	•	Autonomous agents
	•	Multi-model pipelines

As long as they output a valid (c, m, f, k) vector.

9. Reference Implementations

Included in /src/ of this repo:
	•	/src/python/parc.py — Python reference
	•	/src/js/parc.mjs — JavaScript module
	•	/api/http-parc.md — HTTP interface

These are the canonical examples of UTF-PARC compliant encoders.

10. Versioning

UTF-PARC uses semantic versioning:

MAJOR.MINOR.PATCH

Example:
	•	1.0.0 — first stable release
	•	1.1.0 — added dimensions or metadata
	•	2.0.0 — breaking changes


11. License

UTF-PARC 1.0 is released under the MIT License.

12. Contact

For proposals, extensions, or standardization work:

jn.lewis1@outlook.com or jared.lewis@outlook.com


















  
