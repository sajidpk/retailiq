# AGENTS.md — RetailIQ Inventory Forecasting

Instructions for AI coding agents working in this repository.

## Project Overview

**RetailIQ** is a standalone single-file dashboard for retail inventory forecasting and management.

- **Entry point**: `inventory-forecast.html` (all HTML, CSS, and JS in one file)
- **No build step** — open directly in a browser, no server required
- **No package manager** — no `npm install`, no `node_modules`
- **One external dependency**: Chart.js v4.4.0 loaded via CDN:
  ```html
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  ```

## Architecture

### Data
All inventory data lives in the `skus` array (hardcoded mock data). Each SKU object has:
```js
{ id, name, cat, supplier, lead, stock, safety, rop, forecast, status, trend, dos }
```
- `status` is always one of: `"critical"`, `"low"`, `"healthy"`
- Modifying the `skus` array is all that's needed to change displayed data

### Page Routing
Pages are toggled via `.active` class on `.page` divs — no router library.
- Page container IDs follow the pattern: `page-{name}` (e.g. `page-dashboard`, `page-sku-explorer`)
- The `navigate(pageId)` function handles routing, title updates, and nav highlighting
- Page titles/subtitles are configured in the `pageTitles` object

### Config Objects
Status → style mappings are centralized as object literals near the top of the script:
```js
statusColor  // status → CSS color value (e.g. 'var(--red)')
statusClass  // status → badge CSS class (e.g. 'badge-red')
statusLabel  // status → display text (e.g. 'Critical')
hmClass      // status → heatmap cell CSS class
```

### Rendering
- `render*()` functions build HTML strings and assign to `innerHTML`
- Called once on page load; all content is pre-rendered into the DOM
- SKU detail content is re-generated on each `openSKU(id)` call

### Charts
- All charts use Chart.js v4.4.0
- Dashboard charts are created once in IIFEs and never destroyed
- The detail forecast chart is managed via `detailChartInstance` — always call `.destroy()` before recreating it
- Use `var(--accent)`, `var(--green)`, etc. for chart colors to stay consistent with the theme

## Conventions

### CSS
- **Always use CSS variables** for colors — never hardcode hex values
  - Available: `--bg`, `--surface`, `--surface2`, `--border`, `--accent`, `--accent2`, `--green`, `--yellow`, `--red`, `--text`, `--muted`
- Layout uses Flexbox (sidebar, nav, button rows) and CSS Grid (KPI cards, chart rows, detail panels)
- Hover transitions are `all .15s`

### JavaScript
- Dynamic HTML is built with **template literals**
- Function naming: `render*()` for DOM-building, `open*()` for navigation/actions
- Inline `onclick` attributes are used on dynamically generated table rows (e.g. `onclick="openSKU('${s.id}')"`)
- Variables: `s` for a single SKU in loops, `tbody`/`grid` for DOM containers

### IDs
- Page containers: `page-{name}`
- SKU detail fields: `detail-{field}` (e.g. `detail-name`, `detail-stock`, `detail-rop`)
- Chart canvases: `{name}Chart` (e.g. `dashForecastChart`, `detailForecastChart`)

## How to Extend

### Add a new SKU
Add an object to the `skus` array. All render functions read from this array.

### Add a new page
1. Add a `<div class="page" id="page-{name}">` section in the HTML
2. Add an entry to `pageTitles` for the title/subtitle
3. Add a `.nav-item` with `data-page="{name}"` in the sidebar

### Add a new chart
Use the IIFE pattern for isolation:
```js
(function() {
  const ctx = document.getElementById('myChart');
  new Chart(ctx, { /* config */ });
})();
```
For charts on the detail page, follow the destroy/recreate pattern used by `detailChartInstance`.

### Add a new status type
Update all four config objects: `statusColor`, `statusClass`, `statusLabel`, `hmClass`.

## Constraints

- **Keep it a single HTML file** — do not introduce a build system, bundler, or npm
- **Do not add CDN dependencies** without noting them in this file
- **Do not add localStorage persistence** unless explicitly requested
- **Dates are hardcoded** to Spring 2026 — update them when touching time-sensitive content
- The `skus` data is mock-only; there is no real backend or API integration

## Verification

To test changes, open `inventory-forecast.html` directly in a browser and:
1. Navigate all pages: Dashboard, SKU Explorer, Forecast Board, Alerts
2. Click a SKU row to open SKU Detail — verify charts and similar SKUs render
3. Toggle view modes (table / cards / heatmap) on SKU Explorer
4. Switch mode tabs (Summary / Forecast / Operations)
