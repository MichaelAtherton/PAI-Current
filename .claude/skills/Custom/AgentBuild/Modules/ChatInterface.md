# Module: UI — Chat Interface

> Production-ready AI chat interface using composable React primitives. Handles streaming, markdown, code highlighting, tool visualization, attachments, and accessibility out of the box — with any LLM backend.

**Module status:** NEW
**Primary library:** [assistant-ui](https://github.com/assistant-ui/assistant-ui) (MIT, 8.6k stars, YC-backed)
**Design guidance:** OpenAI ChatKit widget patterns (extracted, not used as dependency)
**When to use:** Any project with a conversational AI interface — chatbots, co-pilots, learning assistants, support tools, briefing interfaces, agent dashboards
**When NOT to use:** Projects with no chat UI; projects using a full-stack platform that provides its own chat (e.g., Intercom, Drift); non-React frontends (see Alternatives section)

---

## What This Module Provides

| Capability | What You Get |
|-----------|--------------|
| Chat UI components | Thread, Composer, Message primitives — composable, not monolithic |
| Streaming | Real-time token rendering optimized for LLM responses |
| Markdown & code | Rich text, syntax-highlighted code blocks, LaTeX math |
| Tool visualization | Inline tool call rendering, human-in-the-loop approvals |
| Attachments | File upload in composer, attachment display in messages |
| Message actions | Copy, edit, regenerate, text-to-speech |
| Conversation branching | Navigate between conversation branches when editing messages |
| Theming | shadcn/ui + Radix primitives, CSS variables, dark/light mode |
| Accessibility | Keyboard navigation, screen reader support, auto-scroll |
| Provider-agnostic | Works with Claude, OpenAI, Gemini, Ollama, any LLM via runtime adapters |

---

## Toolchain Selection

| Decision | Selection | Rationale |
|---------|-----------|-----------|
| Chat UI library | `@assistant-ui/react` | Composable primitives (Radix-style), provider-agnostic, streaming-first, MIT licensed |
| LLM integration | Vercel AI SDK (`ai` + `@ai-sdk/anthropic`) | Standard streaming protocol, works with assistant-ui's runtime, supports Claude natively |
| Styling | shadcn/ui + Tailwind CSS | assistant-ui components are built on shadcn — consistent, customizable, no vendor CSS |
| State management | Built-in (assistant-ui runtime) | Handles streaming, retries, branching, interruptions — no Redux/Zustand needed for chat state |

**Why not OpenAI ChatKit?** ChatKit loads JavaScript from OpenAI's CDN (`cdn.platform.openai.com`) and requires `openai.chatkit.sessions.create()` for server-side auth — a hard dependency on OpenAI infrastructure. assistant-ui is fully self-hosted with no external runtime dependencies.

---

## Environment Variables Required

```bash
# .env (never commit)

# Required — Claude/Anthropic backend
ANTHROPIC_API_KEY=sk-ant-...          # Claude API key (server-side only)

# Alternative — OpenAI backend
# OPENAI_API_KEY=sk-...

# Optional — assistant-ui Cloud (thread persistence)
# ASSISTANT_UI_API_KEY=...            # Only if using AssistantCloud for thread history
```

---

## AGENTS.md Additions

Add this block to the Domain-Specific Notes section of AGENTS.md:

```markdown
## Chat Interface (assistant-ui)

- All chat UI uses `@assistant-ui/react` — do NOT build custom chat components from scratch
- Components are composable primitives (like Radix UI), not a single monolithic widget
- Streaming is handled by the runtime — never manually manage token buffering
- Use `AssistantRuntimeProvider` as the root wrapper — all chat components must be inside it
- Thread component handles: message list, auto-scroll, streaming indicators, and composer
- Tool calls render inline using `makeAssistantToolUI` — never hide tool execution from users
- Message branching: when users edit a message, previous branch is preserved and navigable
- Attachments: use `AttachmentPrimitive` for file display, not custom file components
- Theming: override via CSS variables or Tailwind — do NOT modify assistant-ui source
- API route at `/api/chat` handles LLM communication — keep all API keys server-side
- For Claude backend: use `@ai-sdk/anthropic` provider with Vercel AI SDK streaming
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    React App                         │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │         AssistantRuntimeProvider               │   │
│  │                                                │   │
│  │  ┌─────────────────────┐  ┌───────────────┐  │   │
│  │  │       Thread         │  │ AssistantModal│  │   │
│  │  │  ┌───────────────┐  │  │ (floating)    │  │   │
│  │  │  │  Messages      │  │  └───────────────┘  │   │
│  │  │  │  ├─ Text       │  │                      │   │
│  │  │  │  ├─ Markdown   │  │  ┌───────────────┐  │   │
│  │  │  │  ├─ Code       │  │  │AssistantSidebar│  │   │
│  │  │  │  ├─ ToolCall   │  │  │ (co-pilot)    │  │   │
│  │  │  │  ├─ Attachment  │  │  └───────────────┘  │   │
│  │  │  │  └─ Widget*    │  │                      │   │
│  │  │  └───────────────┘  │                      │   │
│  │  │  ┌───────────────┐  │                      │   │
│  │  │  │   Composer     │  │                      │   │
│  │  │  │  ├─ Input      │  │                      │   │
│  │  │  │  ├─ Send       │  │                      │   │
│  │  │  │  └─ Attachments│  │                      │   │
│  │  │  └───────────────┘  │                      │   │
│  │  └─────────────────────┘                      │   │
│  └──────────────────────────────────────────────┘   │
│                         │                            │
│                         ▼                            │
│              ┌─────────────────┐                    │
│              │    Runtime       │                    │
│              │  (AI SDK / Custom)│                   │
│              └────────┬────────┘                    │
└───────────────────────┼─────────────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │   /api/chat      │
              │  (Server Route)  │
              │                  │
              │  Claude / OpenAI │
              │  / Any LLM       │
              └─────────────────┘

* Widget = ChatKit-inspired rich components inside messages
  (forms, tables, cards, charts — see Widget Pattern section)
```

**Three deployment patterns:**

| Pattern | Component | Best For |
|---------|-----------|----------|
| **Full-page chat** | `<Thread />` | Dedicated chat apps, learning assistants |
| **Floating modal** | `<AssistantModal />` | Support widgets, help overlays |
| **Side panel** | `<AssistantSidebar />` | Co-pilot experiences, IDE-style assistants |

---

## Standard Implementation Pattern

### 1. Project Setup

```bash
# Option A: CLI scaffold (fastest)
npx assistant-ui@latest create my-chat-app
cd my-chat-app

# Option B: Add to existing Next.js/React project
npm install @assistant-ui/react ai @ai-sdk/anthropic
npx shadcn@latest init  # if not already using shadcn
```

### 2. API Route — Claude Backend (Next.js App Router)

```typescript
// app/api/chat/route.ts
import { anthropic } from '@ai-sdk/anthropic'
import { streamText } from 'ai'

export async function POST(req: Request) {
  const { messages, system } = await req.json()

  const result = streamText({
    model: anthropic('claude-sonnet-4-6'),
    system: system || 'You are a helpful assistant.',
    messages,
    // Tool definitions (optional)
    tools: {
      // Define tools here — they render inline in the chat
    },
  })

  return result.toDataStreamResponse()
}
```

### 3. API Route — Claude Backend (Express)

```typescript
// src/api/chat.ts
import { anthropic } from '@ai-sdk/anthropic'
import { streamText } from 'ai'
import { Router } from 'express'

const router = Router()

router.post('/api/chat', async (req, res) => {
  const { messages, system } = req.body

  const result = streamText({
    model: anthropic('claude-sonnet-4-6'),
    system: system || 'You are a helpful assistant.',
    messages,
  })

  result.pipeDataStreamToResponse(res)
})

export default router
```

### 4. Chat Page Component

```tsx
// app/page.tsx (Next.js) or src/components/Chat.tsx (any React)
'use client'

import { AssistantRuntimeProvider } from '@assistant-ui/react'
import { useVercelAIRuntime } from '@assistant-ui/react-ai-sdk'
import { useChat } from 'ai/react'
import { Thread } from '@/components/ui/assistant-ui/thread'

export default function ChatPage() {
  const chat = useChat({
    api: '/api/chat',
  })

  const runtime = useVercelAIRuntime(chat)

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Thread />
    </AssistantRuntimeProvider>
  )
}
```

### 5. Custom Runtime (No Vercel AI SDK)

```tsx
// For projects not using Vercel AI SDK
import { useLocalRuntime, type ChatModelAdapter } from '@assistant-ui/react'

const anthropicAdapter: ChatModelAdapter = {
  async *run({ messages, abortSignal }) {
    // Call your own API endpoint
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages }),
      signal: abortSignal,
    })

    const reader = response.body!.getReader()
    const decoder = new TextDecoder()
    let content = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      content += decoder.decode(value, { stream: true })
      yield { content: [{ type: 'text', text: content }] }
    }
  },
}

function ChatPage() {
  const runtime = useLocalRuntime(anthropicAdapter)

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Thread />
    </AssistantRuntimeProvider>
  )
}
```

---

## Tool Visualization (Agentic UI)

One of assistant-ui's strongest features — tool calls render inline with custom components.

### Defining Tool UI

```tsx
// components/tools/weather-tool.tsx
import { makeAssistantToolUI } from '@assistant-ui/react'

export const WeatherToolUI = makeAssistantToolUI({
  toolName: 'get_weather',
  render: ({ args, result, status }) => {
    if (status === 'running') {
      return <div className="animate-pulse">Checking weather for {args.city}...</div>
    }

    if (status === 'complete' && result) {
      return (
        <div className="rounded-lg border p-4">
          <h3 className="font-semibold">{result.city}</h3>
          <p className="text-2xl">{result.temperature}°F</p>
          <p className="text-muted-foreground">{result.conditions}</p>
        </div>
      )
    }

    return null
  },
})
```

### Human-in-the-Loop Approval

```tsx
// components/tools/approval-tool.tsx
import { makeAssistantToolUI } from '@assistant-ui/react'

export const DangerousActionToolUI = makeAssistantToolUI({
  toolName: 'delete_record',
  render: ({ args, result, status, addResult }) => {
    if (status === 'requires-action') {
      return (
        <div className="rounded-lg border-red-200 border p-4">
          <p>Delete record <strong>{args.recordId}</strong>?</p>
          <div className="flex gap-2 mt-2">
            <button
              onClick={() => addResult({ approved: true })}
              className="bg-red-500 text-white px-3 py-1 rounded"
            >
              Confirm Delete
            </button>
            <button
              onClick={() => addResult({ approved: false })}
              className="border px-3 py-1 rounded"
            >
              Cancel
            </button>
          </div>
        </div>
      )
    }

    return <p>{result?.approved ? 'Deleted.' : 'Cancelled.'}</p>
  },
})
```

### Registering Tool UIs

```tsx
// app/page.tsx
import { AssistantRuntimeProvider } from '@assistant-ui/react'
import { WeatherToolUI } from '@/components/tools/weather-tool'
import { DangerousActionToolUI } from '@/components/tools/approval-tool'

export default function ChatPage() {
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <WeatherToolUI />
      <DangerousActionToolUI />
      <Thread />
    </AssistantRuntimeProvider>
  )
}
```

---

## Widget Pattern (Extracted from OpenAI ChatKit)

OpenAI ChatKit's most powerful pattern is **rich widgets rendered inside chat messages** — not just text, but interactive components. assistant-ui supports this via custom message parts and tool UIs. Here's the pattern translated:

### ChatKit Widget Categories → assistant-ui Implementation

| ChatKit Widget Type | assistant-ui Equivalent | Use Case |
|--------------------|-----------------------|----------|
| **Form controls** (Input, Select, Checkbox, DatePicker) | Tool UI with `requires-action` status | Collect user input inline (preferences, filters, approvals) |
| **Data display** (Table, ListView, Card) | Custom `MessagePart` component | Show structured data (search results, reports, comparisons) |
| **Layout** (Box, Row, Col, Spacer) | Standard React + Tailwind in tool UI | Organize complex tool outputs |
| **Charts** (implied) | Tool UI wrapping chart library (Recharts, etc.) | Visualize data inline (metrics, trends) |
| **Media** (Image, Video) | `AttachmentPrimitive` + custom renderers | Display generated images, previews |
| **Navigation** (Link, Button) | Tool UI with clickable actions | Deep-link to app features from chat |
| **Status** (Progress, Badge, Alert) | Tool UI with streaming status | Show operation progress, system states |

### Example: Rich Data Widget (ChatKit-inspired)

```tsx
// components/tools/briefing-summary.tsx
// Inspired by ChatKit's Card + Table widget pattern
import { makeAssistantToolUI } from '@assistant-ui/react'

export const BriefingSummaryToolUI = makeAssistantToolUI({
  toolName: 'show_briefing_summary',
  render: ({ args, result, status }) => {
    if (status === 'running') {
      return (
        <div className="animate-pulse rounded-lg border p-4">
          <div className="h-4 bg-muted rounded w-3/4 mb-2" />
          <div className="h-4 bg-muted rounded w-1/2" />
        </div>
      )
    }

    if (!result) return null

    return (
      <div className="rounded-lg border overflow-hidden">
        {/* Card header */}
        <div className="bg-muted/50 px-4 py-3 border-b">
          <h3 className="font-semibold text-sm">{result.topic}</h3>
          <p className="text-xs text-muted-foreground">
            {result.sourceCount} sources · {result.readTime} min read
          </p>
        </div>

        {/* Key insights list */}
        <div className="px-4 py-3 space-y-2">
          {result.insights.map((insight: string, i: number) => (
            <div key={i} className="flex gap-2 text-sm">
              <span className="text-muted-foreground">{i + 1}.</span>
              <span>{insight}</span>
            </div>
          ))}
        </div>

        {/* Action footer */}
        <div className="bg-muted/30 px-4 py-2 border-t flex gap-2">
          <button className="text-xs text-primary hover:underline">
            Read full briefing
          </button>
          <span className="text-muted-foreground">·</span>
          <button className="text-xs text-primary hover:underline">
            Save to library
          </button>
        </div>
      </div>
    )
  },
})
```

### Example: Inline Form Widget (ChatKit-inspired)

```tsx
// components/tools/preference-collector.tsx
// Inspired by ChatKit's Form controls pattern
import { makeAssistantToolUI } from '@assistant-ui/react'
import { useState } from 'react'

export const PreferenceCollectorToolUI = makeAssistantToolUI({
  toolName: 'collect_preferences',
  render: ({ args, status, addResult }) => {
    const [selected, setSelected] = useState<string[]>([])

    if (status !== 'requires-action') return null

    return (
      <div className="rounded-lg border p-4 space-y-3">
        <p className="text-sm font-medium">{args.question}</p>
        <div className="flex flex-wrap gap-2">
          {args.options.map((option: string) => (
            <button
              key={option}
              onClick={() => setSelected(prev =>
                prev.includes(option)
                  ? prev.filter(o => o !== option)
                  : [...prev, option]
              )}
              className={`px-3 py-1 rounded-full text-sm border transition-colors ${
                selected.includes(option)
                  ? 'bg-primary text-primary-foreground'
                  : 'hover:bg-muted'
              }`}
            >
              {option}
            </button>
          ))}
        </div>
        <button
          onClick={() => addResult({ selections: selected })}
          className="bg-primary text-primary-foreground px-4 py-2 rounded text-sm"
          disabled={selected.length === 0}
        >
          Continue
        </button>
      </div>
    )
  },
})
```

---

## Theming & Customization

### CSS Variables (Quick Customization)

```css
/* globals.css — override assistant-ui defaults */
:root {
  --aui-thread-max-width: 42rem;
  --aui-composer-min-height: 3rem;
}

/* Dark mode */
.dark {
  --aui-message-bg: hsl(222 47% 11%);
  --aui-message-user-bg: hsl(222 47% 20%);
}
```

### Component Composition (Deep Customization)

```tsx
// components/ui/assistant-ui/custom-thread.tsx
import {
  ThreadPrimitive,
  ComposerPrimitive,
  MessagePrimitive,
} from '@assistant-ui/react'

export function CustomThread() {
  return (
    <ThreadPrimitive.Root className="flex flex-col h-full">
      <ThreadPrimitive.Viewport className="flex-1 overflow-y-auto p-4">
        <ThreadPrimitive.Messages
          components={{
            UserMessage: CustomUserMessage,
            AssistantMessage: CustomAssistantMessage,
          }}
        />
      </ThreadPrimitive.Viewport>

      <div className="border-t p-4">
        <ComposerPrimitive.Root className="flex gap-2">
          <ComposerPrimitive.Input
            placeholder="Ask anything..."
            className="flex-1 rounded-lg border px-4 py-2"
          />
          <ComposerPrimitive.Send className="bg-primary text-white rounded-lg px-4 py-2">
            Send
          </ComposerPrimitive.Send>
        </ComposerPrimitive.Root>
      </div>
    </ThreadPrimitive.Root>
  )
}
```

---

## Deployment Patterns

### Pattern A: Full-Page Chat (Learning Assistant, Briefing Platform)

```tsx
// Entire page is the chat
export default function ChatPage() {
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="h-screen">
        <Thread />
      </div>
    </AssistantRuntimeProvider>
  )
}
```

### Pattern B: Floating Modal (Support Widget)

```tsx
// Chat bubble in corner of any page
export default function AppLayout({ children }) {
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      {children}
      <AssistantModal />
    </AssistantRuntimeProvider>
  )
}
```

### Pattern C: Side Panel (Co-pilot)

```tsx
// Chat alongside main content
export default function WorkspacePage() {
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="flex h-screen">
        <main className="flex-1">{/* App content */}</main>
        <AssistantSidebar className="w-[400px] border-l" />
      </div>
    </AssistantRuntimeProvider>
  )
}
```

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Streaming stops mid-response | API route not returning stream properly | Use `result.toDataStreamResponse()` (Next.js) or `result.pipeDataStreamToResponse(res)` (Express) |
| Messages flash on re-render | Missing `key` prop or thread state reset | Ensure `AssistantRuntimeProvider` wraps the entire chat, not just the thread |
| Tool UI not rendering | Tool name mismatch between API and UI registration | `toolName` in `makeAssistantToolUI` must exactly match the tool name in `streamText({ tools })` |
| Attachments not uploading | Missing multipart handler on API route | Add file upload endpoint separate from `/api/chat` |
| Dark mode not applying | CSS variables not scoped to `.dark` class | Use `@media (prefers-color-scheme: dark)` or ensure `.dark` class on root element |
| Auto-scroll breaks | Custom scroll container interfering | Use `ThreadPrimitive.Viewport` instead of custom scroll wrapper |
| Message branching not visible | Using `Thread` component without enabling edit | Thread supports branching by default — ensure `ActionBarPrimitive.Edit` is rendered |
| Claude context window exceeded | Long conversations without truncation | Implement message windowing in API route — send last N messages |

---

## Test Coverage Required

```typescript
// tests/chat/interface.test.tsx
describe('Chat Interface', () => {
  // Rendering
  it('should render Thread component with empty state')
  it('should display user messages after sending')
  it('should render assistant messages with markdown formatting')
  it('should syntax-highlight code blocks in responses')

  // Streaming
  it('should show streaming indicator while response generates')
  it('should render tokens incrementally during streaming')
  it('should handle stream interruption gracefully')

  // Tool visualization
  it('should render custom tool UI for registered tools')
  it('should show loading state while tool executes')
  it('should handle human-in-the-loop approval flow')
  it('should fall back to default UI for unregistered tools')

  // Attachments
  it('should allow file upload via composer')
  it('should display attachments in messages')

  // Actions
  it('should copy message text to clipboard')
  it('should regenerate assistant response on retry')
  it('should support message editing with branch navigation')

  // Accessibility
  it('should support keyboard navigation through messages')
  it('should announce new messages to screen readers')
  it('should maintain focus management during streaming')

  // API integration
  it('should send messages to /api/chat endpoint')
  it('should handle API errors with user-visible error state')
  it('should include conversation history in API requests')
})
```

---

## Setup Checklist

Before first deployment:
- [ ] Install `@assistant-ui/react`, `ai`, and `@ai-sdk/anthropic`
- [ ] Initialize shadcn/ui if not already configured (`npx shadcn@latest init`)
- [ ] Add assistant-ui components (`npx assistant-ui@latest add thread`)
- [ ] Create API route at `/api/chat` with Claude backend
- [ ] Set `ANTHROPIC_API_KEY` in environment
- [ ] Wrap chat page in `AssistantRuntimeProvider`
- [ ] Add `Thread` (or `AssistantModal` / `AssistantSidebar`) component
- [ ] Register tool UIs for any tools defined in the API route
- [ ] Test: send message, verify streaming response
- [ ] Test: verify markdown and code block rendering
- [ ] Customize theme to match application design
- [ ] Test: dark mode rendering

---

## Alternatives

If assistant-ui doesn't fit your project:

| Library | Best For | Trade-off |
|---------|----------|-----------|
| [NLUX](https://www.npmjs.com/package/@nlux/react) | Quick prototypes, simple chat | Less customizable, fewer primitives |
| [LlamaIndex chat-ui](https://github.com/run-llama/chat-ui) | RAG applications using LlamaIndex | Tied to LlamaIndex ecosystem |
| [ProChat (Ant Design)](https://github.com/ant-design/pro-chat) | Ant Design projects | Brings full Ant Design dependency |
| [reachat](https://madewithreactjs.com/reachat) | Lightweight chat UIs | Smaller community, fewer features |
| Custom build | Full control needed | Significant engineering investment |

---

*Module maintained by AgentBuild. Primary library: assistant-ui. Widget patterns extracted from OpenAI ChatKit (github.com/openai/chatkit-js). Update Known Issues when new failures are discovered.*
