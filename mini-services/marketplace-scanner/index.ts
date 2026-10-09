/**
 * Marketplace Scanner — 24/7 background service.
 *
 * Polls /api/marketplaces/scan every 5 minutes.
 * When an honest paid task appears (the "gold"), it logs the finding.
 *
 * Port: 3031
 * Endpoints: GET /status — returns latest scan + uptime
 *           GET /scan-now — triggers immediate scan
 */

const SCAN_INTERVAL_MS = 5 * 60 * 1000;
const SCAN_URL = "http://localhost:3000/api/marketplaces/scan";
const STATUS_PORT = 3031;
const STATE_FILE = "/home/z/my-project/.marketplace-state/scanner-service.json";

const serviceStart = Date.now();
let scanCount = 0;
let lastScan: any = null;
let lastError: string | null = null;

async function runScan(): Promise<void> {
  scanCount++;
  console.log(`[scanner] scan #${scanCount} at ${new Date().toISOString()}`);

  try {
    const ctrl = new AbortController();
    const timeout = setTimeout(() => ctrl.abort(), 25000);
    const res = await fetch(SCAN_URL, { method: "POST", signal: ctrl.signal });
    clearTimeout(timeout);

    if (!res.ok) throw new Error(`scan endpoint returned HTTP ${res.status}`);

    const data = await res.json();
    const ba = data.basedagents || {};
    const tb = data.taskbounty || {};

    const has_gold = (ba.honest_paid || 0) > 0 || (tb.total_bounties || 0) > 0 || (tb.paid_missions || 0) > 0;

    let best_task: any = null;
    if (ba.best_paid_task) {
      best_task = {
        platform: "BasedAgents",
        task_id: ba.best_paid_task.task_id,
        title: ba.best_paid_task.title,
        bounty: `${ba.best_paid_task.bounty?.amount_display || "?"} ${ba.best_paid_task.bounty?.token || "USDC"}`,
        ev: ba.best_paid_task.estimated_ev_usd || 0,
      };
    } else if (tb.best_bounty) {
      best_task = {
        platform: "TaskBounty",
        task_id: tb.best_bounty.task_id || tb.best_bounty.id || "?",
        title: tb.best_bounty.title,
        bounty: `$${tb.best_bounty.reward || tb.best_bounty.bounty_amount || "?"}`,
        ev: 0,
      };
    }

    lastScan = {
      scanned_at: data.scanned_at,
      has_gold,
      basedagents_honest_paid: ba.honest_paid || 0,
      taskbounty_bounties: tb.total_bounties || 0,
      best_task,
    };
    lastError = null;

    if (has_gold) {
      console.log(`[scanner] 🎯 GOLD FOUND! ${JSON.stringify(best_task)}`);
    } else {
      console.log(`[scanner] no gold yet — BA paid=${ba.honest_paid || 0}, TB bounties=${tb.total_bounties || 0}`);
    }

    try {
      const state = {
        service_started_at: new Date(serviceStart).toISOString(),
        scan_count: scanCount,
        last_scan: lastScan,
        last_error: lastError,
        uptime_seconds: Math.floor((Date.now() - serviceStart) / 1000),
      };
      await Bun.write(STATE_FILE, JSON.stringify(state, null, 2));
    } catch (e) {
      console.error(`[scanner] state file write failed: ${e}`);
    }
  } catch (e) {
    lastError = e instanceof Error ? e.message : String(e);
    console.error(`[scanner] scan failed: ${lastError}`);
  }
}

Bun.serve({
  port: STATUS_PORT,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/status" || url.pathname === "/") {
      return Response.json({
        service: "marketplace-scanner",
        status: "running",
        uptime_seconds: Math.floor((Date.now() - serviceStart) / 1000),
        scan_count: scanCount,
        scan_interval_seconds: SCAN_INTERVAL_MS / 1000,
        last_scan: lastScan,
        last_error: lastError,
        scan_endpoint: SCAN_URL,
      });
    }
    if (url.pathname === "/scan-now") {
      runScan();
      return Response.json({ triggered: true, message: "scan started" });
    }
    return new Response("Not Found", { status: 404 });
  },
});

console.log(`[scanner] service started on port ${STATUS_PORT}`);
console.log(`[scanner] polling ${SCAN_URL} every ${SCAN_INTERVAL_MS / 1000}s`);

runScan();
setInterval(runScan, SCAN_INTERVAL_MS);

process.on("SIGTERM", () => {
  console.log("[scanner] received SIGTERM, shutting down");
  process.exit(0);
});
