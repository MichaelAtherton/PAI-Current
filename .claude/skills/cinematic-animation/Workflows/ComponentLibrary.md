# Component Library

Ready-to-use cinematic animation components. Each is self-contained, copy-pasteable, and built for React 19 + Tailwind CSS + `motion` package.

## Install

```bash
npm install motion
```

All components use `"use client"` directive for Next.js App Router compatibility.

---

## 1. CinematicHeading

Blur-to-sharp text materialization with optional subtitle and gradient divider.

### Props

```tsx
interface CinematicHeadingProps {
  title: string
  subtitle?: string
  delay?: number
  className?: string
}
```

### Component

```tsx
"use client"

import { motion } from "motion/react"

interface CinematicHeadingProps {
  title: string
  subtitle?: string
  delay?: number
  className?: string
}

export function CinematicHeading({
  title,
  subtitle,
  delay = 0,
  className = "",
}: CinematicHeadingProps) {
  return (
    <motion.div
      initial={{ opacity: 0, filter: "blur(12px)", y: 20 }}
      animate={{ opacity: 1, filter: "blur(0px)", y: 0 }}
      transition={{
        duration: 0.8,
        delay,
        ease: [0.25, 0.46, 0.45, 0.94],
      }}
      className={`space-y-2 ${className}`}
    >
      <h1 className="text-3xl font-light tracking-[0.2em] text-amber-400">
        {title}
      </h1>
      {subtitle && (
        <p className="text-sm text-neutral-500 tracking-widest uppercase">
          {subtitle}
        </p>
      )}
      <div className="h-px bg-gradient-to-r from-amber-400/40 via-amber-400/10 to-transparent mt-4" />
    </motion.div>
  )
}
```

### Usage

```tsx
<CinematicHeading
  title="SYSTEM STATUS"
  subtitle="March 10, 2026 — 09:00 UTC"
  delay={0.2}
/>
```

---

## 2. StreamingParagraph

Word-by-word text reveal with blur entrance. Works with both pre-written text and dynamically growing text.

### Props

```tsx
interface StreamingParagraphProps {
  text: string
  wordsPerSecond?: number
  className?: string
  onComplete?: () => void
}
```

### Component

```tsx
"use client"

import { useState, useEffect, useRef } from "react"
import { motion } from "motion/react"

interface StreamingParagraphProps {
  text: string
  wordsPerSecond?: number
  className?: string
  onComplete?: () => void
}

export function StreamingParagraph({
  text,
  wordsPerSecond = 14,
  className = "",
  onComplete,
}: StreamingParagraphProps) {
  const [visibleCount, setVisibleCount] = useState(0)
  const words = text.split(" ")
  const completedRef = useRef(false)

  useEffect(() => {
    setVisibleCount(0)
    completedRef.current = false
  }, [text])

  useEffect(() => {
    if (visibleCount >= words.length) {
      if (!completedRef.current) {
        completedRef.current = true
        onComplete?.()
      }
      return
    }

    const timeout = setTimeout(() => {
      setVisibleCount((c) => c + 1)
    }, 1000 / wordsPerSecond)

    return () => clearTimeout(timeout)
  }, [visibleCount, words.length, wordsPerSecond, onComplete])

  return (
    <p className={`text-neutral-300 leading-relaxed ${className}`}>
      {words.slice(0, visibleCount).map((word, i) => (
        <motion.span
          key={`${word}-${i}`}
          initial={{ opacity: 0, filter: "blur(4px)" }}
          animate={{ opacity: 1, filter: "blur(0px)" }}
          transition={{ duration: 0.2, ease: "easeOut" }}
          className="inline-block mr-[0.25em]"
        >
          {word}
        </motion.span>
      ))}
      {visibleCount < words.length && (
        <motion.span
          className="inline-block w-0.5 h-[1.1em] bg-amber-400/60 align-text-bottom ml-0.5"
          animate={{ opacity: [1, 0] }}
          transition={{ duration: 0.6, repeat: Infinity, repeatType: "reverse" }}
        />
      )}
    </p>
  )
}
```

### Usage

```tsx
<StreamingParagraph
  text="The analysis is complete. Revenue grew 14% quarter-over-quarter driven primarily by enterprise expansion."
  wordsPerSecond={12}
  onComplete={() => console.log("Done streaming")}
/>
```

---

## 3. GlowingSection

Container with an animated ambient glow border. Use to draw focus to a section.

### Props

```tsx
interface GlowingSectionProps {
  children: React.ReactNode
  color?: "amber" | "blue" | "emerald" | "red"
  intensity?: "low" | "medium" | "high"
  className?: string
}
```

### Component

