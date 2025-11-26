## 1. Overview

The HTTP-PARC API exposes:

- `/v1/parc/vector` – compute cognitive state from text  
- `/v1/parc/update` – apply temporal update rules  
- `/v1/parc/batch` – batch vectorization  
- `/v1/parc/meta` – attach or extract PARC metadata  
- `/v1/parc/validate` – verify UTF-PARC compliance  

All endpoints return JSON.  
All servers must be stateless.

---

## 2. Base URL

https://api.parc.dev

Local development:

http://localhost:8000

---

## 3. Authentication

Local/offline: **no auth required**  
Cloud deployments may use:

- `Authorization: Bearer <token>`
- OAuth2
- Basic Auth (discouraged)

---

## 4. Endpoints

---

### 4.1 POST `/v1/parc/vector`

Compute a UTF-PARC cognitive vector for a text input.

#### **Request**
```json
{
  "text": "Photosynthesis uses sunlight to convert CO2 and water into glucose.",
  "confidence_hint": 0.8
}
```
Response

{
  "c": 0.74,
  "m": 0.10,
  "f": 0.26,
  "k": 0.83
}


⸻

4.2 POST /v1/parc/update

Apply one or more temporal update steps.

Request

{
  "state": { "c": 0.51, "m": 0.22, "f": 0.49, "k": 0.55 },
  "steps": 2,
  "params": {
    "gamma": 0.3,
    "delta": 0.1,
    "beta": 0.5,
    "rho": 0.2
  }
}

Response

{
  "c": 0.62,
  "m": 0.17,
  "f": 0.38,
  "k": 0.67
}


⸻

4.3 POST /v1/parc/batch

Vectorize multiple texts.

Request

{
  "texts": [
    "Gravity pulls objects toward Earth.",
    "Congress writes and passes laws.",
    "The heart pumps blood through the circulatory system."
  ]
}

Response

{
  "results": [
    { "c": 0.88, "m": 0.04, "f": 0.12, "k": 0.91 },
    { "c": 0.73, "m": 0.09, "f": 0.27, "k": 0.80 },
    { "c": 0.92, "m": 0.03, "f": 0.08, "k": 0.89 }
  ]
}


⸻

4.4 POST /v1/parc/meta

Attach or extract metadata associated with a UTF-PARC vector.

Request

{
  "vector": { "c": 0.52, "m": 0.21, "f": 0.48, "k": 0.59 },
  "meta": {
    "domain": "legal",
    "misconception_type": "burden_of_proof"
  }
}

Response

{
  "c": 0.52,
  "m": 0.21,
  "f": 0.48,
  "k": 0.59,
  "_parc_meta": {
    "domain": "legal",
    "misconception_type": "burden_of_proof"
  }
}


⸻

4.5 POST /v1/parc/validate

Validate a UTF-PARC vector.

Request

{
  "vector": { "c": 0.92, "m": 0.15, "f": 0.10, "k": 0.85 }
}

Response

{
  "valid": false,
  "errors": [
    "c + m > 1",
    "fog must equal 1 - max(c,m)"
  ]
}


⸻

5. Error Responses

Example Error

{
  "error": {
    "type": "InvalidVector",
    "message": "c + m must not exceed 1",
    "hint": "Normalize the vector using UTF-PARC rules."
  }
}


⸻

6. Versioning

Clients may request a specific version:

Accept: application/vnd.parc.v1+json

Servers must respond:

Content-Type: application/vnd.parc.v1+json


⸻

7. Self-Hosted Implementations

Python server:

/server/python/http_server.py

JavaScript server:

/server/js/http_server.mjs

Run locally:

python server/python/http_server.py

or

node server/js/http_server.mjs


⸻

8. Rate Limits

Tier	Limit (req/min)
Local	Unlimited
Free	60
Pro	600
Enterprise	Custom


⸻

9. Security

Production servers should:
	•	enforce HTTPS
	•	rate limit abusive requests
	•	cap input size
	•	normalize vectors
	•	log security-critical actions

⸻

10. Summary

HTTP-PARC is the official REST protocol for UTF-PARC:
	•	Universal cognitive state extraction
	•	Model-agnostic reasoning diagnostics
	•	Lightweight integration
	•	Safe, interpretable AI pipelines
	•	Cross-model interoperability

---
