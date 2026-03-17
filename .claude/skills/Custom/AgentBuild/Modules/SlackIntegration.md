# Module: Messaging — Slack Integration

> AI-native Slack integration for applications that communicate with users via DMs, channels, and threads. Handles connection modes, session isolation, message delivery, streaming, and access control.

**Module status:** NEW
**Pattern source:** OpenClaw Slack channel architecture (docs.openclaw.ai)
**When to use:** Any project where the AI agent communicates with users through Slack — briefing delivery, conversational assistants, notification bots, team-facing AI tools
**When NOT to use:** Projects that only need simple webhook notifications (use Slack Incoming Webhooks directly); projects using Discord or other platforms

---

## What This Module Provides

| Capability | What You Get |
|-----------|--------------|
| Dual connection mode | Socket Mode (dev/simple) and HTTP Events API (production) |
| Session isolation | Separate conversation context for DMs, channels, and threads |
| Message delivery | Chunked long messages, paragraph-aware splitting, proactive delivery |
| Text streaming | Real-time response streaming via Slack Agents & AI Apps API |
| Access control | Layered DM policy, channel policy, mention gating, per-channel config |
| Acknowledgment UX | Immediate emoji reaction ("I heard you") while processing |
| File handling | Inbound attachment download, outbound file delivery |
| Graceful degradation | Fallback to simpler delivery when advanced features unavailable |

---

## Toolchain Selection

| Decision | Selection | Rationale |
|---------|-----------|-----------|
| SDK | `@slack/bolt` | Official Slack SDK, supports both Socket Mode and HTTP, well-documented |
| Socket adapter | `@slack/socket-mode` | Required for Socket Mode (WebSocket, no public URL needed) |
| Connection mode (dev) | Socket Mode | No public endpoint, simpler setup, works behind firewalls |
| Connection mode (prod) | HTTP Events API | Scalable, stateless, works behind load balancers |
| Streaming | Slack Agents & AI Apps API | Native text streaming for conversational AI responses |

---

## Environment Variables Required

```bash
# .env (never commit)

# Required — both modes
SLACK_BOT_TOKEN=xoxb-...              # Bot user OAuth token (Bot Token Scopes)
SLACK_SIGNING_SECRET=...              # Verify incoming requests (HTTP mode)

# Required — Socket Mode only
SLACK_APP_TOKEN=xapp-...              # App-level token with connections:write scope

# Optional — streaming
# No env var needed — streaming uses bot token with assistant:write scope

# Optional — proactive messaging
# Bot must be in the channel or have a DM open with the user
```

---

## AGENTS.md Additions

Add this block to the Domain-Specific Notes section of AGENTS.md:

```markdown
## Slack Integration

- All Slack communication uses `@slack/bolt` — do NOT use raw Slack Web API directly
- Two connection modes: Socket Mode (dev, no public URL) and HTTP Events (prod, needs public endpoint)
- Session isolation pattern: DMs = user-scoped, channels = channel-scoped, threads = thread-scoped
- Message chunking: split long messages at paragraph boundaries, max 4000 chars per message
- Acknowledgment pattern: react with emoji immediately on message receipt, remove after response sent
- Mention gating: in channels, only respond when @mentioned (prevents noise)
- Proactive delivery: use `app.client.chat.postMessage()` with channel/user ID to initiate messages
- Thread replies: always use `thread_ts` to keep conversations organized
- File attachments: download from Slack's private URLs using bot token, upload via `files.uploadV2`
- Error handling: if streaming unavailable, fall back to normal message; never hard-fail on optional features
- User ID format: always a string like `U0123ABC` — never assume numeric
```

---

## Architecture Patterns (Extracted from OpenClaw)

### Pattern 1: Dual Connection Mode

```
┌─────────────────┐     ┌──────────────────┐
│   Socket Mode   │     │  HTTP Events API  │
│  (Development)  │     │   (Production)    │
├─────────────────┤     ├──────────────────┤
│ WebSocket out   │     │ Webhook in        │
│ No public URL   │     │ Public endpoint   │
│ App token req'd │     │ Signing secret    │
│ Simple setup    │     │ Scalable          │
│ Single instance │     │ Multi-instance    │
└─────────────────┘     └──────────────────┘
```

**Decision guide for agent-generated code:**
- If `SLACK_APP_TOKEN` is set → use Socket Mode
- If `SLACK_SIGNING_SECRET` is set but no app token → use HTTP Events API
- If both are set → prefer HTTP Events API (production-ready)

### Pattern 2: Session Isolation by Conversation Type

Every conversation with the AI agent gets its own context scope:

