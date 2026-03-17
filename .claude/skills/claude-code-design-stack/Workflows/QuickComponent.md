# Design Stack — Quick Component Workflow

Fast path for a single polished component. Skips mockup generation. Uses 21st.dev Magic for generation and UI/UX Pro Max for validation and design reasoning.

---

## When to Use

- User needs a specific component (modal, table, card, form, navbar)
- The project already has a design system (check for `design-system/MASTER.md`)
- No mockup needed — the requirement is clear

---

## Step 1: Understand the Component

Don't just accept "make me a modal." Ask:

> "What triggers this [component]? What's inside it? What happens when the user is done with it?"

Extract:
- **Purpose** — what user action this serves
- **Content** — what's displayed inside
- **Interactions** — states (default, hover, active, disabled, loading, error)
- **Context** — where this sits in the page and what surrounds it

**Push back on under-specified requests:**

> "A 'card component' could be anything from a product listing to a stats widget to a user profile preview. They have completely different information hierarchies. What data is in this card, and what should the user do with it?"

## Step 2: Check for Existing Design System

Look for `design-system/MASTER.md` in the project.

**If it exists:** Load the locked tokens (style, palette, fonts, spacing) and use them as constraints for generation. Also check for page-specific overrides in `design-system/pages/`.

**If it doesn't exist:** Run a quick design system generation:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <style_keywords>" --design-system -p "<Project Name>"
```

> "You don't have a design system set up for this project yet. I've generated one based on [inferred product type]. Want to review it before I generate the component, or should I use these defaults?"

## Step 3: Generate with 21st.dev Magic

### 21st.dev Magic Tools (prefixed `mcp__magic__` in Claude Code)

| Tool | When |
|------|------|
| `21st_magic_component_inspiration` | First — browse existing components for reference |
| `21st_magic_component_builder` | Generate the component with full design context |
| `21st_magic_component_refiner` | Polish/fix issues after initial generation |
| `logo_search` | If the component needs brand logos (JSX/TSX/SVG) |

### Step 3a: Search for Inspiration (Optional)

```
mcp__magic__21st_magic_component_inspiration({
  message: "Looking for [component type] for a professional [product type]",
  searchQuery: "[2-4 words, e.g. 'status card grid']"
})
```

### Step 3b: Generate

```
mcp__magic__21st_magic_component_builder({
  message: "<user's original request>",
  searchQuery: "<2-4 word component search>",
  absolutePathToCurrentFile: "<target file path>",
  absolutePathToProjectDirectory: "<project root>",
  standaloneRequestQuery: "<detailed component spec with design tokens from MASTER.md>"
})
```

**Embed the design system in `standaloneRequestQuery`** — colors, fonts, spacing, border-radius, shadow levels, and interaction states from MASTER.md.

### Step 3c: Refine if Needed

```
mcp__magic__21st_magic_component_refiner({
  userMessage: "<what to improve>",
  absolutePathToRefiningFile: "<path to generated component>",
  context: "<specific elements and aspects to fix>"
})
```

**One component per request.** If the user asks for something complex (e.g., "a settings page"), decompose it:

> "A settings page isn't one component — it's a layout with a sidebar navigation, form sections, toggle groups, and a save bar. I'll generate each piece separately for better quality. Starting with the sidebar navigation."

**If 21st.dev Magic MCP is not connected** (added mid-session), fall back to the `frontend-design` plugin skill with the MASTER.md design tokens.

## Step 4: Validate (Non-Negotiable)

Run every generated component through UI/UX Pro Max checks before presenting:

**Must pass:**
- [ ] Color contrast 4.5:1 minimum against the locked palette
- [ ] Focus states visible on all interactive elements
- [ ] Touch targets 44x44px minimum
- [ ] cursor-pointer on clickable elements
- [ ] No emojis as icons (use Lucide/Heroicons)
- [ ] Loading/disabled states for async actions
- [ ] Transitions 150-300ms (not instant, not sluggish)
- [ ] Semantic HTML and ARIA labels where needed

**If the generated component violates any of these, fix it before showing the user. Don't deliver broken components and call them "starting points."**

## Step 5: Deliver with Context

Present the component with:

> "Here's your [component name]:
>
> **Design system:** Using [style/palette/fonts] from your project's MASTER.md
> **States:** [list all interaction states implemented]
> **Accessibility:** [specific checks that passed]
> **Usage:** [how to import/use this component, any props it accepts]
>
> One thing to watch: [any caveat — e.g., 'this dropdown needs a click-outside handler that depends on your app's event system']"
