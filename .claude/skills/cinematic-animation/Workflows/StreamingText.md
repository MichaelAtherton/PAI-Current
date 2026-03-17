# Streaming Text Workflow

Animating streaming AI responses — text that arrives token-by-token from an LLM and needs to feel cinematic rather than jumpy.

## The Problem

Raw streaming text (appending tokens to a string) looks cheap: text jumps, layout shifts, no sense of intention. Cinematic streaming means each token arrives with physics-based settling, the layout smoothly expands, and the overall effect feels like text is being *composed* rather than dumped.

## Architecture

```
StreamingContainer
├── FlowToken (word-level animation + layout smoothing)
│   └── motion.span (per-token entrance animation)
├── Cursor (blinking caret at insertion point)
└── ScrollAnchor (keeps latest content in view)
```

## FlowToken with LLM Streaming

FlowToken handles the hard part: smooth layout transitions as new tokens push existing text around.

### Basic Setup

```tsx
"use client"

import { useState, useCallback } from "react"
import { FlowText, FlowTextProps } from "flowtoken"
import { motion } from "motion/react"

interface StreamingDisplayProps {
  className?: string
}

export function StreamingDisplay({ className }: StreamingDisplayProps) {
  const [text, setText] = useState("")
  const [isStreaming, setIsStreaming] = useState(false)

  const startStream = useCallback(async () => {
    setIsStreaming(true)
    setText("")

    const response = await fetch("/api/chat", {
      method: "POST",
      body: JSON.stringify({ prompt: "Your prompt here" }),
    })

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) return

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value, { stream: true })
      setText((prev) => prev + chunk)
    }

    setIsStreaming(false)
  }, [])

  return (
    <div className={`bg-black text-neutral-100 p-8 ${className ?? ""}`}>
      <FlowText
        text={text}
        windowSize={10}
        animationDuration={0.3}
        className="text-base leading-relaxed"
      />
      {isStreaming && (
        <motion.span
          className="inline-block w-0.5 h-5 bg-amber-400 ml-0.5 align-text-bottom"
          animate={{ opacity: [1, 0] }}
          transition={{ duration: 0.8, repeat: Infinity, repeatType: "reverse" }}
        />
      )}
    </div>
  )
}
```

### FlowToken Key Props

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `text` | `string` | — | The current accumulated text |
| `windowSize` | `number` | `5` | How many recent tokens animate (older ones are static) |
| `animationDuration` | `number` | `0.3` | Seconds per token animation |
| `className` | `string` | — | Tailwind classes for the text container |

## Motion Layering

Layer Motion on top of FlowToken for section-level effects:

```tsx
import { motion, AnimatePresence } from "motion/react"

interface StreamingSectionProps {
  label: string
  text: string
  isActive: boolean
}

export function StreamingSection({ label, text, isActive }: StreamingSectionProps) {
  return (
    <AnimatePresence>
      {isActive && (
        <motion.div
          initial={{ opacity: 0, filter: "blur(8px)", y: 8 }}
          animate={{ opacity: 1, filter: "blur(0px)", y: 0 }}
          exit={{ opacity: 0, filter: "blur(4px)", y: -4 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
          className="space-y-2"
        >
          <span className="text-[11px] tracking-[0.15em] text-amber-400/70 uppercase font-medium">
            {label}
          </span>
          <div className="text-neutral-300 leading-relaxed">
            <FlowText text={text} windowSize={8} animationDuration={0.25} />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

## Performance Optimization

### The Buffer-Batch-rAF Pattern

LLM streaming can deliver tokens faster than the browser can render smoothly. The solution: buffer incoming tokens and flush them in batches aligned with `requestAnimationFrame`.

```tsx
import { useRef, useState, useCallback, useEffect } from "react"

