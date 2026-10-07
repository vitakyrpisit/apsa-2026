"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";

interface FadeInProps {
  children: ReactNode;
  delay?: number;
  duration?: number;
  y?: number;
  className?: string;
}

/**
 * FadeIn — a reusable entrance-animation wrapper using framer-motion.
 * Fades + slides up slightly. Respects `prefers-reduced-motion` via
 * framer-motion's built-in support.
 *
 * Usage: `<FadeIn delay={0.1}><Card>...</Card></FadeIn>`
 */
export function FadeIn({
  children,
  delay = 0,
  duration = 0.35,
  y = 12,
  className,
}: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration, delay, ease: [0.22, 1, 0.36, 1] }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/**
 * StaggeredFadeIn — for lists of cards. Wraps children in a stagger
 * container so each child fades in sequentially.
 */
export function StaggeredFadeIn({
  children,
  stagger = 0.06,
  className,
}: {
  children: ReactNode[];
  stagger?: number;
  className?: string;
}) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: {
          transition: { staggerChildren: stagger },
        },
      }}
      className={className}
    >
      {children.map((child, i) => (
        <motion.div
          key={i}
          variants={{
            hidden: { opacity: 0, y: 12 },
            visible: {
              opacity: 1,
              y: 0,
              transition: { duration: 0.3, ease: [0.22, 1, 0.36, 1] },
            },
          }}
        >
          {child}
        </motion.div>
      ))}
    </motion.div>
  );
}
