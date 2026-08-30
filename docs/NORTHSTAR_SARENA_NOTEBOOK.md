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

## Word processor pivot (2026-08-30) — real capability check first, not assumed

Founder real-time, same-session rapid burst: "build word processor into JEWEL i want to parlay
the infrastructure of SARENA notebook to power a gui word processor including spell check and
auto complete" → "power it via LO" → "dogfood the variables and shit you need" → "basically build
PARENA editor into SARENA" → "like start porting us to webgl my bro." All posted via `emily
observe` before acting (Principle 18). Real, honest reframing of each piece, checked directly
against what actually exists rather than assumed:

1. **"PARENA editor into SARENA"** — the real, concrete, buildable-today piece. `PARENA/stdlib/
   editor/*.prn` (`buffer.prn`, `widget.prn`, `render.prn`, `textmate*.prn`, `spotlight.prn`) is
   real, already-verified text-buffer/cursor/undo/syntax-highlighting logic — this doc's own
   "note rendering" and any future word-processor document model should be BUILT ON this existing
   editor stdlib, not a new buffer implementation invented inside SARENA_NOTEBOOK's own frontend
   JS. Real integration shape: JEWEL's kernel already shells out to `parena build` per cell — a
   word-processor "document" is the same real shape, with `buffer.prn`'s own real functions
   (`move-cursor-home`/`-end`, line navigation) becoming the actual editing engine behind
   SARENA_NOTEBOOK's NOTE cells, replacing a plain `<textarea>` with real PARENA-backed cursor/
   selection state. Not started — real, separate implementation work, sequenced first among these
   five asks since everything else in this section builds on having a real document/buffer model.
2. **"Power it via LO"** — checked directly against LO's own real, current state (`LO/GRAMMAR.md`,
   Phase 1 just landed same session): LO has no variables, no multi-argument functions, no
   records, and no real string manipulation yet. It categorically cannot power word-processor
   logic (spell-check, autocomplete, document state) today. Real, honest reading of "dogfood the
   variables and shit you need" (the founder's own very next message): rather than defer this to
   an abstract future Phase 2, treat the word processor's real needs as the forcing function for
   LO's next real language feature — but a genuinely new `let`/variable-binding construct is a
   real language-design decision (a new grammar production, `GRAMMAR.md` §2 amendment, new lexer/
   parser/emitter support), not something to bolt on inside this same pass without its own
   review. **Real, deliberate simplification found and worth naming now, before that design
   work starts**: LO's original source spec invented a De Bruijn/"Environment Matrix + Magnet"
   scheme for `let` specifically because LO's target (raw base4 ternaries) has no `let` of its
   own — but LO's REAL target as of Phase 1 is PARENA, which already has real, working `let`.
   There is no real reason for LO's own `let` to lower through an environment-matrix at all; it
   can — and should — emit a real PARENA `(let [x v] body)` directly, sidestepping the source
   spec's own named AST-duplication blowup risk entirely. This is a real, significant, positive
   finding for LO's own Phase 2 scoping, surfaced here rather than only in `NORTHSTAR.md` because
   this is the concrete task that surfaced it. **Not implemented in this pass** — named as the
   real next LO language-design step (a `GRAMMAR.md` amendment first, per this repo's own
   established "Spec Before Implementation" discipline), not rushed in under time pressure.
3. **Spell-check + autocomplete** — real, separate feature work, genuinely buildable on PARENA
   today (has real `String`/`Vec` support already) regardless of LO's own timeline: a real
   dictionary-lookup primitive (`Vec String` or a real trie) plus an edit-distance/prefix-match
   decision function, matching this stdlib's own established "small, verified, narrow v0"
   discipline. Not started — real, separate follow-up, sequenced after item 1 (needs a real
   buffer/cursor model to know what word is being typed).
4. **WebGL rendering** — a real, third rendering backend alongside this doc's own already-named
   "HTML first... SDL native second" sequencing (a founder-set order, not silently reordered) —
   read as a real, additional destination, not a replacement for either. Real, honest, unresolved
   question: does WebGL rendering sit alongside the HTML-first v0 (a progressive-enhancement
   canvas layer) or is it PAPERCRAFT/DUNG-style native-app rendering ported to the browser? Not
   started, not designed further here — a founder call once there's a real document model (item
   1) worth rendering.

**Real, honest sequencing this section commits to, not left ambiguous**: 1 (PARENA editor
integration) is the real, buildable-today foundation everything else depends on. 2 (LO `let`) is
a real, separate, next-scoped language change, not blocking 1 or 3. 3 (spell-check/autocomplete)
and 4 (WebGL) are each real, separate follow-ups layered on top of 1, not designed further in
this pass.

## Related

- `EMILY/BACKLOG.md` SECTION 201 — the full real founder-quote history this doc draws from.
- `JEWEL/CLAUDE.md` — the kernel this frontend is built against; the "Distinct from
  SARENA_NOTEBOOK" section is the real boundary line between the two.
- `gpt2-alpine-c/config/broker-routes.json` — the real, current routing/auth layer.
- `PARENA/stdlib/editor/*.prn` — the real, already-verified buffer/cursor/undo/syntax-
  highlighting logic the word-processor pivot (above) builds the real document model on.
- `LO/GRAMMAR.md`/`LO/NORTHSTAR.md` — LO's own real, current phased plan; the word-processor
  pivot's own item 2 above is a real, named input into LO's next real Phase 2 scoping pass, not
  a competing plan.
