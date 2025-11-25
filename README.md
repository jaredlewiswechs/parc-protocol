# UTF-PARC 1.0 — Universal Cognitive State Protocol

PARC is a universal reasoning protocol that compresses *any* model’s output into a
4-dimensional cognitive state: S = (c, m, f, k)

Where:
- **c** — correctness  
- **m** — misconception strength  
- **f** — fog / uncertainty  
- **k** — confidence  

PARC provides a standardized way to interpret and compare reasoning across
LLMs, agents, humans, and symbolic systems.

It works in any domain:
- law  
- medicine  
- math  
- science  
- education  
- coding  
- everyday reasoning  

And across all model families:
- OpenAI  
- Anthropic  
- Google  
- Meta  
- Local LLMs  
- Rule-based systems  
- Autonomous agents  

---

## 🧠 The Core Insight

Human meaning is infinite.  
But **the number of cognitive states is finite**.

PARC compresses reasoning into a universal vector that:
- detects hallucinations  
- identifies misconceptions  
- measures confidence  
- quantifies uncertainty  
- standardizes output from any model  
- enables cross-model interoperability  

PARC is to cognitive state what **UTF-8** is to text encoding.

---

## 🧰 What’s in This Repo?

- **UTF-PARC 1.0 Spec** → `/spec/utf-parc-1.0.md`  
- **Python Reference Engine** → `/src/python/parc.py`  
- **JavaScript Module** → `/src/js/parc.mjs`  
- **HTTP API Spec** → `/api/http-parc.md`  
- **Colab Demo Notebook** → `/examples/demo_parc.ipynb`  

You now have:
- a protocol  
- an SDK  
- a reference implementation  
- example code  
- open-source licensing  

Everything needed for adoption.

---

## 🚀 Quick Start (Python)

\`\`\`python
from parc import parc_vector

s = parc_vector("The mitochondria is the powerhouse of the cell")
print(s)

# → { "c": 0.72, "m": 0.08, "f": 0.18, "k": 0.63 }
\`\`\`

---

## 🚀 Quick Start (JavaScript)

\`\`\`js
import { parcVector } from "./src/js/parc.mjs";

const s = parcVector("Photosynthesis converts light into chemical energy");
console.log(s);

// → { c: 0.81, m: 0.04, f: 0.15, k: 0.58 }
\`\`\`

---

## 🌐 Quick Start (HTTP API)

\`\`\`bash
curl -X POST https://api.yourdomain.com/parc \
  -H "Content-Type: application/json" \
  -d '{ "text": "The president makes laws" }'
\`\`\`

Response:

\`\`\`json
{ "c": 0.18, "m": 0.62, "f": 0.82, "k": 0.27 }
\`\`\`

---

## 📦 Install (Local)

Python:
\`\`\`bash
pip install parc-protocol
\`\`\`

JavaScript:
\`\`\`bash
npm install parc-protocol
\`\`\`

---

## 🧪 Run Tests

\`\`\`bash
pytest tests/
\`\`\`

---

## 📄 License

MIT License — free for commercial and academic use.

---

## 📬 Contact

jn.lewis1@outlook.com
or
jared.lewis@houstonisd.org
