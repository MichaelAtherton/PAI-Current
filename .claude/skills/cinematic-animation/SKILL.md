---
name: cinematic-animation
description: "Cinematic streaming text animations — Motion + FlowToken + Aceternity patterns for reveal modes, streaming AI responses, and theatrical presentations. USE WHEN cinematic, reveal mode, streaming animation, text assembly, dramatic text, stage mode, presentation mode, dark canvas, theatrical UI, text materialize, briefing animation."
user_invocable: false
---

# Cinematic Animation Skill

Theatrical text animation system for building dark-canvas reveal interfaces, streaming AI response displays, and cinematic presentation modes. Built on three complementary tools that handle different layers of animation.

## Tools

### 1. Motion (primary animation engine)

The `motion` package (v11+) is the successor to Framer Motion. It provides declarative React animation primitives.

```bash
npm install motion
```

**Import pattern:**
```tsx
import { motion, AnimatePresence, useMotionValue, useTransform } from "motion/react"
```

**When to use:** Layout animations, enter/exit transitions, gesture-driven motion, scroll-linked effects, staggered reveals. This is the default choice for all animation needs.

### 2. FlowToken

Specialized library for animating streaming text — designed for LLM output where tokens arrive one at a time.

```bash
npm install flowtoken
```

**When to use:** Streaming AI responses, word-by-word text assembly, typewriter effects with physics-based settling, any scenario where text content grows incrementally.

### 3. Aceternity UI Patterns

Design patterns (not a package) from Aceternity UI for theatrical visual effects — glows, gradients, spotlight cursors, aurora backgrounds.

**When to use:** Ambient visual atmosphere, background effects, glow borders, gradient text, spotlight/cursor effects. These are CSS/Tailwind patterns, not a separate dependency.

## Core Principles

1. **Dark canvas first.** Cinematic UI starts with `bg-black` or `bg-neutral-950`. Light backgrounds kill the theatrical feel.
2. **Stagger everything.** Never reveal multiple elements simultaneously. Use 80-150ms stagger delays between sections.
3. **Blur-to-sharp is the signature.** Text materializing from `blur(12px)` to `blur(0)` with simultaneous opacity creates the cinematic feel.
4. **Gold accents on dark.** Use `text-amber-400` or `text-yellow-500` for emphasis on dark backgrounds. Avoid saturated colors.
5. **Respect the timing.** Reveals should feel deliberate: 600-1200ms per element. Faster feels cheap, slower feels broken.
6. **Performance matters.** Animate only `transform` and `opacity` for 60fps. Use `will-change` sparingly. Batch streaming updates with `requestAnimationFrame`.

## Install Commands (All Dependencies)

```bash
npm install motion flowtoken
# Aceternity patterns use only Tailwind — no additional package
```

Requires: React 19+, Tailwind CSS 4+, TypeScript 5+.

## Workflow Routing

| Request | Workflow |
|---------|----------|
| Build a reveal mode / dark canvas / cinematic page | `Workflows/RevealMode.md` |
| Animate streaming AI text / LLM output | `Workflows/StreamingText.md` |
| Need a specific cinematic component | `Workflows/ComponentLibrary.md` |
| Full theatrical presentation with streaming + reveal | Start with `RevealMode.md`, incorporate `StreamingText.md` patterns |

## Integration

### Feeds Into
- **claude-code-design-stack** — Use cinematic components inside design stack outputs
- Any Next.js / React project requiring theatrical presentation

### Uses
- **motion** package for all animation primitives
- **flowtoken** for streaming text
- **Tailwind CSS** for all styling (no CSS modules, no styled-components)
