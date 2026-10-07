"use client";

/**
 * URL-hash encode/decode utilities for shareable scenario state.
 *
 * The hash format is a compact `#key=value&key=value` query string, stripped
 * of empty values so a default-state URL is just `#`.
 *
 * These are low-level helpers — components read the hash on mount and write
 * it via a debounced effect.
 */

interface UrlHashCodec<T extends Record<string, string | number | boolean>> {
  parse: (hash: string) => Partial<T>;
  stringify: (value: Partial<T>) => string;
}

function defaultCodec<T extends Record<string, string | number | boolean>>(): UrlHashCodec<T> {
  return {
    parse: (hash) => {
      const clean = hash.replace(/^#/, "");
      if (!clean) return {};
      const out: Record<string, string> = {};
      for (const pair of clean.split("&")) {
        const [k, v] = pair.split("=");
        if (k && v !== undefined) out[decodeURIComponent(k)] = decodeURIComponent(v);
      }
      return out as Partial<T>;
    },
    stringify: (value) => {
      const pairs: string[] = [];
      for (const [k, v] of Object.entries(value)) {
        if (v === undefined || v === null || v === "") continue;
        pairs.push(`${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`);
      }
      return pairs.length ? `#${pairs.join("&")}` : "";
    },
  };
}

/**
 * Read the URL hash once (client-only) and return the parsed partial.
 */
export function readUrlHash<T extends Record<string, string | number | boolean>>(): Partial<T> {
  if (typeof window === "undefined") return {};
  return defaultCodec<T>().parse(window.location.hash);
}

/**
 * Write a partial value to the URL hash, replacing the existing hash.
 * Uses `history.replaceState` to avoid polluting the back-button stack.
 */
export function writeUrlHash<T extends Record<string, string | number | boolean>>(
  value: Partial<T>,
): void {
  if (typeof window === "undefined") return;
  const hash = defaultCodec<T>().stringify(value);
  const url = `${window.location.pathname}${window.location.search}${hash}`;
  window.history.replaceState(null, "", url);
}
