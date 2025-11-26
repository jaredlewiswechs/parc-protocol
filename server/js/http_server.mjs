// UTF-PARC Reference HTTP Server (Node.js)
// Version 1.0

import http from "http";

// ---------------------------------------------------------
// Core PARC Functions (matches spec 1.0)
// ---------------------------------------------------------

function normalizePARC(v) {
  let c = Number(v.c ?? 0);
  let m = Number(v.m ?? 0);
  let k = Number(v.k ?? 0.5);

  // Clamp c,m to [0,1]
  c = Math.max(0, Math.min(1, c));
  m = Math.max(0, Math.min(1, m));

  // Enforce c + m ≤ 1
  if (c + m > 1) {
    const total = c + m;
    c = c / total;
    m = m / total;
  }

  // Fog rule
  const f = 1 - Math.max(c, m);

  return { c, m, f, k };
}

function validatePARC(v) {
  const errors = [];

  // Required fields
  for (const key of ["c", "m", "f", "k"]) {
    if (!(key in v)) errors.push(`missing field: ${key}`);
  }

  // Range check
  for (const key of ["c", "m", "f", "k"]) {
    if (key in v) {
      const num = Number(v[key]);
      if (!(num >= 0 && num <= 1)) {
        errors.push(`${key} out of range [0,1]`);
      }
    }
  }

  const c = Number(v.c ?? 0);
  const m = Number(v.m ?? 0);
  const f = Number(v.f ?? 0);

  if (c + m > 1) errors.push("c + m must not exceed 1");
  if (Math.abs(f - (1 - Math.max(c, m))) > 1e-6)
    errors.push("fog must equal 1 - max(c,m)");

  return { valid: errors.length === 0, errors };
}

function encodeText(text, confidenceHint = 0.4) {
  // NOTE:
  // This is not the production classifier.
  // It is a minimal demonstrator for the protocol.

  const words = text.toLowerCase().split(/\s+/g);

  const cWords = ["is", "are", "means", "because"];
  const mWords = ["not", "wrong", "never", "unless"];

  let c =
    words.filter((w) => cWords.includes(w)).length /
    Math.max(1, words.length);

  let m =
    words.filter((w) => mWords.includes(w)).length /
    Math.max(1, words.length);

  let f = 1 - Math.max(c, m);
  let k = confidenceHint;

  return normalizePARC({ c, m, f, k });
}

// ---------------------------------------------------------
// HTTP Server
// ---------------------------------------------------------

function jsonResponse(res, code, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(code, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  });
  res.end(body);
}

const server = http.createServer(async (req, res) => {
  if (req.method !== "POST") {
    return jsonResponse(res, 405, { error: "POST required" });
  }

  // Parse body
  let raw = "";
  for await (const chunk of req) raw += chunk;
  let data;
  try {
    data = JSON.parse(raw);
  } catch {
    return jsonResponse(res, 400, { error: "Invalid JSON" });
  }

  const path = req.url;

  // ---------------------------------------------------------
  // /v1/parc/vector
  // ---------------------------------------------------------
  if (path === "/v1/parc/vector") {
    const text = data.text ?? "";
    const conf = data.confidence_hint;
    return jsonResponse(res, 200, encodeText(text, conf));
  }

  // ---------------------------------------------------------
  // /v1/parc/update
  // ---------------------------------------------------------
  if (path === "/v1/parc/update") {
    let v = data.state;
    const steps = Number(data.steps ?? 1);
    const params = data.params ?? {};

    const gamma = Number(params.gamma ?? 0.3);
    const delta = Number(params.delta ?? 0.1);
    const beta = Number(params.beta ?? 0.5);
    const rho = Number(params.rho ?? 0.5);

    for (let i = 0; i < steps; i++) {
      let c = v.c + gamma * (1 - v.c - v.m);
      let m = v.m * (1 - delta - beta * v.c);
      let k = Math.max(0, Math.min(1, v.k + rho * (1 - v.k)));
      let f = 1 - Math.max(c, m);

      v = normalizePARC({ c, m, f, k });
    }

    return jsonResponse(res, 200, v);
  }

  // ---------------------------------------------------------
  // /v1/parc/batch
  // ---------------------------------------------------------
  if (path === "/v1/parc/batch") {
    const texts = data.texts ?? [];
    const results = texts.map((t) => encodeText(t));
    return jsonResponse(res, 200, { results });
  }

  // ---------------------------------------------------------
  // /v1/parc/validate
  // ---------------------------------------------------------
  if (path === "/v1/parc/validate") {
    return jsonResponse(res, 200, validatePARC(data.vector ?? {}));
  }

  // Unknown route
  return jsonResponse(res, 404, { error: "Unknown endpoint" });
});

// ---------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------

const PORT = process.env.PORT || 8000;
server.listen(PORT, () => {
  console.log(`UTF-PARC JS server running at http://localhost:${PORT}`);
});
