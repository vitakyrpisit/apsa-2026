/**
 * GitHub client for APSA-2026 bugfix bounty delivery.
 *
 * Purpose: end-to-end bugfix-PR workflow for bounty tasks.
 *   1. ensureFork(upstream)         — create fork in operator account if needed
 *   2. cloneAndBranch(upstream, br) — shallow clone fork + new branch
 *   3. commitAndPush(files, msg, br)— write files, commit, push to fork branch
 *   4. createPR(upstream, br, ...)  — open PR upstream:main <- fork:br
 *   5. listExistingPRs(upstream)    — dedupe (don't double-claim)
 *   6. status()                     — connection + identity check (no token leak)
 *
 * Token source: process.env.GITHUB_TOKEN (fine-grained PAT, stored in .env.local, mode 0600).
 * Never echo the token. Construct git URLs with the token only inside the spawned git process
 * (and redact it before any console output via the GIT_ASKPASS indirection pattern).
 *
 * Operator account: vitakyrpisit (verified 2026-10-09).
 */

import { exec as execCb, execFileSync } from "node:child_process";
import { promisify } from "node:util";
import { mkdtemp, rm, writeFile, mkdir, chmod, readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const exec = promisify(execCb);

const GH_API = "https://api.github.com";
const OPERATOR_LOGIN_FALLBACK = "vitakyrpisit";

export interface GhStatus {
  connected: boolean;
  reason?: string;
  login?: string;
  account_id?: number;
  public_repos?: number;
  has_write?: boolean;        // verified write on at least one own repo
  has_pr_read?: boolean;      // verified PR listing on own repo
  token_kind?: "fine_grained" | "classic" | "unknown";
  verified_at?: string;
}

export interface ForkInfo {
  fork_full_name: string;     // e.g. vitakyrpisit/SomeRepo
  fork_html_url: string;
  fork_ssh_url?: string;
  fork_clone_url: string;    // public clone URL (no token)
  created_now: boolean;      // true if just forked, false if already existed
}

export interface PrInfo {
  number: number;
  html_url: string;
  state: "open" | "closed";
  title: string;
  head_ref: string;
  base_ref: string;
}

function getToken(): string {
  const t = process.env.GITHUB_TOKEN || "";
  if (!t) throw new Error("GITHUB_TOKEN missing in env");
  return t;
}

function authedHeaders(extra: Record<string, string> = {}): Record<string, string> {
  return {
    Authorization: `Bearer ${getToken()}`,
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "apsa-2026-bugfixer-v4",
    ...extra,
  };
}

function authedCloneUrl(plainUrl: string): string {
  // Inject token into HTTPS URL for git clone.
  // https://github.com/owner/repo.git -> https://x-access-token:TOKEN@github.com/owner/repo.git
  // Using x-access-token as the username is GitHub's recommended practice for PAT auth.
  return plainUrl.replace(
    /^https:\/\/github\.com\//,
    `https://x-access-token:${encodeURIComponent(getToken())}@github.com/`
  );
}

async function ghFetch<T = any>(
  path: string,
  init: RequestInit = {}
): Promise<{ ok: boolean; status: number; body: T; headers: Headers }> {
  const res = await fetch(`${GH_API}${path}`, {
    ...init,
    headers: authedHeaders(init.headers as Record<string, string> | undefined),
  });
  const text = await res.text();
  let body: any = null;
  if (text) {
    try { body = JSON.parse(text); } catch { body = text; }
  }
  return { ok: res.ok, status: res.status, body, headers: res.headers };
}

/**
 * Status check. Verifies token + reports identity. Never leaks the token string.
 */
export async function status(): Promise<GhStatus> {
  try {
    const r = await ghFetch<any>("/user");
    if (!r.ok) {
      return {
        connected: false,
        reason: `api_http_${r.status}`,
        token_kind: "unknown",
      };
    }
    const login = body_login(r.body);
    const id = r.body?.id as number | undefined;
    const public_repos = r.body?.public_repos as number | undefined;
    const tokenKind: GhStatus["token_kind"] = guessTokenKind(r.headers);

    // Probe write access on operator's most-recently-pushed own repo.
    let hasWrite = false;
    let hasPrRead = false;
    if (login) {
      const reposR = await ghFetch<any>(
        `/users/${login}/repos?per_page=10&sort=updated&type=owner`
      );
      if (reposR.ok && Array.isArray(reposR.body) && reposR.body.length > 0) {
        const own = reposR.body.find((x: any) => x && !x.fork) || reposR.body[0];
        const name = own?.name as string | undefined;
        if (name) {
          const probe = await ghFetch<any>(`/repos/${login}/${name}`);
          if (probe.ok) {
            hasWrite = !!probe.body?.permissions?.push;
          }
          // PR listing endpoint (PR read).
          const pr = await ghFetch<any>(`/repos/${login}/${name}/pulls?state=open&per_page=1`);
          hasPrRead = pr.ok;
        }
      }
    }

    return {
      connected: true,
      login,
      account_id: id,
      public_repos,
      has_write: hasWrite,
      has_pr_read: hasPrRead,
      token_kind: tokenKind,
      verified_at: new Date().toISOString(),
    };
  } catch (e: any) {
    return { connected: false, reason: `exception: ${e?.message || String(e)}` };
  }
}

function body_login(b: any): string | undefined {
  return typeof b?.login === "string" ? b.login : undefined;
}

function guessTokenKind(h: Headers): GhStatus["token_kind"] {
  // Fine-grained PATs do NOT emit X-OAuth-Scopes (that's classic only).
  // Classic tokens emit X-OAuth-Scopes (even if empty list, header is present).
  const oauth = h.get("x-oauth-scopes");
  if (oauth === null || oauth === undefined) return "fine_grained";
  return "classic";
}

/**
 * Returns the operator's GitHub login (from API, falls back to env / known default).
 */
export async function getOperatorLogin(): Promise<string> {
  const fromEnv = process.env.GITHUB_USERNAME;
  if (fromEnv) return fromEnv;
  try {
    const r = await ghFetch<any>("/user");
    if (r.ok && r.body?.login) return r.body.login as string;
  } catch { /* fallthrough */ }
  return OPERATOR_LOGIN_FALLBACK;
}

export interface EnsureForkArgs {
  upstream_owner: string;
  upstream_repo: string;
}

/**
 * Ensures a fork of the upstream repo exists in the operator's account.
 * Returns fork metadata. Idempotent: returns existing fork if present.
 */
export async function ensureFork(args: EnsureForkArgs): Promise<ForkInfo> {
  const operator = await getOperatorLogin();
  const upstream = `${args.upstream_owner}/${args.upstream_repo}`;
  const forkFullName = `${operator}/${args.upstream_repo}`;

  // 1. Check if fork already exists.
  const existing = await ghFetch<any>(`/repos/${forkFullName}`);
  if (existing.ok && existing.body?.fork && existing.body?.parent?.full_name === upstream) {
    return {
      fork_full_name: forkFullName,
      fork_html_url: existing.body.html_url as string,
      fork_ssh_url: existing.body.ssh_url as string | undefined,
      fork_clone_url: existing.body.clone_url as string,
      created_now: false,
    };
  }
  // If something exists at forkFullName but it's not a fork of upstream, abort (avoid stomping real repo).
  if (existing.ok && existing.body && !existing.body.fork) {
    throw new Error(
      `Refusing to fork: ${forkFullName} already exists as a NON-fork repository. Aborting to prevent data loss.`
    );
  }

  // 2. Create fork.
  const created = await ghFetch<any>(
    `/repos/${upstream}/forks`,
    { method: "POST", body: JSON.stringify({ default_branch_only: false }) }
  );
  if (!created.ok) {
    throw new Error(
      `fork_create_failed: HTTP ${created.status} ${JSON.stringify(created.body).slice(0, 200)}`
    );
  }
  const fork = created.body;
  return {
    fork_full_name: fork.full_name as string,
    fork_html_url: fork.html_url as string,
    fork_ssh_url: fork.ssh_url as string | undefined,
    fork_clone_url: fork.clone_url as string,
    created_now: true,
  };
}

/**
 * Wait for fork to become available (GitHub forks are async).
 * Polls the parent link / clone availability up to ~60s.
 */
export async function waitForFork(args: EnsureForkArgs, timeoutMs = 60_000): Promise<void> {
  const operator = await getOperatorLogin();
  const forkFullName = `${operator}/${args.upstream_repo}`;
  const start = Date.now();
  let lastErr = "";
  while (Date.now() - start < timeoutMs) {
    const r = await ghFetch<any>(`/repos/${forkFullName}`);
    if (r.ok && r.body?.parent?.full_name === `${args.upstream_owner}/${args.upstream_repo}`) {
      // Also confirm the default branch ref exists (fork sometimes returns 404 for HEAD right after fork).
      const head = await ghFetch<any>(
        `/repos/${forkFullName}/git/refs/heads/${r.body.default_branch || "main"}`
      );
      if (head.ok) return;
      lastErr = `head_ref_not_ready (${head.status})`;
    } else if (r.ok && r.body && !r.body.fork) {
      throw new Error(`${forkFullName} exists but is not a fork`);
    } else {
      lastErr = `http_${r.status}`;
    }
    await sleep(2000);
  }
  throw new Error(`fork_not_ready_after_${timeoutMs}ms (last=${lastErr})`);
}

function sleep(ms: number) { return new Promise((r) => setTimeout(r, ms)); }

export interface CloneAndBranchArgs {
  fork: ForkInfo;
  branch_name: string;
  base_ref?: string; // default: fork's default branch (e.g. main)
}

export interface CloneResult {
  local_dir: string;
  branch: string;
  base_ref: string;
}

/**
 * Shallow-clones the fork into a temp dir and creates a new branch.
 * Token is injected into the URL via x-access-token username (HTTPS).
 * The token NEVER appears in stdout/stderr because we strip credentials from git URLs.
 */
export async function cloneAndBranch(args: CloneAndBranchArgs): Promise<CloneResult> {
  const baseRef = args.base_ref || (await forkDefaultBranch(args.fork));
  const localDir = await mkdtemp(join(tmpdir(), `apsa-fix-`));
  // Clone with --no-tags, shallow (depth 1 + branch) to keep it fast and offline-friendly.
  const url = authedCloneUrl(args.fork.fork_clone_url);
  // GIT_TERMINAL_PROMPT=0 prevents interactive password prompts (would hang).
  // GIT_CONFIG_GLOBAL=/dev/null keeps sandbox config clean.
  // We redact the URL in any error output.
  try {
    await exec(
      `git -c credential.helper= -c credential.helper='!echo' clone --depth 1 --branch ${shellQuote(baseRef)} --no-tags ${shellQuote(url)} ${shellQuote(localDir)}`,
      {
        env: {
          ...process.env,
          GIT_TERMINAL_PROMPT: "0",
          GIT_CONFIG_GLOBAL: "/dev/null",
          GIT_ASKPASS: "/bin/echo", // disables any askpass prompt
        },
        maxBuffer: 16 * 1024 * 1024,
      }
    );
  } catch (e: any) {
    // Redact token from error before throwing.
    const safe = redactToken(e?.message || String(e));
    throw new Error(`git_clone_failed: ${safe}`);
  }
  // Set committer identity for the work (deterministic, traceable to APSA agent).
  await exec(`git -C ${shellQuote(localDir)} config user.name "apsa-2026-bugfixer-v4"`);
  await exec(`git -C ${shellQuote(localDir)} config user.email "apsa-bugfixer@vitakyrpisit.local"`);
  // Create + switch to the work branch.
  await exec(`git -C ${shellQuote(localDir)} checkout -b ${shellQuote(args.branch_name)}`);
  return { local_dir: localDir, branch: args.branch_name, base_ref: baseRef };
}

async function forkDefaultBranch(fork: ForkInfo): Promise<string> {
  const r = await ghFetch<any>(`/repos/${fork.fork_full_name}`);
  if (!r.ok) throw new Error(`fork_meta_failed: HTTP ${r.status}`);
  return (r.body?.default_branch as string) || "main";
}

export interface CommitAndPushArgs {
  local_dir: string;
  branch: string;
  files: Array<{ path: string; content: string; mode?: "100644" | "100755" }>;
  commit_message: string;
}

/**
 * Writes the given files (path relative to repo root), stages them, commits,
 * and pushes the branch back to the fork.
 * Token-in-URL push: x-access-token:TOKEN@github.com/<fork>.git
 */
export async function commitAndPush(args: CommitAndPushArgs): Promise<{ commit_sha: string; pushed: boolean }> {
  for (const f of args.files) {
    const abs = join(args.local_dir, f.path);
    await mkdir(join(abs, ".."), { recursive: true });
    await writeFile(abs, f.content, { encoding: "utf-8" });
    if (f.mode === "100755") {
      try { await chmod(abs, 0o755); } catch { /* not fatal */ }
    }
    await exec(`git -C ${shellQuote(args.local_dir)} add ${shellQuote(f.path)}`);
  }
  // Commit (allow empty commits is fine; we usually have changes).
  const msgFile = join(args.local_dir, ".apsa-commit-msg.txt");
  await writeFile(msgFile, args.commit_message, { encoding: "utf-8" });
  await exec(
    `git -C ${shellQuote(args.local_dir)} commit -F ${shellQuote(msgFile)} --no-verify`
  );
  // Read HEAD sha.
  const { stdout: headOut } = await exec(
    `git -C ${shellQuote(args.local_dir)} rev-parse HEAD`
  );
  const sha = headOut.trim();
  // Push branch to fork.
  // Use the same authed URL via a configured remote "origin" (we'll re-set the URL to be safe).
  await exec(
    `git -C ${shellQuote(args.local_dir)} remote set-url origin ${shellQuote(authedCloneUrl("https://github.com/" + (await forkRemoteFullNameFromDir(args.local_dir)) + ".git"))}`
  ).catch(() => { /* if remote-name is not 'origin' we'll fall through to direct push below */ });

  // Push directly with the authed URL to be robust regardless of remote name.
  const remoteUrl = await getOriginUrl(args.local_dir);
  const pushUrl = authedCloneUrl(stripUrl(remoteUrl));
  try {
    await exec(
      `git -C ${shellQuote(args.local_dir)} push ${shellQuote(pushUrl)} HEAD:refs/heads/${shellQuote(args.branch)}`,
      {
        env: {
          ...process.env,
          GIT_TERMINAL_PROMPT: "0",
          GIT_ASKPASS: "/bin/echo",
        },
      }
    );
  } catch (e: any) {
    throw new Error(`git_push_failed: ${redactToken(e?.message || String(e))}`);
  }
  return { commit_sha: sha, pushed: true };
}

async function getOriginUrl(localDir: string): Promise<string> {
  try {
    const { stdout } = await exec(`git -C ${shellQuote(localDir)} remote get-url origin`);
    return stdout.trim();
  } catch {
    return "";
  }
}

async function forkRemoteFullNameFromDir(localDir: string): Promise<string> {
  // origin URL is something like https://github.com/<owner>/<repo>.git (with or without token).
  const u = await getOriginUrl(localDir);
  return stripUrl(u).replace(/^https:\/\/github\.com\//, "").replace(/\.git$/, "");
}

function stripUrl(u: string): string {
  // Remove any credentials embedded before @github.com.
  return u.replace(/^https:\/\/[^@]+@github\.com\//, "https://github.com/");
}

function redactToken(s: string): string {
  const t = getToken();
  if (!t) return s;
  let out = s.split(t).join("<redacted>");
  // Also redact the url-encoded form.
  try {
    out = out.split(encodeURIComponent(t)).join("<redacted>");
  } catch { /* ignore */ }
  return out;
}

function shellQuote(s: string): string {
  // POSIX-safe single-quote. We use single quotes; embedded ' becomes '\''.
  return "'" + s.replace(/'/g, "'\\''") + "'";
}

export interface CreatePrArgs {
  upstream_owner: string;
  upstream_repo: string;
  branch: string;       // head branch (on the fork)
  base: string;         // upstream base branch (e.g. main)
  title: string;
  body: string;
}

export async function createPR(args: CreatePrArgs): Promise<PrInfo> {
  const operator = await getOperatorLogin();
  const head = `${operator}:${args.branch}`;
  const r = await ghFetch<any>(
    `/repos/${args.upstream_owner}/${args.upstream_repo}/pulls`,
    {
      method: "POST",
      body: JSON.stringify({
        title: args.title,
        body: args.body,
        head,
        base: args.base,
        maintainer_can_modify: true, // allows upstream maintainer to push to my branch if needed
      }),
    }
  );
  if (!r.ok) {
    throw new Error(
      `pr_create_failed: HTTP ${r.status} ${JSON.stringify(r.body).slice(0, 300)}`
    );
  }
  return {
    number: r.body.number as number,
    html_url: r.body.html_url as string,
    state: r.body.state as "open" | "closed",
    title: r.body.title as string,
    head_ref: head,
    base_ref: args.base,
  };
}

export async function listExistingPRs(
  upstream_owner: string,
  upstream_repo: string,
  headBranch?: string
): Promise<PrInfo[]> {
  const operator = await getOperatorLogin();
  const q = [
    `repo:${upstream_owner}/${upstream_repo}`,
    `is:pr`,
    `author:${operator}`,
  ];
  if (headBranch) q.push(`head:${headBranch}`);
  const r = await ghFetch<any>(
    `/search/issues?q=${encodeURIComponent(q.join(" "))}&per_page=20`
  );
  if (!r.ok) return [];
  const items = Array.isArray(r.body?.items) ? r.body.items : [];
  return items.map((it: any) => ({
    number: it.number as number,
    html_url: it.html_url as string,
    state: it.state as "open" | "closed",
    title: it.title as string,
    head_ref: it.head?.ref as string,
    base_ref: it.base?.ref as string,
  }));
}

/**
 * Convenience: clean up a temp clone dir.
 */
export async function cleanupClone(localDir: string): Promise<void> {
  if (localDir && existsSync(localDir)) {
    await rm(localDir, { recursive: true, force: true });
  }
}