export function useBufferedStream() {
  const [displayText, setDisplayText] = useState("")
  const bufferRef = useRef("")
  const rafRef = useRef<number | null>(null)
  const isFlushingRef = useRef(false)

  const flushBuffer = useCallback(() => {
    if (bufferRef.current.length === 0) {
      isFlushingRef.current = false
      return
    }

    // Take up to 3 tokens (words) per frame for smooth pacing
    const words = bufferRef.current.split(/(\s+)/)
    const batch = words.slice(0, 6).join("") // 3 words + 3 spaces
    bufferRef.current = words.slice(6).join("")

    setDisplayText((prev) => prev + batch)

    rafRef.current = requestAnimationFrame(flushBuffer)
  }, [])

  const addToken = useCallback(
    (token: string) => {
      bufferRef.current += token

      if (!isFlushingRef.current) {
        isFlushingRef.current = true
        rafRef.current = requestAnimationFrame(flushBuffer)
      }
    },
    [flushBuffer]
  )

  const reset = useCallback(() => {
    bufferRef.current = ""
    setDisplayText("")
    if (rafRef.current) cancelAnimationFrame(rafRef.current)
    isFlushingRef.current = false
  }, [])

  useEffect(() => {
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current)
    }
  }, [])

  return { displayText, addToken, reset }
}
```

### Usage with Streaming API

```tsx
const { displayText, addToken, reset } = useBufferedStream()

async function handleStream() {
  reset()
  const response = await fetch("/api/chat", { method: "POST", body: "..." })
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    addToken(decoder.decode(value, { stream: true }))
  }
}
```

### Performance Rules

1. **Never set state on every token.** Buffer and batch with rAF.
2. **Limit the animation window.** FlowToken's `windowSize` should be 5-10. Animating 200 tokens simultaneously will drop frames.
3. **Use `transform` and `opacity` only.** Animating `filter: blur()` is GPU-composited on most browsers but test on target hardware.
4. **Avoid layout thrash.** Don't measure DOM between token additions. Let FlowToken handle layout internally.
5. **Clean up rAF on unmount.** Always cancel pending animation frames in the cleanup function.

## Integration Patterns

### Pattern A: Streaming into Reveal Mode

Combine with RevealMode workflow — the page reveals with cinematic stagger, then a section begins streaming live content:

```tsx
<RevealCanvas>
  <CinematicHeading title="LIVE ANALYSIS" />
  <StreamingSection label="OUTPUT" text={streamedText} isActive={isStreaming} />
</RevealCanvas>
```

### Pattern B: Multi-Section Streaming

Multiple sections stream sequentially (section 2 starts when section 1 completes):

```tsx
const sections = ["summary", "analysis", "recommendation"]
const [activeIndex, setActiveIndex] = useState(0)
const [texts, setTexts] = useState<Record<string, string>>({})

// When stream for current section completes, advance to next
useEffect(() => {
  if (streamComplete && activeIndex < sections.length - 1) {
    setActiveIndex((i) => i + 1)
  }
}, [streamComplete, activeIndex])
```

### Pattern C: Typewriter with Motion Blur

For non-streaming text that should *look* like it's streaming (e.g., pre-written briefing text):

```tsx
export function SimulatedStream({ text, wordsPerSecond = 12 }: {
  text: string
  wordsPerSecond?: number
}) {
  const [visibleCount, setVisibleCount] = useState(0)
  const words = text.split(" ")

  useEffect(() => {
    const interval = setInterval(() => {
      setVisibleCount((c) => {
        if (c >= words.length) {
          clearInterval(interval)
          return c
        }
        return c + 1
      })
    }, 1000 / wordsPerSecond)
    return () => clearInterval(interval)
  }, [words.length, wordsPerSecond])

  return (
    <p className="text-neutral-300 leading-relaxed">
      {words.slice(0, visibleCount).map((word, i) => (
        <motion.span
          key={i}
          initial={{ opacity: 0, filter: "blur(4px)" }}
          animate={{ opacity: 1, filter: "blur(0px)" }}
          transition={{ duration: 0.2 }}
          className="inline-block mr-[0.25em]"
        >
          {word}
        </motion.span>
      ))}
    </p>
  )
}
```
