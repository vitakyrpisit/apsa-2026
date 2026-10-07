"use client";

import { useCallback, useRef, useState } from "react";
import { Upload, FileJson } from "lucide-react";
import { toast } from "sonner";

interface ImportJsonButtonProps {
  /** Expected keys in the imported JSON; only these are read. */
  expectedKeys: string[];
  /** Called with the parsed (and key-filtered) object on success. */
  onImport: (data: Record<string, unknown>) => void;
}

/**
 * ImportJsonButton — imports a scenario from a JSON file via click-to-browse
 * OR drag-and-drop. Validates the file is valid JSON and contains at least
 * one expected key before invoking `onImport`. Shows sonner toasts for
 * success / parse errors / missing keys.
 *
 * The drop zone covers the whole button area (and expands while dragging
 * a file over it). Uses a hidden `<input type=file>` for the click path.
 */
export function ImportJsonButton({
  expectedKeys,
  onImport,
}: ImportJsonButtonProps) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(
    (file: File) => {
      if (!file.name.endsWith(".json") && file.type !== "application/json") {
        toast.error("Invalid file type", {
          description: "Please select a .json file.",
        });
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const text = String(e.target?.result ?? "");
          const parsed = JSON.parse(text) as Record<string, unknown>;
          const found = expectedKeys.filter((k) => k in parsed);
          if (found.length === 0) {
            toast.error("Invalid scenario file", {
              description: `Expected keys like ${expectedKeys.slice(0, 3).join(", ")} — none found.`,
            });
            return;
          }
          onImport(parsed);
          toast.success("Scenario imported", {
            description: `${found.length} value${found.length === 1 ? "" : "s"} restored from ${file.name}.`,
          });
        } catch {
          toast.error("Could not parse JSON", {
            description: "The file is not valid JSON.",
          });
        }
      };
      reader.onerror = () => {
        toast.error("Could not read file", {
          description: "Try again or paste the values manually.",
        });
      };
      reader.readAsText(file);
    },
    [expectedKeys, onImport],
  );

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const file = e.dataTransfer.files?.[0];
      if (file) handleFile(file);
    },
    [handleFile],
  );

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(true);
  }, []);

  const onDragLeave = useCallback(() => setDragging(false), []);

  return (
    <>
      <button
        onClick={() => inputRef.current?.click()}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        title="Import a scenario from a JSON file (or drag-drop)"
        className={`px-2.5 py-1 text-xs font-mono rounded-md border flex items-center gap-1.5 transition-all ${
          dragging
            ? "bg-emerald-950 border-emerald-500 text-emerald-300 ring-2 ring-emerald-500/30 scale-105"
            : "bg-slate-800 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700"
        }`}
      >
        {dragging ? (
          <>
            <FileJson className="w-3 h-3" />
            Drop here
          </>
        ) : (
          <>
            <Upload className="w-3 h-3" />
            Import
          </>
        )}
      </button>
      <input
        ref={inputRef}
        type="file"
        accept=".json,application/json"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
          // Reset so the same file can be re-selected.
          e.target.value = "";
        }}
      />
    </>
  );
}
