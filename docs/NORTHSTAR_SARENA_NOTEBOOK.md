# SARENA_NOTEBOOK — NORTHSTAR

Founder real-time (2026-08-24/25, `EMILY/BACKLOG.md` SECTION 201): "same functionality as jupyter
but its going to have a compiler you know?" → "look at the tyler episodes" / "they have all these
weird title cards" / "whatever parena native title card ui you want" → "there should be note
rendering built in" → "build our libplot shit into it" / "html first" / "SDL native second". Then,
this session (2026-08-28): "continue working on SARENA notebook" → "the notebook like jupyter but
for parena" → "docs are somewhere" → "in backlog maybe". This doc is that real scoping pass,
grounded in the actual backlog history (SECTION 201, S201-07) rather than re-deriving it from
scratch.

## What this is, and what it is NOT

**SARENA_NOTEBOOK is the custom notebook FRONTEND.** It is explicitly NOT the Jupyter kernel —
that's `JEWEL` (this same repo, `jewel_kernel.py`), real, shipped, already running
(`jewel-jupyter.service`, kernelspec `jewel` registered against the real Jupyter Server at
`127.0.0.1:8890`, real `/jewel/` broker route with Basic Auth). `JEWEL/CLAUDE.md`'s own "Distinct
from SARENA_NOTEBOOK" section already draws this line: JEWEL is "a real, working Jupyter *kernel*,
using standard Jupyter infrastructure," SARENA_NOTEBOOK is "a separate, bigger, not-yet-started
native GUI project." This doc is that project's own real v0 scoping, living inside JEWEL's own
repo because it's the frontend for JEWEL's own kernel — no new repo created (this monorepo's own
established pattern has the founder create a new empty repo first; no `SARENA` repo exists on
GitHub yet, confirmed via the API before writing this doc).

## Real, current state

- JEWEL's kernel is real and reachable: `GET /jewel/api` returns `{"version": "2.20.0"}`,
  `GET /jewel/api/kernelspecs` lists the real `jewel` kernelspec alongside the default `python3`
  one. Standard Jupyter Server REST + WebSocket API, nothing SARENA-specific needed on the kernel
  side to build a custom frontend against it.
- No frontend exists yet beyond stock JupyterLab (reachable at `/jewel/lab`) — genuinely a clean
  slate for the custom UI.
- Real TYLER visual grounding (grepped the actual episode scripts, not invented): recurring
  `TITLE CARD (white text, black field)` -- stark, minimal, black-background/white-text cards,
  almost always a terse declarative phrase (`DAY 79`, `DAY 131`) rather than a decorative treatment.
  SARENA_NOTEBOOK's own title-card styling draws directly from this: real black/white contrast,
  terse section headers between notebook cells, not a generic "make it look cool" invention.

## Real v0 scope (this session)

1. **A single, self-contained static frontend** (`notebook/index.html` in this repo) — real HTML/
   CSS/JS, no build step, no external CDN dependency (this is a real, deployed, internet-facing
   tool behind Basic Auth, not a sandboxed artifact — but "no external dependency" is still the
   right call here: one fewer thing that can silently break when a CDN has an outage).
2. **A real notebook document model**: an ordered list of cells, each either a real CODE cell
   (PARENA source, run against JEWEL's own kernel) or a real NOTE cell (markdown, rendered
   in-page) — the founder's own explicit "there should be note rendering built in" ask, not
   deferred to a later phase.
3. **Real kernel execution, not a mock**: `POST /jewel/api/kernels` (kernel_name: `jewel`) creates
   a real kernel session; a real WebSocket to `/jewel/api/kernels/{id}/channels` sends a real
   Jupyter-protocol `execute_request` per Run click and renders the real `stream`/`error`/
   `execute_result` messages that come back, matching `msg_id` to route replies to the right cell
   (cells can be run out of order / while a previous one is still running).
4. **Real TYLER-style title-card visual identity**: black field, white text, a terse declarative
   header treatment between/around cells — not generic Jupyter chrome re-skinned.
5. **Persistence**: v0 saves the notebook document to the browser's own `localStorage` — a real,
   honest, minimal choice (no server-side notebook storage exists yet; inventing one is real,
   separate, deferred scope, not silently assumed here).

## Explicitly deferred, not guessed at

- **SDL-native rendering** — founder's own explicit sequencing ("html first... SDL native
  second"). Not started.
- **`libplot` integration** (real plot/chart output from executed cells) — founder's own explicit
  "build our libplot shit into it" ask, real, but a genuinely separate, larger integration (a real
  rich-display `execute_result` MIME type, e.g. `image/svg+xml` or `image/png`, rendered inline) —
  not attempted in this v0 pass.
- **Server-side notebook persistence / a real save-to-disk `.sarena`/`.ipynb`-shaped file format**
  — v0 uses `localStorage` only, per the Persistence note above.
- **Cross-cell PARENA state** — inherited limitation from JEWEL itself (each cell compile+runs
  independently; PARENA has no REPL/incremental-compilation story yet).

## Deployment

Served as static files by a new, minimal systemd user service (`sarena-notebook.service`, same
real shape `jewel-jupyter.service` already establishes) on `127.0.0.1:8891`, reachable via a new
`/sarena/` route added to `gpt2-alpine-c/config/broker-routes.json` (the fatbaby-broker — per
`sudo-queue/31-jewel-nginx-basic-auth.sh`'s own header comment, "adding the NEXT broker-routed
service needs no sudo at all," the real, current, lowest-friction way to expose a new internal
service in this monorepo). Reuses JEWEL's own Basic Auth credentials for consistency (one set of
notebook credentials, not two) — the frontend's own client-side `fetch`/WebSocket calls to
`/jewel/api/...` rely on the browser's own per-origin Basic Auth credential caching once the user
has authenticated to `/jewel/` once in the same session.

## Related

- `EMILY/BACKLOG.md` SECTION 201 — the full real founder-quote history this doc draws from.
- `JEWEL/CLAUDE.md` — the kernel this frontend is built against; the "Distinct from
  SARENA_NOTEBOOK" section is the real boundary line between the two.
- `gpt2-alpine-c/config/broker-routes.json` — the real, current routing/auth layer.