```tsx
"use client"

import { motion } from "motion/react"

interface GlowingSectionProps {
  children: React.ReactNode
  color?: "amber" | "blue" | "emerald" | "red"
  intensity?: "low" | "medium" | "high"
  className?: string
}

const glowColors = {
  amber: { border: "border-amber-400/20", shadow: "251, 191, 36" },
  blue: { border: "border-blue-400/20", shadow: "96, 165, 250" },
  emerald: { border: "border-emerald-400/20", shadow: "52, 211, 153" },
  red: { border: "border-red-400/20", shadow: "248, 113, 113" },
}

const intensityValues = {
  low: { min: 0.03, max: 0.1, spread: 20, maxSpread: 30 },
  medium: { min: 0.05, max: 0.15, spread: 25, maxSpread: 40 },
  high: { min: 0.08, max: 0.25, spread: 30, maxSpread: 50 },
}

export function GlowingSection({
  children,
  color = "amber",
  intensity = "medium",
  className = "",
}: GlowingSectionProps) {
  const { shadow } = glowColors[color]
  const { border } = glowColors[color]
  const { min, max, spread, maxSpread } = intensityValues[intensity]

  return (
    <motion.div
      animate={{
        boxShadow: [
          `0 0 ${spread}px 2px rgba(${shadow}, ${min})`,
          `0 0 ${maxSpread}px 8px rgba(${shadow}, ${max})`,
        ],
      }}
      transition={{
        duration: 2.5,
        ease: "easeInOut",
        repeat: Infinity,
        repeatType: "reverse",
      }}
      className={`border ${border} rounded-lg p-6 bg-neutral-950/50 ${className}`}
    >
      {children}
    </motion.div>
  )
}
```

### Usage

```tsx
<GlowingSection color="amber" intensity="medium">
  <h2 className="text-amber-400 text-sm tracking-widest">ALERT</h2>
  <p className="text-neutral-300 mt-2">System requires attention.</p>
</GlowingSection>

<GlowingSection color="emerald" intensity="low">
  <p className="text-emerald-300">All systems operational.</p>
</GlowingSection>
```

---

## 4. RevealInput

Minimal dark input with gold accent focus state. Designed for command-line-style interfaces on dark canvases.

### Props

```tsx
interface RevealInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit?: (value: string) => void
  placeholder?: string
  prefix?: string
  delay?: number
  className?: string
}
```

### Component

```tsx
"use client"

import { useCallback } from "react"
import { motion } from "motion/react"

interface RevealInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit?: (value: string) => void
  placeholder?: string
  prefix?: string
  delay?: number
  className?: string
}

export function RevealInput({
  value,
  onChange,
  onSubmit,
  placeholder = "Enter command...",
  prefix = ">",
  delay = 0,
  className = "",
}: RevealInputProps) {
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter" && value.trim()) {
        onSubmit?.(value.trim())
      }
    },
    [value, onSubmit]
  )

  return (
    <motion.div
      initial={{ opacity: 0, filter: "blur(8px)", y: 8 }}
      animate={{ opacity: 1, filter: "blur(0px)", y: 0 }}
      transition={{
        duration: 0.5,
        delay,
        ease: "easeOut",
      }}
      className={`relative ${className}`}
    >
      <span className="absolute left-3 top-1/2 -translate-y-1/2 text-amber-400/50 text-sm font-mono">
        {prefix}
      </span>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="w-full bg-neutral-950 border border-neutral-800 rounded-md py-2.5 pl-8 pr-4 text-sm text-neutral-200 font-mono placeholder:text-neutral-600 focus:outline-none focus:border-amber-400/40 focus:ring-1 focus:ring-amber-400/20 transition-colors duration-200"
      />
    </motion.div>
  )
}
```

### Usage

```tsx
const [command, setCommand] = useState("")

<RevealInput
  value={command}
  onChange={setCommand}
  onSubmit={(cmd) => console.log("Submitted:", cmd)}
  placeholder="Type a command..."
  prefix="$"
  delay={1.2}
/>
```

---

## 5. AssemblyTimeline

Coordinated multi-section reveal orchestrator. Sections appear one after another with configurable stagger. Supports both automatic timed reveals and manual progression.

### Props

```tsx
interface TimelineSection {
  id: string
  label: string
  content: React.ReactNode
}

interface AssemblyTimelineProps {
  sections: TimelineSection[]
  staggerDelay?: number
  autoPlay?: boolean
  className?: string
  onSectionReveal?: (sectionId: string, index: number) => void
  onComplete?: () => void
}
```

### Component

