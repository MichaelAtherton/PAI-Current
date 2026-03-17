# Option 2: GSAP Master MCP Server -- Installation & Capabilities Report

**Date:** 2026-03-10
**Source:** https://github.com/bruzethegreat/gsap-master-mcp-server

---

## 1. MCP Installation Status

**Status: INSTALLED**

The GSAP Master MCP server has been added at both the user level (via `claude mcp add-json`) and the project level (in `settings.json`).

### CLI Install Command

```bash
claude mcp add-json gsap-master '{"command":"npx","args":["bruzethegreat-gsap-master-mcp-server@latest"]}'
```

### Project-Level Config (settings.json mcpServers section)

```json
{
  "mcpServers": {
    "cloudflare": {
      "url": "https://mcp.cloudflare.com/mcp"
    },
    "gsap-master": {
      "command": "npx",
      "args": ["bruzethegreat-gsap-master-mcp-server@latest"]
    }
  }
}
```

**Dependencies:** Node.js 18+ (handled automatically by npx -- no manual install needed). All GSAP plugins are now free (thanks to Webflow acquisition).

---

## 2. MCP Tools List (6 Tools)

| Tool | Description |
|------|-------------|
| `understand_and_create_animation` | Converts natural language descriptions into framework-specific GSAP animation code (React, Vue, Next.js, Svelte, vanilla JS) |
| `get_gsap_api_expert` | Provides complete documentation for all GSAP methods, plugins, and their parameters |
| `generate_complete_setup` | Creates full project boilerplate with correct dependencies for your chosen framework |
| `debug_animation_issue` | Troubleshoots performance lag, mobile compatibility, ScrollTrigger positioning, and timeline sequencing problems |
| `optimize_for_performance` | Transforms animations for 60fps on desktop, creates mobile variants, and optimizes for battery efficiency |
| `create_production_pattern` | Delivers pre-built animation systems for hero sections, scroll effects, text treatments, and UI components |

### Plugin Coverage

- **ScrollTrigger** -- parallax, reveals, pins, progress tracking
- **SplitText** -- character/word/line manipulation
- **DrawSVG** -- path animations
- **MorphSVG** -- shape transitions
- **Draggable** -- interactive elements
- **Core** -- gsap.to, gsap.from, gsap.fromTo, timeline sequencing

---

## 3. Code Examples

### Required Dependencies

```bash
npm install gsap @gsap/react
```

