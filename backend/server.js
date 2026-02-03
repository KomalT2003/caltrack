const express = require("express");
const path = require("path");

const app = express();

app.use(express.json({ limit: "1mb" }));

// Basic CORS for local dev (ok since this is a local-only app)
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});

function extractJsonObject(text) {
  if (!text) return null;
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start === -1 || end === -1 || end <= start) return null;
  const slice = text.slice(start, end + 1);
  try {
    return JSON.parse(slice);
  } catch {
    return null;
  }
}

app.post("/api/estimate", async (req, res) => {
  try {
    const text = String(req.body?.text || "").trim();
    if (!text) return res.status(400).json({ error: "Missing 'text'" });

    // Ollama defaults
    const ollamaHost = process.env.OLLAMA_HOST || "http://127.0.0.1:11434";
    // "phi3:mini" is commonly available in Ollama; override if you use a different tag.
    const model = process.env.OLLAMA_MODEL || "phi3:mini";

    const system =
      "You estimate calories from food descriptions. Return ONLY strict JSON with keys: " +
      "calories (number, integer), notes (string). " +
      "No markdown, no extra text.";

    const user =
      "Estimate total calories for this single entry. If quantity is vague, assume typical portion sizes. " +
      "Food: " +
      text;

    const payload = {
      model,
      stream: false,
      messages: [
        { role: "system", content: system },
        { role: "user", content: user }
      ],
      options: { temperature: 0.2 }
    };

    const resp = await fetch(`${ollamaHost}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const bodyText = await resp.text().catch(() => "");
      return res.status(502).json({
        error:
          `Ollama error (${resp.status}). Is Ollama running and model '${model}' pulled?`,
        details: bodyText.slice(0, 1000)
      });
    }

    const data = await resp.json();
    const content = data?.message?.content || "";

    const parsed = extractJsonObject(content);
    const calories = Number(parsed?.calories);
    const notes = parsed?.notes;

    if (!Number.isFinite(calories)) {
      return res.status(502).json({
        error: "Model returned invalid calories.",
        details: content.slice(0, 1000)
      });
    }

    return res.json({
      calories: Math.max(0, Math.round(calories)),
      notes: typeof notes === "string" ? notes : ""
    });
  } catch (err) {
    // Common case: Ollama not running
    const msg = err?.message || String(err);
    return res.status(502).json({
      error:
        "Failed to call Ollama. Start Ollama and pull the model, then try again.",
      details: msg
    });
  }
});

// Serve frontend for a single "app" origin (recommended)
const frontendDir = path.join(__dirname, "..", "frontend");
app.use(express.static(frontendDir));
app.get("/", (req, res) => {
  res.sendFile(path.join(frontendDir, "index.html"));
});

const port = Number(process.env.PORT || 8787);
app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`CalTrack server running: http://localhost:${port}`);
  console.log(`Using Ollama host: ${process.env.OLLAMA_HOST || "http://127.0.0.1:11434"}`);
  console.log(`Using model: ${process.env.OLLAMA_MODEL || "phi3:mini"}`);
});
