# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**RetailIQ** is a standalone single-file retail inventory forecasting dashboard.

- **Entry point**: `inventory-forecast.html` — all HTML, CSS, and JS in one file
- **No build step** — open directly in a browser, no server required
- **No package manager** — no npm, no node_modules
- **One external dependency**: Chart.js v4.4.0 via CDN

## Running & Testing

Open `inventory-forecast.html` directly in a browser. There is no build, lint, or automated test command.

After making changes, manually verify:
1. Navigate all pages: Dashboard, SKU Explorer, Forecast Board, Alerts
2. Click a SKU row → SKU Detail renders with charts and similar SKUs
3. Toggle view modes (table / cards / heatmap) on SKU Explorer
4. Switch mode tabs (Summary / Forecast / Operations)

## Architecture

### Data
All inventory data is in the `skus` array (mock data, no backend). Each SKU:
```js
{ id, name, cat, supplier, lead, stock, safety, rop, forecast, status, trend, dos }
```
`status` is always one of `"critical"`, `"low"`, `"healthy"`. Modifying `skus` is all that's needed to change displayed data.

### Routing
Pages are `<div class="page" id="page-{name}">` elements toggled via `.active` class — no router library. The `navigate(pageId)` function handles routing, title updates, and nav highlighting. Page titles/subtitles are in the `pageTitles` config object.

### Config Objects (top of `<script>`)
Status-to-style mappings are centralized:
- `statusColor` → CSS color value (e.g. `var(--red)`)
- `statusClass` → badge class (e.g. `badge-red`)
- `statusLabel` → display text (e.g. `"Critical"`)
- `hmClass` → heatmap cell class

### Rendering
`render*()` functions build HTML strings and assign to `innerHTML`. All content is pre-rendered on page load. SKU detail is re-generated on each `openSKU(id)` call.

### Charts
- Dashboard charts are created once in IIFEs and never destroyed
- Detail forecast chart uses `detailChartInstance` — always call `.destroy()` before recreating
- Use CSS variables (`var(--accent)`, `var(--green)`, etc.) for chart colors

## Conventions

### CSS
- **Always use CSS variables** — never hardcode hex values
- Available theme variables: `--bg`, `--surface`, `--surface2`, `--border`, `--accent`, `--accent2`, `--green`, `--yellow`, `--red`, `--text`, `--muted`
- Layout: Flexbox for sidebar/nav/button rows, CSS Grid for KPI cards/chart rows/detail panels
- Hover transitions: `all .15s`

### JavaScript
- Dynamic HTML via template literals
- Naming: `render*()` for DOM-building, `open*()` for navigation/actions
- Inline `onclick` on dynamically generated rows: `onclick="openSKU('${s.id}')"`
- Loop variable `s` for a single SKU; `tbody`/`grid` for DOM containers

### ID Conventions
- Page containers: `page-{name}`
- SKU detail fields: `detail-{field}` (e.g. `detail-stock`, `detail-rop`)
- Chart canvases: `{name}Chart` (e.g. `dashForecastChart`, `detailForecastChart`)

## How to Extend

**Add a SKU**: Append an object to the `skus` array.

**Add a page**:
1. Add `<div class="page" id="page-{name}">` in the HTML
2. Add entry to `pageTitles`
3. Add `.nav-item` with `data-page="{name}"` in the sidebar

**Add a chart**: Use the IIFE pattern for isolation; for the detail page, follow the `detailChartInstance` destroy/recreate pattern.

**Add a status type**: Update all four config objects (`statusColor`, `statusClass`, `statusLabel`, `hmClass`).

## Constraints

- Keep it a single HTML file — no build system, bundler, or npm
- Do not add CDN dependencies without documenting them in AGENTS.md
- Do not add localStorage persistence unless explicitly requested
- Dates are hardcoded to Spring 2026 — update when touching time-sensitive content
