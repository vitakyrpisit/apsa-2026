"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";
import type { OnChainWalletStatus } from "@/lib/apsa/base-rpc";
import type { TestResultItem } from "@/lib/apsa/test-suite";

interface SuiteState {
  loading: boolean;
  passed: boolean | null;
  results: TestResultItem[];
  lastRunAt: number | null;
  /** Re-run the suite (debounced to one in-flight call). */
  rerun: () => void;
}

interface WalletState {
  status: OnChainWalletStatus | null;
  loading: boolean;
  lastRunAt: number | null;
  refresh: () => void;
}

interface ApsaDataContextValue {
  suite: SuiteState;
  wallet: WalletState;
}

const ApsaDataContext = createContext<ApsaDataContextValue | null>(null);

const SUITE_TTL_MS = 60_000; // re-use a suite result for up to 60s
const WALLET_TTL_MS = 15_000; // re-use a wallet status for up to 15s

/**
 * ApsaDataProvider — a single source of truth for the two slow server
 * queries (12-test suite + on-chain wallet status). Both the page-level
 * LiveTicker/MetricCards and the Mission tab's RealRevenueHarness consume
 * this context so the suite only runs ONCE per TTL window instead of
 * once-per-consumer.
 *
 * Fetches are debounced via an in-flight ref so concurrent mounts don't
 * trigger duplicate POST /api/test-suite calls.
 */
export function ApsaDataProvider({ children }: { children: ReactNode }) {
  const [suiteLoading, setSuiteLoading] = useState(false);
  const [suitePassed, setSuitePassed] = useState<boolean | null>(null);
  const [suiteResults, setSuiteResults] = useState<TestResultItem[]>([]);
  const [suiteLastRunAt, setSuiteLastRunAt] = useState<number | null>(null);

  const [walletStatus, setWalletStatus] = useState<OnChainWalletStatus | null>(
    null,
  );
  const [walletLoading, setWalletLoading] = useState(false);
  const [walletLastRunAt, setWalletLastRunAt] = useState<number | null>(null);

  const suiteInFlight = useRef<Promise<void> | null>(null);
  const walletInFlight = useRef<Promise<void> | null>(null);

  const runSuite = useCallback(() => {
    // Re-use a fresh-enough result.
    if (suiteLastRunAt && Date.now() - suiteLastRunAt < SUITE_TTL_MS) {
      return Promise.resolve();
    }
    if (suiteInFlight.current) return suiteInFlight.current;

    setSuiteLoading(true);
    const p = (async () => {
      try {
        const res = await fetch("/api/test-suite", { method: "POST" });
        const data = (await res.json()) as {
          passed: boolean;
          count: number;
          results: TestResultItem[];
        };
        setSuitePassed(data.passed);
        setSuiteResults(data.results);
        setSuiteLastRunAt(Date.now());
      } catch {
        setSuitePassed(false);
        setSuiteLastRunAt(Date.now());
      } finally {
        setSuiteLoading(false);
        suiteInFlight.current = null;
      }
    })();
    suiteInFlight.current = p;
    return p;
  }, [suiteLastRunAt]);

  const runWallet = useCallback(
    (network: "base-mainnet" | "base-sepolia" = "base-mainnet") => {
      if (walletLastRunAt && Date.now() - walletLastRunAt < WALLET_TTL_MS) {
        return Promise.resolve();
      }
      if (walletInFlight.current) return walletInFlight.current;

      setWalletLoading(true);
      const p = (async () => {
        try {
          const res = await fetch(
            `/api/onchain/status?network=${network}`,
          );
          const data = (await res.json()) as OnChainWalletStatus;
          setWalletStatus(data);
          setWalletLastRunAt(Date.now());
        } catch {
          // keep previous state; provider is resilient to transient failures
        } finally {
          setWalletLoading(false);
          walletInFlight.current = null;
        }
      })();
      walletInFlight.current = p;
      return p;
    },
    [walletLastRunAt],
  );

  // Initial fetch on mount.
  useEffect(() => {
    runSuite();
    runWallet("base-mainnet");
    // The polling interval for the wallet is handled by LiveOnChainTracker
    // when the Scanner tab is open; the provider just primes the cache.
  }, [runSuite, runWallet]);

  const value: ApsaDataContextValue = {
    suite: {
      loading: suiteLoading,
      passed: suitePassed,
      results: suiteResults,
      lastRunAt: suiteLastRunAt,
      rerun: () => {
        // Force a fresh run by clearing the timestamp gate, then run.
        setSuiteLastRunAt(null);
        // Defer the actual fetch to the next tick so state has flushed.
        setTimeout(() => runSuite(), 0);
      },
    },
    wallet: {
      status: walletStatus,
      loading: walletLoading,
      lastRunAt: walletLastRunAt,
      refresh: () => {
        setWalletLastRunAt(null);
        setTimeout(() => runWallet("base-mainnet"), 0);
      },
    },
  };

  return (
    <ApsaDataContext.Provider value={value}>
      {children}
    </ApsaDataContext.Provider>
  );
}

export function useApsaData(): ApsaDataContextValue {
  const ctx = useContext(ApsaDataContext);
  if (!ctx) {
    throw new Error("useApsaData must be used within an ApsaDataProvider");
  }
  return ctx;
}