All components use: `@gsap/react` useGSAP hook, React 19, TypeScript, Tailwind CSS, Navy (#0A1628) / Gold (#D4AF37) color palette.

---

### 3.1 CinematicTextReveal.tsx

Character-by-character text reveal with blur-to-sharp using GSAP SplitText + timeline.

```tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { SplitText } from "gsap/SplitText";

gsap.registerPlugin(SplitText);

interface CinematicTextRevealProps {
  text: string;
  subtitle?: string;
  delay?: number;
  staggerSpeed?: number;
}

export default function CinematicTextReveal({
  text,
  subtitle,
  delay = 0.5,
  staggerSpeed = 0.04,
}: CinematicTextRevealProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const subtitleRef = useRef<HTMLParagraphElement>(null);

  useGSAP(
    () => {
      if (!headingRef.current) return;

      const split = SplitText.create(headingRef.current, {
        type: "chars",
      });

      const tl = gsap.timeline({ delay });

      // Set initial state -- invisible, blurred, shifted down
      gsap.set(split.chars, {
        opacity: 0,
        filter: "blur(12px)",
        y: 20,
        rotationX: -90,
        transformOrigin: "bottom center",
      });

      // Reveal characters one by one: blur-to-sharp + slide up
      tl.to(split.chars, {
        opacity: 1,
        filter: "blur(0px)",
        y: 0,
        rotationX: 0,
        duration: 0.8,
        ease: "power3.out",
        stagger: {
          each: staggerSpeed,
          from: "start",
        },
      });

      // Gold underline sweep
      tl.fromTo(
        ".cinematic-underline",
        { scaleX: 0, transformOrigin: "left center" },
        { scaleX: 1, duration: 0.6, ease: "power2.inOut" },
        "-=0.3"
      );

      // Subtitle fade in
      if (subtitleRef.current) {
        tl.fromTo(
          subtitleRef.current,
          { opacity: 0, y: 10, filter: "blur(4px)" },
          {
            opacity: 1,
            y: 0,
            filter: "blur(0px)",
            duration: 0.6,
            ease: "power2.out",
          },
          "-=0.2"
        );
      }

      return () => {
        split.revert();
      };
    },
    { scope: containerRef }
  );

  return (
    <div
      ref={containerRef}
      className="flex min-h-[50vh] flex-col items-center justify-center px-6"
      style={{ backgroundColor: "#0A1628" }}
    >
      <h1
        ref={headingRef}
        className="text-center text-5xl font-bold tracking-tight md:text-7xl"
        style={{ color: "#F0F4F8", perspective: "600px" }}
      >
        {text}
      </h1>

      <div
        className="cinematic-underline mt-4 h-[2px] w-48"
        style={{ backgroundColor: "#D4AF37" }}
      />

      {subtitle && (
        <p
          ref={subtitleRef}
          className="mt-6 text-lg tracking-wide opacity-0 md:text-xl"
          style={{ color: "#8899AA" }}
        >
          {subtitle}
        </p>
      )}
    </div>
  );
}
```

---

### 3.2 SectionAssembly.tsx

Multiple sections staggering in with spring easing and scroll-triggered reveal.

```tsx
"use client";

import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

interface Section {
  title: string;
  content: string;
  icon?: string;
}

interface SectionAssemblyProps {
  sections: Section[];
  springDamping?: number;
}

const defaultSections: Section[] = [
  {
    title: "Intelligence Gathered",
    content: "42 sources analyzed across 6 domains in the last 24 hours.",
    icon: "shield",
  },
  {
    title: "Threat Assessment",
    content: "3 emerging risks identified. 1 requires immediate attention.",
    icon: "alert",
  },
  {
    title: "Strategic Outlook",
    content: "Market conditions favor acceleration. Window: 14 days.",
    icon: "target",
  },
  {
    title: "Action Items",
    content: "5 recommendations generated. 2 marked high priority.",
    icon: "list",
  },
];

export default function SectionAssembly({
  sections = defaultSections,
  springDamping = 0.6,
}: SectionAssemblyProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const cards = gsap.utils.toArray<HTMLElement>(".assembly-card");

      // Initial state: scattered, invisible
      gsap.set(cards, {
        opacity: 0,
        y: 80,
        scale: 0.9,
        rotationY: -15,
        transformOrigin: "left center",
      });

      // Create a timeline with scroll trigger
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top 75%",
          end: "bottom 25%",
          toggleActions: "play none none reverse",
        },
      });

      // Header reveal
      tl.fromTo(
        ".assembly-header",
        { opacity: 0, y: -30, filter: "blur(8px)" },
        {
          opacity: 1,
          y: 0,
          filter: "blur(0px)",
          duration: 0.6,
          ease: "power2.out",
        }
      );

      // Stagger cards with spring physics
      tl.to(
        cards,
        {
          opacity: 1,
          y: 0,
          scale: 1,
          rotationY: 0,
          duration: 1.2,
          ease: `elastic.out(1, ${springDamping})`,
          stagger: {
            each: 0.15,
            from: "start",
          },
        },
        "-=0.2"
      );

      // Gold accent lines on each card
      tl.fromTo(
        ".card-accent",
        { scaleY: 0, transformOrigin: "top" },
        {
          scaleY: 1,
          duration: 0.4,
          ease: "power2.out",
          stagger: 0.1,
        },
        "-=0.8"
      );
    },
    { scope: containerRef }
  );

  return (
    <div
      ref={containerRef}
      className="min-h-screen px-6 py-24"
      style={{ backgroundColor: "#0A1628" }}
    >
      <div className="mx-auto max-w-4xl">
        <h2
          className="assembly-header mb-12 text-center text-3xl font-bold tracking-tight md:text-4xl"
          style={{ color: "#D4AF37" }}
        >
          Briefing Assembly
        </h2>

        <div className="grid gap-6 md:grid-cols-2">
          {sections.map((section, i) => (
            <div
              key={i}
              className="assembly-card relative overflow-hidden rounded-lg border p-6"
              style={{
                backgroundColor: "rgba(255, 255, 255, 0.03)",
                borderColor: "rgba(212, 175, 55, 0.15)",
              }}
            >
              {/* Gold left accent bar */}
              <div
                className="card-accent absolute left-0 top-0 h-full w-[3px]"
                style={{ backgroundColor: "#D4AF37" }}
              />

              <div className="pl-4">
                <h3
                  className="mb-2 text-lg font-semibold"
                  style={{ color: "#F0F4F8" }}
                >
                  {section.title}
                </h3>
                <p
                  className="text-sm leading-relaxed"
                  style={{ color: "#8899AA" }}
                >
                  {section.content}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

---

### 3.3 RevealSequence.tsx

Complete dark canvas -> input -> generate -> briefing assembles orchestration.

```tsx
"use client";

import { useRef, useState, useCallback } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { SplitText } from "gsap/SplitText";

gsap.registerPlugin(SplitText);

type Phase = "idle" | "input" | "generating" | "revealing" | "complete";

interface BriefingLine {
  label: string;
  value: string;
}

const mockBriefing: BriefingLine[] = [
  { label: "CLASSIFICATION", value: "PRIORITY ALPHA" },
  { label: "SUBJECT", value: "Market Disruption Analysis" },
  { label: "SOURCES", value: "42 feeds / 6 domains / 24hr window" },
  { label: "THREAT LEVEL", value: "ELEVATED" },
  { label: "CONFIDENCE", value: "94.2%" },
  { label: "RECOMMENDATION", value: "Accelerate defensive positioning" },
];

export default function RevealSequence() {
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<gsap.core.Timeline | null>(null);
  const [phase, setPhase] = useState<Phase>("idle");
  const [query, setQuery] = useState("");

  const runSequence = useCallback(() => {
    if (!containerRef.current || phase !== "idle") return;

    setPhase("input");

    const tl = gsap.timeline({
      onComplete: () => setPhase("complete"),
    });
    timelineRef.current = tl;

    // Phase 1: Input field materializes
    tl.fromTo(
      ".reveal-input-group",
      { opacity: 0, y: 30, scale: 0.95 },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.6,
        ease: "power2.out",
      }
    );

    // Phase 2: After brief pause, simulate typing + generation
    tl.call(() => setPhase("generating"), [], "+=1.5");

    // Input shrinks up, spinner appears
    tl.to(".reveal-input-group", {
      y: -20,
      scale: 0.9,
      opacity: 0.5,
      duration: 0.4,
      ease: "power2.in",
    });

    tl.fromTo(
      ".reveal-spinner",
      { opacity: 0, scale: 0 },
      {
        opacity: 1,
        scale: 1,
        duration: 0.3,
        ease: "back.out(2)",
      }
    );

    // Spinner pulses
    tl.to(".reveal-spinner", {
      scale: 1.1,
      duration: 0.4,
      repeat: 3,
      yoyo: true,
      ease: "sine.inOut",
    });

    // Phase 3: Spinner dissolves, briefing assembles
    tl.call(() => setPhase("revealing"));

    tl.to(".reveal-spinner", {
      opacity: 0,
      scale: 0,
      duration: 0.2,
    });

    tl.to(".reveal-input-group", {
      opacity: 0,
      y: -40,
      duration: 0.3,
    });

    // Header appears
    tl.fromTo(
      ".briefing-header",
      { opacity: 0, y: 20, filter: "blur(8px)" },
      {
        opacity: 1,
        y: 0,
        filter: "blur(0px)",
        duration: 0.5,
        ease: "power2.out",
      }
    );

    // Horizontal rule sweeps
    tl.fromTo(
      ".briefing-rule",
      { scaleX: 0, transformOrigin: "left" },
      { scaleX: 1, duration: 0.4, ease: "power2.inOut" }
    );

    // Each briefing line staggers in
    tl.fromTo(
      ".briefing-line",
      { opacity: 0, x: -30, filter: "blur(4px)" },
      {
        opacity: 1,
        x: 0,
        filter: "blur(0px)",
        duration: 0.5,
        ease: "power2.out",
        stagger: 0.12,
      },
      "-=0.1"
    );

    // Values highlight with gold flash
    tl.fromTo(
      ".briefing-value",
      { color: "#8899AA" },
      {
        color: "#D4AF37",
        duration: 0.3,
        stagger: 0.08,
        ease: "power1.in",
      },
      "-=0.4"
    );

    // Final bottom rule
    tl.fromTo(
      ".briefing-rule-end",
      { scaleX: 0, transformOrigin: "right" },
      { scaleX: 1, duration: 0.4, ease: "power2.inOut" }
    );
  }, [phase]);

  const reset = useCallback(() => {
    if (timelineRef.current) {
      timelineRef.current.kill();
    }
    // Reset all elements
    gsap.set(
      [
        ".reveal-input-group",
        ".reveal-spinner",
        ".briefing-header",
        ".briefing-rule",
        ".briefing-rule-end",
        ".briefing-line",
      ],
      { clearProps: "all" }
    );
    gsap.set(
      [
        ".reveal-spinner",
        ".briefing-header",
        ".briefing-rule",
        ".briefing-rule-end",
        ".briefing-line",
      ],
      { opacity: 0 }
    );
    gsap.set(".reveal-input-group", { opacity: 0 });
    setPhase("idle");
    setQuery("");
  }, []);

  return (
    <div
      ref={containerRef}
      className="flex min-h-screen flex-col items-center justify-center px-6"
      style={{ backgroundColor: "#0A1628" }}
    >
      {/* Trigger button (idle state) */}
      {phase === "idle" && (
        <button
          onClick={runSequence}
          className="rounded-lg border px-8 py-3 text-sm font-medium tracking-widest uppercase transition-colors hover:border-opacity-60"
          style={{
            color: "#D4AF37",
            borderColor: "rgba(212, 175, 55, 0.3)",
            backgroundColor: "rgba(212, 175, 55, 0.05)",
          }}
        >
          Initialize Briefing
        </button>
      )}

      {/* Reset button (complete state) */}
      {phase === "complete" && (
        <button
          onClick={reset}
          className="absolute right-8 top-8 rounded border px-4 py-2 text-xs tracking-wider uppercase"
          style={{
            color: "#8899AA",
            borderColor: "rgba(136, 153, 170, 0.2)",
          }}
        >
          Reset
        </button>
      )}

      {/* Input group */}
      <div className="reveal-input-group w-full max-w-lg opacity-0">
        <label
          className="mb-2 block text-xs tracking-widest uppercase"
          style={{ color: "#D4AF37" }}
        >
          Intelligence Query
        </label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter analysis parameters..."
          className="w-full rounded-lg border bg-transparent px-4 py-3 text-sm outline-none"
          style={{
            color: "#F0F4F8",
            borderColor: "rgba(212, 175, 55, 0.2)",
          }}
        />
      </div>

      {/* Spinner */}
      <div
        className="reveal-spinner mt-8 opacity-0"
        style={{ color: "#D4AF37" }}
      >
        <svg
          className="h-8 w-8 animate-spin"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <circle cx="12" cy="12" r="10" strokeOpacity="0.2" />
          <path d="M12 2a10 10 0 0 1 10 10" strokeLinecap="round" />
        </svg>
      </div>

      {/* Briefing output */}
      <div className="mt-8 w-full max-w-2xl">
        <h3
          className="briefing-header mb-4 text-center text-xl font-bold tracking-widest uppercase opacity-0"
          style={{ color: "#D4AF37" }}
        >
          Executive Briefing
        </h3>

        <div
          className="briefing-rule mb-6 h-px w-full opacity-0"
          style={{ backgroundColor: "rgba(212, 175, 55, 0.3)" }}
        />

        {mockBriefing.map((line, i) => (
          <div
            key={i}
            className="briefing-line mb-3 flex items-baseline justify-between opacity-0"
          >
            <span
              className="text-xs font-medium tracking-widest uppercase"
              style={{ color: "#556677" }}
            >
              {line.label}
            </span>
            <span
              className="briefing-value text-sm font-semibold"
              style={{ color: "#8899AA" }}
            >
              {line.value}
            </span>
          </div>
        ))}

        <div
          className="briefing-rule-end mt-6 h-px w-full opacity-0"
          style={{ backgroundColor: "rgba(212, 175, 55, 0.3)" }}
        />
      </div>
    </div>
  );
}
```

---

### 3.4 StreamingSimulation.tsx

Simulated LLM streaming with GSAP progressive character reveal, cursor blink, and paragraph assembly.

```tsx
"use client";

