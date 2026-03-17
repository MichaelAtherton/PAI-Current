# Reveal Mode Workflow

Step-by-step guide to building a dark-canvas cinematic reveal interface — the kind of UI that feels like a briefing screen or theatrical presentation.

## Component Architecture

```
RevealModePage
├── RevealCanvas          — Full-screen dark container, manages global timing
│   ├── CinematicHeading  — Title with blur-to-sharp materialization
│   ├── StreamingSection  — Section that reveals its children with stagger
│   │   ├── CinematicText — Individual text blocks with reveal animation
│   │   └── RevealInput   — Dark-themed input with gold accent
│   └── AssemblyTimeline  — Coordinated multi-section orchestrator
└── GlowingSection        — Optional ambient border effect wrapper
```

## Animation Timing Reference

| Element | Duration | Delay | Easing |
|---------|----------|-------|--------|
| Page container fade-in | 400ms | 0ms | `ease-out` |
| Heading blur-to-sharp | 800ms | 200ms | `[0.25, 0.46, 0.45, 0.94]` |
| Section stagger (between children) | — | 120ms per child | — |
| Text block reveal | 600ms | staggered | `[0.22, 1, 0.36, 1]` |
| Input field appearance | 500ms | after last text | `ease-out` |
| Glow border pulse | 2000ms | continuous | `ease-in-out` (loop) |
| Exit animations | 300ms | 0ms | `ease-in` |

### Easing Curves

- **Cinematic reveal:** `[0.25, 0.46, 0.45, 0.94]` — smooth deceleration, feels deliberate
- **Snappy settle:** `[0.22, 1, 0.36, 1]` — overshoots slightly, natural landing
- **Soft fade:** `ease-out` — simple, no overshoot

## Step-by-Step Build Process

### Step 1: Create the Canvas

The RevealCanvas is a full-viewport dark container. It fades in on mount and manages the overall reveal timeline.

### Step 2: Add Heading with Blur Materialization

The heading appears first: opacity 0 + blur(12px) -> opacity 1 + blur(0). This is the signature cinematic effect.

### Step 3: Add Staggered Content Sections

Each section's children appear one at a time with 120ms stagger. Use `motion.div` with `variants` and `staggerChildren`.

### Step 4: Wire Up Data

Use mock data during development. Replace with real data sources later. The animation timing should not depend on data fetching — animate whatever is available.

### Step 5: Add Interactive Elements

Inputs and buttons appear last in the reveal sequence. They use the same blur-to-sharp pattern but with shorter duration (500ms).

### Step 6: Optimize for Projector / Large Display

See optimization guidelines below.

## Complete Example: RevealModePage

