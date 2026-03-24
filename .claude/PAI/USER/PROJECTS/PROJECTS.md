# Projects Registry

Your project definitions and metadata. PAI uses this to route requests to the correct project context.

## Master Registry

| Project | Path | URL | Stack |
|---------|------|-----|-------|
| Example Website | `~/Projects/MySite` | `mysite.com` | Astro, React, TypeScript |
| Example API | `~/Projects/MyAPI` | `api.mysite.com` | Hono, Cloudflare Workers |

## Optional Detailed Project Files

```text
PROJECTS/
├── PROJECTS.md
├── website.md
└── api.md
```