```typescript
// Session key generation pattern
function getSessionKey(event: SlackEvent): string {
  const base = `agent:${agentId}:slack`

  if (event.channel_type === 'im') {
    // DMs: one session per user
    return `${base}:dm:${event.user}`
  }

  if (event.thread_ts) {
    // Thread: isolated sub-session
    return `${base}:channel:${event.channel}:thread:${event.thread_ts}`
  }

  // Channel: shared session per channel
  return `${base}:channel:${event.channel}`
}
```

**Why this matters for AI agents:** Without session isolation, a user asking a follow-up question in a thread gets polluted context from the main channel. OpenClaw solved this by scoping sessions to the conversation boundary — DMs are personal, channels are shared, threads are isolated follow-ups.

**Thread history configuration:**
- `inheritParent: false` (default) — threads start fresh, don't inherit channel context
- `initialHistoryLimit: 20` — on thread start, fetch up to 20 prior messages for context
- These are configurable per project based on use case

### Pattern 3: Hierarchical Access Control

Layered permissions prevent the bot from responding where it shouldn't:

```
Global defaults
  └── DM policy (who can DM the bot?)
       ├── open — anyone
       ├── allowlist — specific users only
       └── disabled — no DMs
  └── Channel policy (which channels?)
       ├── open — all channels the bot is in
       ├── allowlist — specific channels only
       └── disabled — no channel responses
  └── Per-channel overrides
       ├── requireMention — only respond when @mentioned
       ├── allowedUsers — restrict who triggers the bot
       └── systemPrompt — channel-specific behavior
```

**Implementation pattern:**

```typescript
// config/slack.ts
export const slackConfig = {
  dm: {
    enabled: true,
    policy: 'open' as 'open' | 'allowlist' | 'disabled',
    allowlist: [] as string[], // user IDs
  },
  channels: {
    policy: 'allowlist' as 'open' | 'allowlist' | 'disabled',
    requireMention: true, // default: only respond when @mentioned
    allowlist: [] as string[], // channel IDs
    overrides: {} as Record<string, {
      requireMention?: boolean
      allowedUsers?: string[]
      systemPrompt?: string
    }>,
  },
}
```

### Pattern 4: Message Delivery with Paragraph-Aware Chunking

```typescript
// utils/chunk.ts
const SLACK_MAX_LENGTH = 4000

export function chunkMessage(text: string): string[] {
  if (text.length <= SLACK_MAX_LENGTH) return [text]

  const chunks: string[] = []
  const paragraphs = text.split('\n\n')
  let current = ''

  for (const para of paragraphs) {
    if ((current + '\n\n' + para).length > SLACK_MAX_LENGTH) {
      if (current) chunks.push(current.trim())
      // If single paragraph exceeds limit, split at sentence boundaries
      if (para.length > SLACK_MAX_LENGTH) {
        const sentences = para.match(/[^.!?]+[.!?]+/g) || [para]
        let sentenceChunk = ''
        for (const s of sentences) {
          if ((sentenceChunk + s).length > SLACK_MAX_LENGTH) {
            chunks.push(sentenceChunk.trim())
            sentenceChunk = s
          } else {
            sentenceChunk += s
          }
        }
        current = sentenceChunk
      } else {
        current = para
      }
    } else {
      current = current ? `${current}\n\n${para}` : para
    }
  }
  if (current) chunks.push(current.trim())
  return chunks
}
```

### Pattern 5: Text Streaming via Slack Agents API

```typescript
// For conversational AI responses — feels real-time like ChatGPT
// Requires: "Agents and AI Apps" enabled in Slack app settings
// Requires: assistant:write scope on bot token

async function streamResponse(
  app: App,
  channelId: string,
  threadTs: string,
  generateResponse: AsyncGenerator<string>
) {
  let streamId: string | null = null

  try {
    for await (const chunk of generateResponse) {
      if (!streamId) {
        // Start stream with first chunk
        const result = await app.client.assistant.threads.setStatus({
          channel_id: channelId,
          thread_ts: threadTs,
          status: 'is thinking...',
        })
        // Post first message, then update it
        const msg = await app.client.chat.postMessage({
          channel: channelId,
          thread_ts: threadTs,
          text: chunk,
        })
        streamId = msg.ts!
      } else {
        // Append to existing message
        await app.client.chat.update({
          channel: channelId,
          ts: streamId,
          text: chunk, // Full accumulated text
        })
      }
    }
  } catch (error) {
    // Fallback: send as normal message if streaming fails
    const fullText = /* collect remaining chunks */
    await app.client.chat.postMessage({
      channel: channelId,
      thread_ts: threadTs,
      text: fullText,
    })
  }
}
```