```tsx
"use client"

import { useState, useEffect, useCallback } from "react"
import { motion, AnimatePresence } from "motion/react"

interface TimelineSection {
  id: string
  label: string
  content: React.ReactNode
}

interface AssemblyTimelineProps {
  sections: TimelineSection[]
  staggerDelay?: number
  autoPlay?: boolean
  className?: string
  onSectionReveal?: (sectionId: string, index: number) => void
  onComplete?: () => void
}

const sectionVariants = {
  hidden: { opacity: 0, filter: "blur(10px)", x: -12, height: 0 },
  visible: {
    opacity: 1,
    filter: "blur(0px)",
    x: 0,
    height: "auto",
    transition: {
      duration: 0.6,
      ease: [0.22, 1, 0.36, 1],
      height: { duration: 0.4, ease: "easeOut" },
    },
  },
  exit: {
    opacity: 0,
    filter: "blur(6px)",
    x: 12,
    transition: { duration: 0.3, ease: "easeIn" },
  },
}

export function AssemblyTimeline({
  sections,
  staggerDelay = 0.8,
  autoPlay = true,
  className = "",
  onSectionReveal,
  onComplete,
}: AssemblyTimelineProps) {
  const [revealedCount, setRevealedCount] = useState(0)

  useEffect(() => {
    if (!autoPlay || revealedCount >= sections.length) {
      if (revealedCount >= sections.length) onComplete?.()
      return
    }

    const timeout = setTimeout(() => {
      const nextIndex = revealedCount
      setRevealedCount((c) => c + 1)
      onSectionReveal?.(sections[nextIndex].id, nextIndex)
    }, staggerDelay * 1000)

    return () => clearTimeout(timeout)
  }, [revealedCount, sections, staggerDelay, autoPlay, onSectionReveal, onComplete])

  const revealNext = useCallback(() => {
    if (revealedCount < sections.length) {
      onSectionReveal?.(sections[revealedCount].id, revealedCount)
      setRevealedCount((c) => c + 1)
    }
  }, [revealedCount, sections, onSectionReveal])

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Timeline track */}
      <div className="relative">
        <div className="absolute left-[5px] top-0 bottom-0 w-px bg-neutral-800" />

        <AnimatePresence>
          {sections.slice(0, revealedCount).map((section, i) => (
            <motion.div
              key={section.id}
              variants={sectionVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="relative pl-8 pb-6"
            >
              {/* Timeline dot */}
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.1, duration: 0.3, ease: "easeOut" }}
                className="absolute left-0 top-1 w-[11px] h-[11px] rounded-full border-2 border-amber-400/60 bg-neutral-950"
              />

              {/* Section content */}
              <div className="space-y-1">
                <span className="text-[11px] font-medium tracking-[0.15em] text-amber-400/70 uppercase">
                  {section.label}
                </span>
                <div className="text-neutral-300 text-base leading-relaxed">
                  {section.content}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Manual advance button (when autoPlay is false) */}
      {!autoPlay && revealedCount < sections.length && (
        <motion.button
          onClick={revealNext}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-sm text-amber-400/60 hover:text-amber-400 tracking-widest uppercase transition-colors"
        >
          Continue
        </motion.button>
      )}

      {/* Completion indicator */}
      {revealedCount >= sections.length && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="pl-8 text-sm text-neutral-600 tracking-wide"
        >
          Assembly complete.
        </motion.div>
      )}
    </div>
  )
}
```

### Usage

```tsx
<AssemblyTimeline
  sections={[
    { id: "overview", label: "OVERVIEW", content: <p>Market analysis indicates strong growth potential in the AI infrastructure sector.</p> },
    { id: "data", label: "KEY DATA", content: <p>Revenue: $4.2M ARR. Growth: 18% MoM. Runway: 14 months.</p> },
    { id: "risk", label: "RISK FACTORS", content: <p>Competitor fundraise announced. Two key hires still open.</p> },
    { id: "action", label: "RECOMMENDED ACTION", content: <p>Accelerate Series A timeline. Target close by Q3.</p> },
  ]}
  staggerDelay={1.2}
  autoPlay={true}
  onSectionReveal={(id) => console.log(`Revealed: ${id}`)}
  onComplete={() => console.log("All sections revealed")}
/>

{/* Manual progression mode */}
<AssemblyTimeline
  sections={briefingSections}
  autoPlay={false}
/>
```

---

## Combining Components

Build a full reveal page by composing these components:

```tsx
"use client"

import { useState } from "react"
import { CinematicHeading } from "./CinematicHeading"
import { StreamingParagraph } from "./StreamingParagraph"
import { GlowingSection } from "./GlowingSection"
import { RevealInput } from "./RevealInput"
import { AssemblyTimeline } from "./AssemblyTimeline"

export default function BriefingPage() {
  const [command, setCommand] = useState("")

  return (
    <div className="min-h-screen bg-black text-neutral-100 flex items-center justify-center p-8">
      <div className="w-full max-w-2xl space-y-8">
        <CinematicHeading
          title="MORNING BRIEFING"
          subtitle="March 10, 2026"
        />

        <GlowingSection color="amber" intensity="low">
          <StreamingParagraph
            text="Three priority items detected. Revenue forecast has been updated with Q1 actuals. Team standup rescheduled to 14:00."
            wordsPerSecond={10}
          />
        </GlowingSection>

        <AssemblyTimeline
          sections={[
            { id: "1", label: "REVENUE", content: <p>Q1 landed at $1.2M, 8% above forecast.</p> },
            { id: "2", label: "PIPELINE", content: <p>14 qualified opportunities. 3 in negotiation.</p> },
            { id: "3", label: "ACTION", content: <p>Review pricing proposal before 15:00 call.</p> },
          ]}
          staggerDelay={1.0}
        />

        <RevealInput
          value={command}
          onChange={setCommand}
          onSubmit={(cmd) => console.log(cmd)}
          delay={3.5}
        />
      </div>
    </div>
  )
}
```
