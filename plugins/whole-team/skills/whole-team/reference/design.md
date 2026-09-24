# Design before code (stories with a screen)

A screen is designed and approved before its code is written. Rework in a mockup costs minutes; rework in components costs hours.

## Design tools: use what is installed, recommend what is missing

At the first story with a screen, check which design and front-end skills or tools the agent already has (the skill list in your context, installed plugins, connected MCP servers). Use them for the mockup and the build:

| Need | Look for | If missing, recommend (the owner installs, or you run it after a yes) |
|------|----------|------------------------------------------------------------------------|
| Distinctive, production-grade UI instead of generic AI look | a `frontend-design` skill | Claude Code: `/plugin install frontend-design@claude-plugins-official`. Any agent: `npx skills add anthropics/skills --skill frontend-design` |
| Colours, type and theme tokens | a `theme-factory` skill, a design-system skill | `npx skills add anthropics/skills --skill theme-factory` |
| Designs that live in Figma | a Figma MCP server or skill | `claude mcp add --transport http figma https://mcp.figma.com/mcp` (other agents: add the same URL to their MCP settings) |
| Screenshots at each viewport, UI checks | a Playwright plugin or MCP, a `webapp-testing` skill | Claude Code: `/plugin install playwright@claude-plugins-official`. Any agent: `npx skills add anthropics/skills --skill webapp-testing` |
| A clickable HTML prototype | a `web-artifacts-builder` skill | `npx skills add anthropics/skills --skill web-artifacts-builder` |

Rules:
- Say which tool you are using and why, in the explanation block ([checkpoints.md](checkpoints.md)).
- Recommend at most two installs at a time, with one line on what each adds. Installing is the owner's call; never install without a yes.
- If the owner declines, carry on with what is there: a precise HTML or markdown wireframe is enough for approval.
- The project's own design system wins over any skill's defaults; pass the tokens from `DESIGN.md` to the skill.

## Before code

1. **Start from what ships.** If the app already runs, take fresh screenshots of the current screens (shell, fonts, spacing, tokens) and design from those, not from memory or the design docs alone.
2. **Screen inventory entry** in `docs/04-design/DESIGN.md`: screen name, route, roles, purpose, primary action, data shown, requirement and story IDs.
3. **States:** loading, empty, error, success, and permission denied where roles apply. Each state needs its own design, the happy path included.
4. **Mockup:** whatever the project uses (Figma, an HTML prototype, a static page, even a precise wireframe in markdown for lite). Show it at the project's viewports (default 390, 1024 and 1280 px).
5. **Owner review:** post the mockup and one question ("Approve this layout for US-014?"). Wait for a yes. Record approval in the story's notes.

## Design system (standard and strict)

Tokens for colour, type scale, spacing and radius in one place (`DESIGN.md` and the code's theme file, kept identical). Components listed with their states. New components only when an existing one cannot be adapted.

## Quality bar

- One primary action per screen.
- Status is never shown by colour alone: pair a label with a dot or icon.
- Keyboard reachable, visible focus, labels on every input, contrast at WCAG AA.
- No horizontal scroll at any target viewport.
- Avoid generic AI-looking UI unless the brand calls for it: decorative gradients, emoji as icons, grids of KPI cards with no decision attached, icons that carry no meaning.
- Copy is specific ("Upload your floor plan") rather than generic ("Submit").

## After code

- Screenshot every changed screen at each viewport and compare with the approved mockup; fix drift or get the owner's yes on the difference.
- Run an accessibility check (axe or the platform's equivalent) on changed screens.
- Update `DESIGN.md` so it describes what shipped.