```tsx
"use client"

import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "motion/react"

// ── Types ──────────────────────────────────────────────
interface BriefingSection {
  id: string
  label: string
  content: string
}

interface RevealModePageProps {
  title?: string
  subtitle?: string
  sections?: BriefingSection[]
}

// ── Animation Variants ────────────────────────────────
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.4, ease: "easeOut", staggerChildren: 0.12 },
  },
  exit: { opacity: 0, transition: { duration: 0.3, ease: "easeIn" } },
}

const headingVariants = {
  hidden: { opacity: 0, filter: "blur(12px)", y: 20 },
  visible: {
    opacity: 1,
    filter: "blur(0px)",
    y: 0,
    transition: { duration: 0.8, ease: [0.25, 0.46, 0.45, 0.94] },
  },
}

const sectionVariants = {
  hidden: { opacity: 0, filter: "blur(8px)", y: 12 },
  visible: {
    opacity: 1,
    filter: "blur(0px)",
    y: 0,
    transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] },
  },
}

const glowVariants = {
  idle: {
    boxShadow: "0 0 20px 2px rgba(251, 191, 36, 0.05)",
  },
  glow: {
    boxShadow: "0 0 40px 8px rgba(251, 191, 36, 0.15)",
    transition: {
      duration: 2,
      ease: "easeInOut",
      repeat: Infinity,
      repeatType: "reverse" as const,
    },
  },
}

// ── Mock Data ─────────────────────────────────────────
const defaultSections: BriefingSection[] = [
  {
    id: "status",
    label: "STATUS",
    content: "All systems operational. Last sync 4 minutes ago.",
  },
  {
    id: "priority",
    label: "PRIORITY",
    content:
      "Three items require attention. Revenue forecast updated. Team standup moved to 14:00.",
  },
  {
    id: "insight",
    label: "INSIGHT",
    content:
      "Conversion rate increased 12% after the landing page update shipped Thursday.",
  },
  {
    id: "next",
    label: "NEXT ACTION",
    content: "Review the Q2 planning document before the 15:00 strategy call.",
  },
]

// ── Component ─────────────────────────────────────────
export default function RevealModePage({
  title = "DAILY BRIEFING",
  subtitle = "March 10, 2026 — Morning",
  sections = defaultSections,
}: RevealModePageProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [commandInput, setCommandInput] = useState("")

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen bg-black text-neutral-100 flex items-center justify-center p-8">
      <AnimatePresence>
        {isVisible && (
          <motion.div
            className="w-full max-w-2xl space-y-8"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
          >
            {/* ── Heading ── */}
            <motion.div variants={headingVariants} className="space-y-2">
              <h1 className="text-3xl font-light tracking-[0.2em] text-amber-400">
                {title}
              </h1>
              <p className="text-sm text-neutral-500 tracking-widest uppercase">
                {subtitle}
              </p>
              <div className="h-px bg-gradient-to-r from-amber-400/40 via-amber-400/10 to-transparent mt-4" />
            </motion.div>

            {/* ── Sections ── */}
            {sections.map((section) => (
              <motion.div
                key={section.id}
                variants={sectionVariants}
                className="space-y-1"
              >
                <span className="text-[11px] font-medium tracking-[0.15em] text-amber-400/70 uppercase">
                  {section.label}
                </span>
                <p className="text-neutral-300 text-base leading-relaxed">
                  {section.content}
                </p>
              </motion.div>
            ))}

            {/* ── Glow Divider ── */}
            <motion.div
              variants={glowVariants}
              initial="idle"
              animate="glow"
              className="h-px bg-amber-400/20 rounded-full"
            />

            {/* ── Command Input ── */}
            <motion.div variants={sectionVariants}>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-amber-400/50 text-sm">
                  {">"}
                </span>
                <input
                  type="text"
                  value={commandInput}
                  onChange={(e) => setCommandInput(e.target.value)}
                  placeholder="Enter command..."
                  className="w-full bg-neutral-950 border border-neutral-800 rounded-md py-2.5 pl-8 pr-4 text-sm text-neutral-200 placeholder:text-neutral-600 focus:outline-none focus:border-amber-400/40 focus:ring-1 focus:ring-amber-400/20 transition-colors"
                />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
```

## Projector / Large Display Optimization

When building for projector or large-screen display:

1. **Increase font sizes.** Body text should be at least `text-lg` (18px). Headings at `text-4xl` or larger. Tracking wider: `tracking-[0.25em]`.
2. **Boost contrast.** Use `text-neutral-100` not `text-neutral-300` for body. Labels at `text-amber-400` not `text-amber-400/70`.
3. **Slow down animations.** Multiply all durations by 1.5x. Stagger delays to 180ms. Audiences need more time to absorb projected content.
4. **Increase spacing.** Use `space-y-12` between sections instead of `space-y-8`. Add `py-16` to the page container.
5. **Avoid thin lines.** The `h-px` divider should become `h-0.5` with higher opacity.
6. **Test at distance.** If you can't read it from 3 meters away, the font is too small.

## Mock Data Pattern

Always start with typed mock data so animations can be developed independently of data sources:

```tsx
interface MockData {
  sections: BriefingSection[]
  metadata: { timestamp: string; status: "live" | "cached" }
}

const MOCK: MockData = {
  sections: [
    { id: "1", label: "SECTION LABEL", content: "Section content here." },
  ],
  metadata: { timestamp: new Date().toISOString(), status: "cached" },
}
```

Swap to real data by replacing the default prop value or passing data from a server component / API route. The animation layer should never know or care where the data came from.