### Pattern 6: Acknowledgment Reaction

```typescript
// Immediately react to show "I heard you, working on it"
app.event('message', async ({ event, client }) => {
  // Acknowledge immediately
  await client.reactions.add({
    channel: event.channel,
    timestamp: event.ts,
    name: 'eyes', // 👀
  })

  try {
    // Process the message (may take seconds)
    const response = await processMessage(event)
    await deliverResponse(client, event, response)
  } finally {
    // Remove ack reaction after response sent
    await client.reactions.remove({
      channel: event.channel,
      timestamp: event.ts,
      name: 'eyes',
    }).catch(() => {}) // ignore if already removed
  }
})
```

### Pattern 7: Graceful Degradation

```typescript
// Feature detection — don't hard-fail on optional capabilities
async function detectCapabilities(app: App): Promise<SlackCapabilities> {
  return {
    streaming: await checkScope(app, 'assistant:write'),
    fileUpload: await checkScope(app, 'files:write'),
    reactions: await checkScope(app, 'reactions:write'),
    userInfo: await checkScope(app, 'users:read'),
  }
}

// Use capabilities with fallbacks
async function sendResponse(app: App, caps: SlackCapabilities, ...) {
  if (caps.streaming && isConversational) {
    try { return await streamResponse(...) } catch { /* fall through */ }
  }

  // Fallback: chunked normal messages
  const chunks = chunkMessage(response)
  for (const chunk of chunks) {
    await app.client.chat.postMessage({ channel, thread_ts, text: chunk })
  }
}
```

---

## Standard Implementation Pattern

### Socket Mode Setup (Development)

```typescript
// src/slack/app.ts
import { App } from '@slack/bolt'
import { logger } from '../observability/logger'

export function createSlackApp() {
  const app = new App({
    token: process.env.SLACK_BOT_TOKEN,
    appToken: process.env.SLACK_APP_TOKEN,
    socketMode: true,
    logger: {
      debug: (...msgs) => logger.debug(msgs.join(' ')),
      info: (...msgs) => logger.info(msgs.join(' ')),
      warn: (...msgs) => logger.warn(msgs.join(' ')),
      error: (...msgs) => logger.error(msgs.join(' ')),
      getLevel: () => 'info',
      setLevel: () => {},
      setName: () => {},
    },
  })

  registerEventHandlers(app)
  return app
}
```

### HTTP Events Setup (Production)

```typescript
// src/slack/app.ts — production mode
import { App, ExpressReceiver } from '@slack/bolt'

export function createSlackApp(expressApp: Express) {
  const receiver = new ExpressReceiver({
    signingSecret: process.env.SLACK_SIGNING_SECRET!,
    app: expressApp,
    endpoints: '/slack/events',
  })

  const app = new App({
    token: process.env.SLACK_BOT_TOKEN,
    receiver,
  })

  registerEventHandlers(app)
  return app
}
```

### Event Handler Registration

```typescript
// src/slack/events.ts
export function registerEventHandlers(app: App) {
  // DM handler — personal context
  app.message(async ({ message, client, say }) => {
    if (message.channel_type !== 'im') return
    const sessionKey = `dm:${message.user}`
    // ... process with user-scoped session
  })

  // Channel mention handler — shared context
  app.event('app_mention', async ({ event, client }) => {
    const sessionKey = event.thread_ts
      ? `channel:${event.channel}:thread:${event.thread_ts}`
      : `channel:${event.channel}`
    // ... process with channel/thread-scoped session
  })

  // Proactive delivery — bot-initiated messages
  // Used for briefing notifications, scheduled content
  // Called from your application logic, not from Slack events
}
```

### Proactive Message Delivery (Bot-Initiated)

```typescript
// src/slack/delivery.ts
// For sending briefings, notifications, and scheduled content

export async function deliverBriefing(
  app: App,
  userId: string,
  briefing: Briefing
) {
  // Open DM channel with user
  const dm = await app.client.conversations.open({ users: userId })
  const channelId = dm.channel!.id!

  // Chunk the briefing content
  const chunks = chunkMessage(formatBriefing(briefing))

  // Send header
  await app.client.chat.postMessage({
    channel: channelId,
    text: `📋 *Your briefing on ${briefing.topic} is ready*`,
  })

  // Send content chunks
  for (const chunk of chunks) {
    await app.client.chat.postMessage({
      channel: channelId,
      text: chunk,
    })
  }
}
```

---

## Slack App Configuration

### Required Bot Token Scopes

