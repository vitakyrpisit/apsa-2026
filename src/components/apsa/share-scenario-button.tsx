"use client";

import { useState } from "react";
import { Share2, Check, Link as LinkIcon } from "lucide-react";
import { toast } from "sonner";

interface ShareScenarioButtonProps {
  /** The serializable key-value pairs to encode into the URL hash. */
  value: Record<string, string | number | boolean>;
}

/**
 * ShareScenarioButton — copies a shareable URL (with the current scenario
 * encoded into the hash) to the clipboard. Pasting the URL into another
 * browser/tab restores the exact slider configuration.
 *
 * Compact and self-contained: renders a single button with a copy/check
 * state transition + a sonner toast on success.
 */
export function ShareScenarioButton({ value }: ShareScenarioButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    // Build the hash string.
    const pairs: string[] = [];
    for (const [k, v] of Object.entries(value)) {
      if (v === undefined || v === null || v === "") continue;
      pairs.push(`${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`);
    }
    const hash = pairs.length ? `#${pairs.join("&")}` : "";
    const url = `${window.location.origin}${window.location.pathname}${window.location.search}${hash}`;

    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      toast.success("Share link copied to clipboard", {
        description: "Paste it anywhere to restore this exact scenario.",
      });
    } catch {
      // Fallback for non-secure contexts: select-and-copy a hidden input.
      const input = document.createElement("input");
      input.value = url;
      document.body.appendChild(input);
      input.select();
      try {
        document.execCommand("copy");
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
        toast.success("Share link copied", {
          description: "Paste it anywhere to restore this exact scenario.",
        });
      } catch {
        toast.error("Could not copy link", {
          description: "Copy it manually from the address bar after pressing Share.",
        });
      } finally {
        document.body.removeChild(input);
      }
    }
  };

  return (
    <button
      onClick={handleShare}
      title="Copy a shareable link to this scenario"
      className={`px-2.5 py-1 text-xs font-mono rounded-md border flex items-center gap-1.5 transition-all ${
        copied
          ? "bg-emerald-950 border-emerald-700 text-emerald-300"
          : "bg-slate-800 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700"
      }`}
    >
      {copied ? (
        <>
          <Check className="w-3 h-3" />
          Copied
        </>
      ) : (
        <>
          <Share2 className="w-3 h-3" />
          Share
          <LinkIcon className="w-2.5 h-2.5 opacity-60" />
        </>
      )}
    </button>
  );
}
