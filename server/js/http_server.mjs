/**
 * UTF-PARC Reference Server (JavaScript)
 * =====================================
 *
 * Minimal HTTP server implementing:
 *    • POST /v1/parc/vector
 *    • POST /v1/parc/update
 *    • POST /v1/parc/batch
 *    • POST /v1/parc/meta
 *    • POST /v1/parc/validate
 *
 * Run locally:
 *      npm install express
 *      node server/js/http_server.mjs
 */

import express from "express";
import bodyParser from "body-parser";

// -----------------------------------------------------
// Import PARC engine
// -----------------------------------------------------
import {
    encodeText,
    updateState,
    validateParc
} from "../../src/js/parc.mjs";

const app = express();
app.use(bodyParser.json());


// -----------------------------------------------------
// Endpoints
// -----------------------------------------------------

// Compute vector from text
app.post("/v1/parc/vector", (req, res) => {
    const { text, confidence_hint } = req.body;
    const result = encodeText(text, confidence_hint);
    res.json(result);
});


// Update state
app.post("/v1/parc/update", (req, res) => {
    const { state, steps, params } = req.body;
    const result = updateState(state, steps, params);
    res.json(result);
});


// Batch vectorization
app.post("/v1/parc/batch", (req, res) => {
    const { texts } = req.body;
    const results = texts.map(t => encodeText(t));
    res.json({ results });
});


// Attach metadata
app.post("/v1/parc/meta", (req, res) => {
    const { vector, meta } = req.body;
    const output = { ...vector, _parc_meta: meta };
    res.json(output);
});


// Validate vector
app.post("/v1/parc/validate", (req, res) => {
    const { vector } = req.body;
    res.json(validateParc(vector));
});


// Root
app.get("/", (req, res) => {
    res.json({
        status: "ok",
        message: "UTF-PARC Reference Server (JavaScript)"
    });
});


// -----------------------------------------------------
// Start Server
// -----------------------------------------------------
const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
    console.log(`UTF-PARC JS server running on http://localhost:${PORT}`);
});
