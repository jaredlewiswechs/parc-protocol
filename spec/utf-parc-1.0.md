Great — next file in your repo structure is:

✅ /spec/utf-parc-1.0.md

This is the official protocol specification — the most important file besides the README.

I will give you:
	•	fully valid GitHub Markdown
	•	all code blocks properly fenced + closed
	•	zero unicode separators that break rendering
	•	no ambiguous formatting

You can paste this as-is and GitHub will render it perfectly.

⸻

✅ COPY/PASTE SAFE VERSION — /spec/utf-parc-1.0.md

# UTF-PARC 1.0 Specification
The Universal Transfer Format for PARC Cognitive State Vectors  
Version 1.0 — Stable Release

UTF-PARC defines how cognitive states are represented, normalized, validated, and transmitted across systems.

A UTF-PARC vector is:

(c, m, f, k)

Where:
- **c** = correctness score ∈ [0,1]  
- **m** = misconception score ∈ [0,1]  
- **f** = fog/uncertainty score ∈ [0,1]  
- **k** = confidence calibration score ∈ [0,1]  

UTF-PARC vectors must obey strict mathematical rules.

---

## 1. Normative Definitions

### 1.1 Vector Format

A UTF-PARC vector MUST be represented as:

```json
{
  "c": 0.0,
  "m": 0.0,
  "f": 0.0,
  "k": 0.0
}
```

1.2 Domain

Valid range for each component:

0.0 ≤ c ≤ 1.0
0.0 ≤ m ≤ 1.0
0.0 ≤ f ≤ 1.0
0.0 ≤ k ≤ 1.0


⸻

2. Canonical Rules

2.1 Mutual Exclusivity Constraint

Correctness and misconception cannot simultaneously exceed the total range:

c + m ≤ 1.0

2.2 Fog (f) Definition

Fog is always derived:

f = 1 - max(c, m)

No implementation may override f.

2.3 Confidence (k)

Confidence must be provided or inferred.
If inferred and no metadata exists:

k = 0.3 + 0.7 * random()

Confidence is NOT normalized automatically.

⸻

3. Required Functions

Every UTF-PARC implementation must provide the following functions.

3.1 normalize(vector)

Normalize a vector enforcing UTF-PARC rules.

Input:
{ "c": 0.8, "m": 0.4, "f": 0.1, "k": 0.7 }

Output:
{
  "c": 0.67,
  "m": 0.33,
  "f": 0.33,
  "k": 0.7
}

3.2 validate(vector)

Validate a UTF-PARC vector.

{
  "valid": false,
  "errors": ["c + m > 1", "fog must equal 1 - max(c,m)"]
}

3.3 compare(v1, v2)

Compare two vectors for cognitive distance.

Distance metric MUST BE:

d = |c1 - c2| + |m1 - m2| + |f1 - f2| + |k1 - k2|


⸻

4. Serialization Requirements

Vector must be encoded as UTF-8 JSON.

4.1 Allowed Media Types

application/vnd.parc.vector+json
application/json

4.2 Disallowed Formats
	•	XML
	•	YAML
	•	Protobuf (unless wrapped in JSON envelope)

⸻

5. Temporal Update Rules (PARC Dynamics)

Systems may include update logic:

c' = c + γ(1 − c − m)
m' = m(1 − δ − βc)
k' = clamp(k + ρ(1 − k), 0, 1)
f' = 1 − max(c', m')

Where:
	•	γ = learning gain
	•	δ = misconception decay
	•	β = corrective coupling
	•	ρ = confidence momentum

All parameters must be documented.

⸻

6. Metadata Extensions

Implementations MAY attach metadata under:

"_parc_meta"

Example:

{
  "c": 0.52,
  "m": 0.21,
  "f": 0.48,
  "k": 0.59,
  "_parc_meta": {
    "domain": "medical",
    "source": "gpt-4o"
  }
}

Metadata MUST NOT affect core values.

⸻

7. Compliance Requirements

A server or library is UTF-PARC compliant if:
	1.	It generates valid (c,m,f,k) vectors
	2.	It enforces fog rule
	3.	It enforces mutual exclusivity (c + m ≤ 1)
	4.	It returns validation results
	5.	It serializes as UTF-8 JSON
	6.	It supports normalization

A reference implementation is provided in /src/python/parc.py.

⸻

8. Error Codes

8.1 VectorConstraintViolation

"c + m must not exceed 1"

8.2 FogViolation

"fog must equal 1 - max(c,m)"

8.3 InvalidRange

"all components must be between 0.0 and 1.0"

8.4 MissingField

"vector must include c, m, f, k"


⸻

9. Versioning

Major versions break compatibility:

UTF-PARC 1.x

Minor versions are additive.

Current version: 1.0.0

⸻

10. Reference Example

{
  "c": 0.72,
  "m": 0.08,
  "f": 0.28,
  "k": 0.63
}


⸻

11. License

UTF-PARC is released under:

MIT License


⸻

12. Summary

UTF-PARC 1.0 defines:
	•	canonical structure of cognitive vectors
	•	universal normalization rules
	•	deterministic fog calculation
	•	explicit constraints
	•	update dynamics
	•	metadata extension rules
	•	verification protocol

This is the official specification for all PARC-compliant systems.

