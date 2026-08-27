const ALLOWED_SOURCE_TYPES = new Set(["SAMPLE", "LOCAL"]);
const ALLOWED_RISK_LEVELS = new Set(["GREEN", "YELLOW", "RED"]);

function numberInRange(value, minimum, maximum, integer = false) {
  const number = Number(value);
  return Number.isFinite(number) && number >= minimum && number <= maximum && (!integer || Number.isInteger(number)) ? number : null;
}

function shortText(value, maximum) {
  return typeof value === "string" && value.trim().length > 0 && value.trim().length <= maximum ? value.trim() : null;
}

function configuration() {
  const url = process.env.SUPABASE_URL;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  return url && serviceRoleKey ? { url: url.replace(/\/$/, ""), serviceRoleKey } : null;
}

module.exports = async (request, response) => {
  response.setHeader("Allow", "POST");
  response.setHeader("Cache-Control", "no-store");

  if (request.method !== "POST") {
    return response.status(405).json({ error: "Only POST requests are supported." });
  }

  const config = configuration();
  if (!config) {
    return response.status(503).json({ error: "Database is not configured yet." });
  }

  const body = request.body || {};
  const sessionId = shortText(body.sessionId, 64);
  const sourceType = shortText(body.sourceType, 12);
  const documentType = shortText(body.documentType, 64);
  const verdict = shortText(body.verdict, 64);
  const riskLevel = shortText(body.riskLevel, 12);
  const auditVersion = shortText(body.auditVersion, 16);
  const imageWidth = numberInRange(body.imageWidth, 1, 20000, true);
  const imageHeight = numberInRange(body.imageHeight, 1, 20000, true);
  const trustScore = numberInRange(body.trustScore, 0, 100, true);
  const anomalyIndex = numberInRange(body.anomalyIndex, 0, 1);

  if (!sessionId || !sourceType || !ALLOWED_SOURCE_TYPES.has(sourceType) || !documentType || !verdict || !riskLevel || !ALLOWED_RISK_LEVELS.has(riskLevel) || !auditVersion || imageWidth === null || imageHeight === null || trustScore === null || anomalyIndex === null) {
    return response.status(400).json({ error: "The audit payload is incomplete or invalid." });
  }

  try {
    const supabaseResponse = await fetch(`${config.url}/rest/v1/scan_audits`, {
      method: "POST",
      headers: {
        apikey: config.serviceRoleKey,
        Authorization: `Bearer ${config.serviceRoleKey}`,
        "Content-Type": "application/json",
        Prefer: "return=representation"
      },
      body: JSON.stringify([{
        session_id: sessionId,
        source_type: sourceType,
        document_type: documentType,
        image_width: imageWidth,
        image_height: imageHeight,
        trust_score: trustScore,
        verdict,
        risk_level: riskLevel,
        anomaly_index: anomalyIndex,
        audit_version: auditVersion
      }])
    });

    if (!supabaseResponse.ok) {
      const details = await supabaseResponse.text();
      console.error("Supabase audit insert failed", supabaseResponse.status, details);
      return response.status(502).json({ error: "The database could not save this audit." });
    }

    const records = await supabaseResponse.json();
    return response.status(201).json({ auditId: records[0].id, createdAt: records[0].created_at });
  } catch (error) {
    console.error("Supabase connection failed", error);
    return response.status(502).json({ error: "The database connection is unavailable." });
  }
};

