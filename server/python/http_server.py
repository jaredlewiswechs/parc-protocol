#!/usr/bin/env python3
# UTF-PARC Reference HTTP Server (Python)
# Version 1.0

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ---------------------------------------------------------
# Core PARC Functions (matches spec 1.0)
# ---------------------------------------------------------

def normalize_parc(v):
    """Normalize and enforce UTF-PARC vector rules."""
    c = float(v.get("c", 0.0))
    m = float(v.get("m", 0.0))
    k = float(v.get("k", 0.5))

    # Keep c,m in [0,1]
    c = max(0.0, min(1.0, c))
    m = max(0.0, min(1.0, m))

    # Enforce c + m ≤ 1
    if c + m > 1:
        total = c + m
        c = c / total
        m = m / total

    # Fog rule
    f = 1 - max(c, m)

    return {"c": c, "m": m, "f": f, "k": k}


def validate_parc(v):
    """Validate UTF-PARC vector and return errors."""
    errors = []

    # Must include all fields
    for key in ["c", "m", "f", "k"]:
        if key not in v:
            errors.append(f"missing field: {key}")

    # Range check
    for k2 in ["c", "m", "f", "k"]:
        if k2 in v:
            if not (0.0 <= float(v[k2]) <= 1.0):
                errors.append(f"{k2} out of range [0,1]")

    c = float(v.get("c", 0))
    m = float(v.get("m", 0))
    f = float(v.get("f", 0))

    # Constraint: c + m ≤ 1
    if c + m > 1:
        errors.append("c + m must not exceed 1")

    # Constraint: fog rule
    if abs(f - (1 - max(c, m))) > 1e-6:
        errors.append("fog must equal 1 - max(c,m)")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def encode_text(text, confidence_hint=None):
    """
    Minimal reference encoder:
    This is NOT the production classifier.
    It demonstrates the pipeline structure only.
    """
    t = text.lower().split()

    c_keywords = ["is", "are", "means", "because"]
    m_keywords = ["not", "wrong", "never", "unless"]

    c = sum(1 for w in t if w in c_keywords) / max(1, len(t))
    m = sum(1 for w in t if w in m_keywords) / max(1, len(t))

    # Fog rule
    f = 1 - max(c, m)

    # Confidence
    k = confidence_hint if confidence_hint is not None else 0.4

    return normalize_parc({"c": c, "m": m, "f": f, "k": k})


# ---------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------

class PARCHandler(BaseHTTPRequestHandler):

    def _json(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body.decode("utf-8"))
        except Exception:
            return self._json(400, {"error": "Invalid JSON"})

        path = self.path

        # ---------------------------------------------------------
        # /v1/parc/vector
        # ---------------------------------------------------------
        if path == "/v1/parc/vector":
            text = data.get("text", "")
            conf = data.get("confidence_hint")
            result = encode_text(text, conf)
            return self._json(200, result)

        # ---------------------------------------------------------
        # /v1/parc/update
        # ---------------------------------------------------------
        if path == "/v1/parc/update":
            v = data.get("state")
            steps = int(data.get("steps", 1))
            params = data.get("params", {})

            gamma = float(params.get("gamma", 0.3))
            delta = float(params.get("delta", 0.1))
            beta  = float(params.get("beta", 0.5))
            rho   = float(params.get("rho", 0.5))

            for _ in range(steps):
                c = v["c"] + gamma * (1 - v["c"] - v["m"])
                m = v["m"] * (1 - delta - beta * v["c"])
                k = max(0.0, min(1.0, v["k"] + rho * (1 - v["k"])))
                f = 1 - max(c, m)
                v = normalize_parc({"c": c, "m": m, "f": f, "k": k})

            return self._json(200, v)

        # ---------------------------------------------------------
        # /v1/parc/batch
        # ---------------------------------------------------------
        if path == "/v1/parc/batch":
            texts = data.get("texts", [])
            results = [encode_text(t) for t in texts]
            return self._json(200, {"results": results})

        # ---------------------------------------------------------
        # /v1/parc/validate
        # ---------------------------------------------------------
        if path == "/v1/parc/validate":
            result = validate_parc(data.get("vector", {}))
            return self._json(200, result)

        # Unknown route
        return self._json(404, {"error": "Unknown endpoint"})


# ---------------------------------------------------------
# Server Bootstrap
# ---------------------------------------------------------

def run(host="0.0.0.0", port=8000):
    print(f"UTF-PARC Python server running at http://{host}:{port}")
    server = HTTPServer((host, port), PARCHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