import { useRef, useState, useCallback, useEffect } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

interface StreamingSimulationProps {
  paragraphs?: string[];
  charDelay?: number;
  paragraphGap?: number;
}

const defaultParagraphs = [
  "Analysis of 42 intelligence sources reveals a significant shift in market dynamics over the past 72 hours.",
  "Three primary threat vectors have been identified. The most critical involves regulatory changes in the APAC region that could impact supply chain operations within 14 days.",
  "Confidence level: 94.2%. Recommendation: Begin defensive repositioning immediately while maintaining optionality for opportunistic moves.",
  "Full detailed assessment follows in the classified appendix. Action items have been routed to relevant stakeholders.",
];

export default function StreamingSimulation({
  paragraphs = defaultParagraphs,
  charDelay = 0.018,
  paragraphGap = 0.3,
}: StreamingSimulationProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<gsap.core.Timeline | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [displayedChars, setDisplayedChars] = useState<number[]>(
    paragraphs.map(() => 0)
  );
  const [activeParagraph, setActiveParagraph] = useState(-1);

  const startStreaming = useCallback(() => {
    if (isStreaming) return;
    setIsStreaming(true);
    setDisplayedChars(paragraphs.map(() => 0));
    setActiveParagraph(0);

    const tl = gsap.timeline({
      onComplete: () => {
        setIsStreaming(false);
        // Final cursor blink then hide
        gsap.to(".stream-cursor", {
          opacity: 0,
          duration: 0.3,
          delay: 1,
        });
      },
    });
    timelineRef.current = tl;

    // Header materializes
    tl.fromTo(
      ".stream-header",
      { opacity: 0, y: -10 },
      { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }
    );

    // Status indicator pulses
    tl.fromTo(
      ".stream-status",
      { opacity: 0 },
      { opacity: 1, duration: 0.2 }
    );

    // Stream each paragraph
    paragraphs.forEach((text, pIndex) => {
      const charCount = text.length;

      // Activate paragraph container
      tl.call(() => setActiveParagraph(pIndex));

      tl.fromTo(
        `.stream-para-${pIndex}`,
        { opacity: 0, y: 8 },
        { opacity: 1, y: 0, duration: 0.2, ease: "power2.out" }
      );

      // Progressive character reveal using a counter
      const counter = { val: 0 };
      tl.to(counter, {
        val: charCount,
        duration: charCount * charDelay,
        ease: "none",
        roundProps: "val",
        onUpdate: () => {
          setDisplayedChars((prev) => {
            const next = [...prev];
            next[pIndex] = counter.val;
            return next;
          });
        },
      });

      // Pause between paragraphs
      if (pIndex < paragraphs.length - 1) {
        tl.to({}, { duration: paragraphGap });
      }
    });

    // Status changes to complete
    tl.call(() => setActiveParagraph(-1));
  }, [isStreaming, paragraphs, charDelay, paragraphGap]);

  const reset = useCallback(() => {
    if (timelineRef.current) {
      timelineRef.current.kill();
    }
    setIsStreaming(false);
    setDisplayedChars(paragraphs.map(() => 0));
    setActiveParagraph(-1);
    gsap.set([".stream-header", ".stream-status"], {
      clearProps: "all",
      opacity: 0,
    });
  }, [paragraphs]);

  return (
    <div
      ref={containerRef}
      className="flex min-h-screen flex-col items-center justify-center px-6"
      style={{ backgroundColor: "#0A1628" }}
    >
      {/* Controls */}
      <div className="mb-12 flex gap-4">
        <button
          onClick={startStreaming}
          disabled={isStreaming}
          className="rounded-lg border px-6 py-2.5 text-sm font-medium tracking-wider uppercase transition-all disabled:opacity-30"
          style={{
            color: "#D4AF37",
            borderColor: "rgba(212, 175, 55, 0.3)",
            backgroundColor: "rgba(212, 175, 55, 0.05)",
          }}
        >
          {isStreaming ? "Streaming..." : "Begin Stream"}
        </button>
        <button
          onClick={reset}
          className="rounded-lg border px-6 py-2.5 text-sm tracking-wider uppercase"
          style={{
            color: "#8899AA",
            borderColor: "rgba(136, 153, 170, 0.15)",
          }}
        >
          Reset
        </button>
      </div>

      {/* Output area */}
      <div className="w-full max-w-2xl">
        {/* Header */}
        <div className="stream-header mb-6 flex items-center justify-between opacity-0">
          <span
            className="text-xs font-medium tracking-widest uppercase"
            style={{ color: "#D4AF37" }}
          >
            Intelligence Stream
          </span>
          <span
            className="stream-status flex items-center gap-2 text-xs opacity-0"
            style={{ color: isStreaming ? "#4ADE80" : "#8899AA" }}
          >
            <span
              className="inline-block h-1.5 w-1.5 rounded-full"
              style={{
                backgroundColor: isStreaming ? "#4ADE80" : "#8899AA",
              }}
            />
            {isStreaming ? "LIVE" : "IDLE"}
          </span>
        </div>

        {/* Divider */}
        <div
          className="mb-6 h-px w-full"
          style={{ backgroundColor: "rgba(212, 175, 55, 0.15)" }}
        />

        {/* Streamed paragraphs */}
        <div className="space-y-4">
          {paragraphs.map((text, i) => {
            const shown = displayedChars[i] || 0;
            if (shown === 0 && activeParagraph < i) return null;

            return (
              <p
                key={i}
                className={`stream-para-${i} text-sm leading-relaxed`}
                style={{ color: "#C8D4E0" }}
              >
                {text.slice(0, shown)}
                {/* Blinking cursor at active paragraph */}
                {i === activeParagraph && isStreaming && (
                  <span
                    className="stream-cursor ml-0.5 inline-block h-4 w-[2px] align-middle"
                    style={{
                      backgroundColor: "#D4AF37",
                      animation: "blink 0.8s step-end infinite",
                    }}
                  />
                )}
              </p>
            );
          })}
        </div>

        {/* Progress indicator */}
        {isStreaming && (
          <div className="mt-8 flex items-center gap-3">
            <div
              className="h-[2px] flex-1 overflow-hidden rounded-full"
              style={{ backgroundColor: "rgba(212, 175, 55, 0.1)" }}
            >
              <div
                className="h-full rounded-full transition-all duration-300"
                style={{
                  backgroundColor: "#D4AF37",
                  width: `${
                    (displayedChars.reduce((a, b) => a + b, 0) /
                      paragraphs.reduce((a, t) => a + t.length, 0)) *
                    100
                  }%`,
                }}
              />
            </div>
            <span className="text-xs" style={{ color: "#556677" }}>
              {Math.round(
                (displayedChars.reduce((a, b) => a + b, 0) /
                  paragraphs.reduce((a, t) => a + t.length, 0)) *
                  100
              )}
              %
            </span>
          </div>
        )}
      </div>

      {/* CSS for cursor blink */}
      <style>{`
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
      `}</style>
    </div>
  );
}
```

---

## 4. Pros/Cons vs Motion (Framer Motion) Approach

### GSAP + MCP Pros

| Advantage | Detail |
|-----------|--------|
| **Timeline sequencing** | gsap.timeline() makes multi-phase orchestration trivial -- phases chain naturally with overlap control (`"-=0.3"`) |
| **SplitText plugin** | Native character/word/line splitting with no extra library -- Motion has no equivalent |
| **ScrollTrigger** | Best-in-class scroll-linked animations with pin, scrub, snap -- far more powerful than Motion's `useScroll` |
| **Performance ceiling** | GSAP uses requestAnimationFrame with internal batching -- consistently hits 60fps on complex sequences |
| **MCP-assisted development** | The 6 MCP tools provide expert debugging, optimization, and production patterns on demand |
| **Plugin ecosystem** | DrawSVG, MorphSVG, Draggable, Flip -- all free, all battle-tested |
| **Precision** | Frame-accurate timing, custom eases, and physics-based springs via `elastic.out()` |

### GSAP + MCP Cons

| Disadvantage | Detail |
|--------------|--------|
| **Imperative model** | Refs + `useGSAP` hook is less React-idiomatic than Motion's declarative `<motion.div>` |
| **Bundle size** | gsap core + plugins is ~30KB gzipped vs Motion's ~18KB (though tree-shaking helps) |
| **Layout animations** | Motion's `layout` prop handles layout changes automatically; GSAP needs manual Flip plugin work |
| **AnimatePresence** | Motion's exit animations are trivial; GSAP requires manual timeline management for unmounting |
| **Learning curve** | Timeline, ScrollTrigger, SplitText each have their own API surface to master |
| **MCP reliability** | MCP server depends on npx + external package; potential cold-start latency |
| **React 19 compat** | `@gsap/react` is maintained but trails React releases slightly |

### Verdict

For the reveal/briefing/streaming use case: **GSAP wins decisively**. The timeline sequencing, SplitText character reveals, and multi-phase orchestration are exactly what GSAP excels at. Motion is better for simple hover/tap interactions and layout animations, but cannot match GSAP's choreography capabilities for cinematic sequences.

---

## 5. What This Enables for Future Work

### Immediate Capabilities

1. **MCP-assisted animation authoring** -- describe an animation in natural language via `understand_and_create_animation` and get production-ready GSAP code
2. **Performance debugging** -- use `debug_animation_issue` when animations drop frames on mobile
3. **Production patterns library** -- `create_production_pattern` provides hero sections, scroll reveals, text treatments, and loading sequences as starting points

### Architecture Patterns Unlocked

- **Phase-based reveal orchestration** -- RevealSequence demonstrates the idle -> input -> generate -> reveal -> complete pattern that can be reused across any AI-driven UI
- **Streaming text with GSAP** -- StreamingSimulation shows how to animate character-level reveals without SplitText, useful for real LLM streaming responses
- **Scroll-driven dashboards** -- SectionAssembly's ScrollTrigger pattern scales to full briefing pages with pinned sections, progress tracking, and parallax
- **Composable timelines** -- each component creates its own timeline; these can be nested into a master timeline for full-page orchestration

### Integration Path

```
GSAP MCP tools   ->   prototype animation code
                 ->   debug + optimize
                 ->   production pattern library
                 ->   reusable component system for PAI briefings
```

The GSAP MCP server is now available in this project. To use the tools, address them via `mcp__gsap-master__understand_and_create_animation` (or any of the 6 tool names) in any Claude Code session running from this project directory.
