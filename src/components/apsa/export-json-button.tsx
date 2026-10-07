"use client";

import { useState } from "react";
import { FileJson, Check } from "lucide-react";
import { toast } from "sonner";

interface ExportJsonButtonProps {
  /** The serializable object to export as JSON. */
  value: Record<string, unknown>;
  /** Filename without extension. */
  filename: string;
}

/**
 * ExportJsonButton — downloads a JSON file containing the provided value.
 * Uses a Blob + temporary anchor element. Shows a check state + sonner
 * toast on success.
 */
export function ExportJsonButton({ value, filename }: ExportJsonButtonProps) {
  const [exported, setExported] = useState(false);

  const handleExport = () => {
    try {
      const json = JSON.stringify(value, null, 2);
      const blob = new Blob([json], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${filename}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      setExported(true);
      setTimeout(() => setExported(false), 2000);
      toast.success("Scenario exported as JSON", {
        description: `${filename}.json downloaded.`,
      });
    } catch {
      toast.error("Export failed", {
        description: "Could not generate the JSON file.",
      });
    }
  };

  return (
    <button
      onClick={handleExport}
      title="Export this scenario as a JSON file"
      className={`px-2.5 py-1 text-xs font-mono rounded-md border flex items-center gap-1.5 transition-all ${
        exported
          ? "bg-emerald-950 border-emerald-700 text-emerald-300"
          : "bg-slate-800 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700"
      }`}
    >
      {exported ? (
        <>
          <Check className="w-3 h-3" />
          Exported
        </>
      ) : (
        <>
          <FileJson className="w-3 h-3" />
          JSON
        </>
      )}
    </button>
  );
}
