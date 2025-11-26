# UTF-PARC 1.0 Specification  
**Universal Cognitive State Encoding Protocol**  
Version 1.0 — (c) 2025 PARC Initiative — MIT Licensed

---

## 1. Overview

UTF-PARC is a universal, model-agnostic protocol for encoding the cognitive state of any linguistic output into a **4-dimensional vector**: S = { c, m, f, k }

Where:

| Component | Name | Meaning |
|----------|-------|---------|
| **c** | Correctness | Alignment with truth or intended concept |
| **m** | Misconception | Strength of systematic wrongness |
| **f** | Fog | Uncertainty, ambiguity, missing information |
| **k** | Confidence | Meta-belief in the answer |

These four dimensions are **epistemological primitives**.  
Every reasoning system—human or machine—exhibits them.

UTF-PARC standardizes how to represent them.

---

## 2. Motivation

Existing systems output text.  
But text reveals nothing about its internal cognitive state.

LLMs, agents, tutors, robots, and reasoning engines need:

- error detection  
- misconception tracking  
- hallucination monitoring  
- uncertainty quantification  
- calibration  
- cross-model comparability  
- safety diagnostics  
- interpretability  
- reasoning drift detection  

UTF-PARC provides this interpretability layer.

---

## 3. Formal Structure

A UTF-PARC vector is:
c ∈ [0,1]
m ∈ [0,1]
f ∈ [0,1]
k ∈ [0,1]

With **global constraint**:
c + m ≤ 1

Fog is *derived*, not independent:
f = 1 − max(c, m)

Thus **only three degrees of freedom** exist:
- correctness  
- misconception  
- confidence  

Fog is always consistent with cognitive geometry.

---

## 4. Encoding Pipeline

Any system producing text must follow: text → heuristic/semiotic encoder → normalize → temporal update (optional)
### 4.1 Step 1 — Initial Heuristic Seed  
Implementations may choose their own method, but MUST:

- produce seeds {c0, m0, f0, k0}
- allow domain-specific heuristics
- allow LLM-based semantic scoring
- allow rule-based systems
- MUST clamp values to [0,1]

### 4.2 Step 2 — Normalization (REQUIRED)

All UTF-PARC encoders MUST enforce:
c = clamp(c)
m = clamp(m)
k = clamp(k)

if c + m > 1:
c = c / (c+m)
m = m / (c+m)

f = 1 − max(c,m)

### 4.3 Step 3 — Temporal Update (OPTIONAL but Recommended)

Systems MAY apply dynamical refinement using:

Parameters: gamma = learning influence
delta = misconception decay
beta  = correction scaling
rho   = confidence calibration

Update equations for each time step t: gamma_eff = gamma * (1 − m)
delta_eff = delta + beta * c

c_{t+1} = c_t + gamma_eff * (1 − c_t − m_t)
m_{t+1} = m_t * (1 − delta_eff)
f_{t+1} = 1 − max(c_{t+1}, m_{t+1})
k_{t+1} = k_t + rho * (c_{t+1} − m_{t+1} − k_t)

Systems SHALL apply between 1–5 iterations.

---

## 5. Output Format

UTF-PARC MUST output JSON:

```json
{
  "c": 0.74,
  "m": 0.12,
  "f": 0.26,
  "k": 0.81
}
```
All values MUST be floats in [0,1].

6. Requirements for UTF-PARC Compliance

To be compliant:
	1.	Must implement all normalization rules
	2.	Must output a valid {c,m,f,k} object
	3.	Must recompute fog as 1 − max(c,m)
	4.	Must expose an accessible parc_vector(text) or equivalent
	5.	Should include transparent heuristics
	6.	Should support temporal updates
	7.	Should allow domain-specific extensions
	8.	Must not redefine or reinterpret the four dimensions

⸻

7. Domain Extensions (Optional)

UTF-PARC MAY be extended for:

Education
	•	concept mastery
	•	misconception classification
	•	knowledge graph alignment

Law
	•	argument validity
	•	precedent alignment
	•	factual grounding

Medicine
	•	diagnostic probability
	•	misdiagnosis risk
	•	clinical uncertainty

Coding
	•	bug likelihood
	•	logic deviation
	•	algorithmic confidence

Each domain MAY append metadata via: _parc_meta
{
  "c": 0.61,
  "m": 0.14,
  "f": 0.39,
  "k": 0.72,
  "_parc_meta": {
    "domain": "medical",
    "misconception_type": "risk inversion"
  }
}

8. Security & Safety Implications

UTF-PARC is essential for:
	•	hallucination alarms
	•	sandboxed agents
	•	cognitive drift detection
	•	safety policy enforcement
	•	risk-aware autonomous systems

Example safety rule:
If (m > 0.60 AND k > 0.70):
    trigger "confident wrongness" failsafe


UTF-PARC uses semantic versioning: MAJOR.MINOR.PATCH
Version 1.0 guarantees:
	•	stable vector definition
	•	stable normalization rules
	•	backward compatibility for all 1.x.x implementations





In: "The mitochondria is the powerhouse of the cell."


Out: {
  "c": 0.72,
  "m": 0.08,
  "f": 0.18,
  "k": 0.63
}

11. License UTF-PARC 1.0 is published under:
MIT License — free for all commercial + academic use


12. Contact / Governance

The PARC specification is maintained by the HyperWeb PARC

Submissions / extensions / drafts via:
	•	GitHub Issues
	•	GitHub Pull Requests
	•	Email: jn.lewis1@outlook.com
	•	Draft proposals follow PIP (PARC Improvement Proposal) format



13. Summary

UTF-PARC 1.0 is:
	•	lightweight
	•	model-agnostic
	•	domain-universal
	•	deterministic
	•	interpretable
	•	safe
	•	future-proof

It is the UTF-8 of cognitive state. Any text → PARC → Universal meaning vector.