```
# Core messaging
chat:write              — Send messages
channels:history        — Read channel messages
groups:history          — Read private channel messages
im:history              — Read DM messages
mpim:history            — Read group DM messages

# Event subscriptions
app_mentions:read       — Detect @mentions

# Reactions (for ack pattern)
reactions:write         — Add/remove emoji reactions
reactions:read          — Read reactions

# File handling
files:read              — Access shared files
files:write             — Upload files

# User context
users:read              — Resolve user info

# Streaming (optional — for Agents API)
assistant:write         — Text streaming in threads

# DM initiation
im:write                — Open DM channels for proactive messaging
```

### Required Event Subscriptions

```
message.channels        — Messages in public channels
message.groups          — Messages in private channels
message.im              — Direct messages
message.mpim            — Group direct messages
app_mention             — Bot @mentioned
```

### Slack App Manifest (Partial)

```json
{
  "display_information": {
    "name": "[Project Name]",
    "description": "[From Phase 0 orientation]"
  },
  "features": {
    "bot_user": {
      "display_name": "[Project Name]",
      "always_online": true
    },
    "assistant_view": {
      "enabled": true
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "chat:write", "channels:history", "groups:history",
        "im:history", "mpim:history", "app_mentions:read",
        "reactions:write", "reactions:read",
        "files:read", "files:write",
        "users:read", "assistant:write", "im:write"
      ]
    }
  },
  "settings": {
    "event_subscriptions": {
      "bot_events": [
        "message.channels", "message.groups",
        "message.im", "message.mpim", "app_mention"
      ]
    },
    "socket_mode_enabled": true
  }
}
```

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Bot doesn't respond in channel | Missing `app_mentions:read` scope or mention gating active | Add scope; ensure user @mentions the bot |
| DMs not received | Missing `im:history` scope or Socket Mode not enabled | Check scopes; enable Socket Mode in app settings |
| Messages truncated | Single message exceeds 4000 chars | Use chunking utility with paragraph-aware splitting |
| Streaming not working | Missing `assistant:write` scope or Agents API not enabled | Enable "Agents and AI Apps" in Slack app settings |
| Proactive DM fails | Bot hasn't opened DM channel with user | Use `conversations.open` before `chat.postMessage` |
| Rate limited | Too many API calls (Slack tier limits) | Implement exponential backoff; batch messages where possible |
| Socket Mode disconnects | App token missing `connections:write` scope | Regenerate app token with correct scope |
| Thread context polluted | Not using `thread_ts` for replies | Always reply with `thread_ts` to keep threads isolated |

---

## Test Coverage Required

```typescript
// tests/slack/integration.test.ts
describe('Slack Integration', () => {
  // Connection
  it('should connect via Socket Mode when app token is provided')
  it('should connect via HTTP when signing secret is provided')

  // Session isolation
  it('should create separate sessions for DMs vs channels')
  it('should create isolated sessions for threads')
  it('should not leak context between conversation types')

  // Message delivery
  it('should chunk messages longer than 4000 characters')
  it('should split at paragraph boundaries, not mid-sentence')
  it('should deliver all chunks in order')

  // Acknowledgment
  it('should react with eyes emoji on message receipt')
  it('should remove reaction after response is sent')

  // Access control
  it('should only respond to @mentions in channels by default')
  it('should respond to all DMs when policy is open')
  it('should reject DMs from non-allowlisted users when policy is allowlist')

  // Proactive delivery
  it('should open DM channel before sending proactive message')
  it('should chunk long briefings into multiple messages')

  // Graceful degradation
  it('should fall back to normal message when streaming unavailable')
  it('should continue text delivery when file upload fails')
})
```

---

## Dashboard Setup Checklist

Before first deployment:
- [ ] Create Slack app at api.slack.com/apps
- [ ] Enable Socket Mode (for development)
- [ ] Generate App-Level Token with `connections:write` scope → `SLACK_APP_TOKEN`
- [ ] Install app to workspace → copy Bot Token → `SLACK_BOT_TOKEN`
- [ ] Copy Signing Secret → `SLACK_SIGNING_SECRET`
- [ ] Add all required Bot Token Scopes (see list above)
- [ ] Subscribe to required events (see list above)
- [ ] Enable "Agents and AI Apps" feature (for streaming)
- [ ] Add bot to relevant channels
- [ ] Test: send DM to bot, verify response
- [ ] Test: @mention bot in channel, verify response

---

*Module maintained by AgentBuild. Patterns extracted from OpenClaw (docs.openclaw.ai/channels/slack). Update Known Issues when new failures are discovered.*
