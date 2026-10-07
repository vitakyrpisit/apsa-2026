"use client";

import { useEffect, useState } from "react";

export interface SubSection {
  id: string;
  label: string;
  icon?: React.ComponentType<{ className?: string }>;
}

interface SubSectionNavProps {
  sections: SubSection[];
  /** Optional heading rendered to the left of the nav pills. */
  title?: string;
}

/**
 * SubSectionNav — a sticky horizontal pill-nav for long tab pages (e.g. the
 * Economics tab now has scenario cards + sliders + 3 charts + an audit
 * table). Clicking a pill smooth-scrolls to that section; the active pill
 * tracks scroll position via IntersectionObserver.
 *
 * The nav itself sticks to the top of the scroll container (just below the
 * global LiveTicker) so it stays visible while browsing a long page.
 */
export function SubSectionNav({ sections, title }: SubSectionNavProps) {
  const [active, setActive] = useState<string>(sections[0]?.id ?? "");

  // Track which section is in view.
  useEffect(() => {
    const els = sections
      .map((s) => document.getElementById(s.id))
      .filter((el): el is HTMLElement => el !== null);
    if (els.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        // Pick the topmost intersecting entry.
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) {
          setActive(visible[0].target.id);
        }
      },
      {
        // Trigger when the section's top crosses ~25% from the viewport top,
        // accounting for the sticky header (57px) + ticker (~40px) + this
        // nav (~44px) ≈ 150px offset.
        rootMargin: "-150px 0px -60% 0px",
        threshold: 0,
      },
    );

    els.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [sections]);

  const handleClick = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      // Adjust for sticky offset after the browser settles the scroll.
      setTimeout(() => {
        const top = el.getBoundingClientRect().top + window.scrollY - 150;
        window.scrollTo({ top, behavior: "smooth" });
      }, 50);
    }
  };

  return (
    <div className="sticky top-[100px] z-20 -mx-4 px-4 py-2.5 bg-slate-950/85 backdrop-blur-md border-y border-slate-800/80 mb-2">
      <div className="flex items-center gap-3 overflow-x-auto scrollbar-none">
        {title && (
          <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 flex-shrink-0 pr-2 border-r border-slate-800">
            {title}
          </span>
        )}
        {sections.map((s) => {
          const Icon = s.icon;
          const isActive = active === s.id;
          return (
            <button
              key={s.id}
              onClick={() => handleClick(s.id)}
              aria-current={isActive ? "true" : undefined}
              className={`px-3 py-1.5 rounded-full text-[11px] font-mono whitespace-nowrap transition-all flex items-center gap-1.5 flex-shrink-0 ${
                isActive
                  ? "bg-emerald-600 text-white shadow-sm ring-1 ring-emerald-400/40"
                  : "bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800"
              }`}
            >
              {Icon && <Icon className="w-3 h-3" />}
              {s.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
