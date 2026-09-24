# Design before code (stories with a screen)

A screen is designed and approved before its code is written. Rework in a mockup costs minutes; rework in components costs hours.

## Before code

1. **Start from what ships.** If the app already runs, take fresh screenshots of the current screens (shell, fonts, spacing, tokens) and design from those, not from memory or the design docs alone.
2. **Screen inventory entry** in `docs/04-design/DESIGN.md`: screen name, route, roles, purpose, primary action, data shown, requirement and story IDs.
3. **States:** loading, empty, error, success, and permission denied where roles apply. Each needs a design, not just the happy path.
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
