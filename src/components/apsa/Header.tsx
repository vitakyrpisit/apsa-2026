'use client';

import React, { useState } from 'react';
import { OFFICIAL_PAYOUT_ADDRESS } from '@/lib/apsa/empirical-data';
import { Check, Copy, ExternalLink, Download, Terminal } from 'lucide-react';
import { toast } from 'sonner';

interface HeaderProps {
  activeNetwork: 'base-mainnet' | 'base-sepolia';
  onNetworkChange: (network: 'base-mainnet' | 'base-sepolia') => void;
  onExportReport: () => void;
  onOpenTestHarness: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  activeNetwork,
  onNetworkChange,
  onExportReport,
  onOpenTestHarness
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(OFFICIAL_PAYOUT_ADDRESS);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      toast.success("Payout address copied", {
        description: `${OFFICIAL_PAYOUT_ADDRESS.slice(0, 10)}…${OFFICIAL_PAYOUT_ADDRESS.slice(-6)}`,
      });
    } catch {
      toast.error("Could not copy address", {
        description: "Copy it manually from the address bar.",
      });
    }
  };

  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">

          {/* Brand & Context */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-950 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-mono font-bold text-sm">
              402
            </div>
            <div>
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <span className="font-semibold text-slate-200">X402 EXPERIMENT</span>
                <span aria-hidden="true">·</span>
                <span>Base L2 USDC Standard</span>
                <span aria-hidden="true">·</span>
                <span className="text-emerald-400 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  Active Audit
                </span>
              </div>
              <h1 className="text-sm sm:text-base font-bold text-white tracking-tight">
                Autonomous Profit Experiment &amp; Empirical Workbench
              </h1>
            </div>
          </div>

          {/* Target Address & Network Controls */}
          <div className="flex flex-wrap items-center gap-3 w-full md:w-auto justify-between md:justify-end">

            {/* Multi-Rail Badges */}
            <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 bg-slate-900 border border-slate-800 rounded-md text-[11px] font-mono">
              <span className="text-slate-400">RAILS:</span>
              <span className="text-emerald-300 font-semibold" title="EVM: 0x829f877daAb94D766BB2b8511ad486C40f2C2BDA">EVM (0x829f)</span>
              <span className="text-slate-600">·</span>
              <span className="text-purple-300 font-semibold" title="Solana: EyTxSdVtku7QtbwgntLvUwyxMvraJyAxoPoZ8ALdG6qL">SOL (EyTx)</span>
              <span className="text-slate-600">·</span>
              <span className="text-red-300 font-semibold" title="Tron: TVVhpdHEg1ZgvPjJNSe2P28bhUDE4m85ZX">TRX (TVVh)</span>
              <span className="text-slate-600">·</span>
              <span className="text-amber-300 font-semibold" title="Bitcoin: bc1qaedy7cmquxjlmkezlxlytkrecv0ufku970tk9c">BTC (bc1q)</span>
            </div>

            {/* Payout Address Box */}
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900 border border-slate-800 text-xs">
              <span className="text-slate-400 text-[11px] uppercase tracking-wider font-mono">Payout (Receive-Only):</span>
              <span className="font-mono text-emerald-300 font-medium">
                {OFFICIAL_PAYOUT_ADDRESS.slice(0, 6)}...{OFFICIAL_PAYOUT_ADDRESS.slice(-4)}
              </span>
              <button
                onClick={handleCopy}
                title="Copy full receive-only payout address"
                className="text-slate-400 hover:text-white transition-colors p-1"
                aria-label="Copy payout address"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
              <a
                href={`https://${activeNetwork === 'base-sepolia' ? 'sepolia.' : ''}basescan.org/address/${OFFICIAL_PAYOUT_ADDRESS}`}
                target="_blank"
                rel="noreferrer"
                title="View on BaseScan"
                className="text-slate-400 hover:text-white transition-colors p-1"
              >
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>

            {/* Network Selector Tabs */}
            <div className="flex items-center gap-1 p-1 bg-slate-900 border border-slate-800 rounded-md">
              <button
                onClick={() => onNetworkChange('base-mainnet')}
                className={`px-2.5 py-1 text-xs font-mono rounded transition-colors ${
                  activeNetwork === 'base-mainnet'
                    ? 'bg-emerald-600 text-white font-medium shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Base Mainnet
              </button>
              <button
                onClick={() => onNetworkChange('base-sepolia')}
                className={`px-2.5 py-1 text-xs font-mono rounded transition-colors ${
                  activeNetwork === 'base-sepolia'
                    ? 'bg-emerald-600 text-white font-medium shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Base Sepolia
              </button>
            </div>

            {/* Direct HTTP Download Button (Works 100% in iframes and popups) */}
            <a
              href="/api/download/bundle.zip"
              download="APSA-2026-COMPLETE-AUTONOMOUS-MONEY-HUNTER.zip"
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-1.5 text-xs font-semibold rounded-md bg-amber-600 hover:bg-amber-500 text-white font-mono transition-colors flex items-center gap-1.5 shadow-sm cursor-pointer no-underline"
              title="Скачать полный архив проекта со всеми скриптами, кошельками и протоколами (.ZIP)"
            >
              <Download className="w-3.5 h-3.5" />
              Скачать Архив (.ZIP)
            </a>

            <button
              onClick={onOpenTestHarness}
              className="px-3 py-1.5 text-xs font-medium rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors flex items-center gap-1.5"
            >
              <Terminal className="w-3.5 h-3.5 text-emerald-400" />
              Run 402 Test
            </button>

            <button
              onClick={onExportReport}
              className="px-3 py-1.5 text-xs font-medium rounded-md bg-emerald-600 hover:bg-emerald-500 text-white transition-colors flex items-center gap-1.5"
            >
              <Download className="w-3.5 h-3.5" />
              Отчет (.MD)
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
