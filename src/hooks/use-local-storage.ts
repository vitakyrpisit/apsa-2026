"use client";

import { useCallback, useEffect, useRef, useState } from "react";

/**
 * useLocalStorage — a useState-like hook that transparently persists the
 * value to `localStorage` under the given key.
 *
 * Hydration strategy: the initial state is read synchronously from
 * localStorage inside a lazy `useState` initializer (client-only; on the
 * server `window` is undefined so the initialValue is used). This avoids
 * the `set-state-in-effect` lint violation AND prevents the hydration
 * flash where the initial value briefly replaces the persisted one.
 *
 * Tolerates JSON parse failures, QuotaExceeded errors, and SSR. Syncs
 * across browser tabs via the `storage` event.
 */
export function useLocalStorage<T>(
  key: string,
  initialValue: T,
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  const [stored, setStored] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;
    try {
      const item = window.localStorage.getItem(key);
      return item !== null ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  // Keep a ref of the key so the storage event handler (which only re-runs
  // on key/initialValue changes) can read the latest key without being
  // re-registered on every render. The ref is updated in an effect, not
  // during render.
  const keyRef = useRef(key);
  useEffect(() => {
    keyRef.current = key;
  }, [key]);

  // Cross-tab sync.
  useEffect(() => {
    const handler = (e: StorageEvent) => {
      if (e.key !== keyRef.current) return;
      if (e.newValue === null) {
        setStored(initialValue);
        return;
      }
      try {
        setStored(JSON.parse(e.newValue) as T);
      } catch {
        // ignore malformed cross-tab payloads
      }
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, [initialValue]);

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStored((prev) => {
        const next =
          typeof value === "function"
            ? (value as (prev: T) => T)(prev)
            : value;
        try {
          window.localStorage.setItem(keyRef.current, JSON.stringify(next));
        } catch {
          // QuotaExceeded or unavailable — keep in-memory state only.
        }
        return next;
      });
    },
    [],
  );

  const remove = useCallback(() => {
    try {
      window.localStorage.removeItem(keyRef.current);
    } catch {
      // ignore
    }
    setStored(initialValue);
  }, [initialValue]);

  return [stored, setValue, remove];
}
