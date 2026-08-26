# JEWEL

## What This Is

A real Jupyter kernel for PARENA (`/home/fatbaby/PARENA`) — write PARENA source in a notebook
cell, run it, see the real compiled program's own output. Born from IDUNA's developer portal
(`internal/http/handlers/portal.go`), which has long listed a "Jupyter — PARENA Jupyter kernel"
tool row as `status-pending`/"Install pending"; this repo is the real thing behind that link.

Founder real-time: "work on our parena JUPYTER backend just use basic auth to protect it for
now until we get google oauthg to work" → "call it JEWEL" → "upstream github JEWEL created in
case its useful" → "put the parena backend for jupyter there". Naming note: "JEWEL" was
previously a discarded candidate name for the unrelated SAND (PARENA-native code editor)
project — see `EMILY/BACKLOG.md` S189-38 for that history. The founder redirected the name
here instead; SAND stays SAND, unaffected.

**Distinct from SARENA_NOTEBOOK** (the portal's *other* tool row, "Native PARENA notebook GUI —
title cards, built-in note rendering, libplot") — that's a separate, bigger, not-yet-started
native GUI project. JEWEL is narrower: a real, working Jupyter *kernel*, using standard Jupyter
infrastructure (JupyterLab/Notebook), not a custom notebook frontend.

## How It Works

`jewel_kernel.py` implements a real `ipykernel.kernelbase.Kernel` subclass. `do_execute` writes
the cell's own source to a temp `.prn` file, runs the real `parena build` compiler
(`/home/fatbaby/PARENA/parena`), links the emitted C against `parena_runtime.c`, runs the
resulting binary, and streams its real stdout/stderr back as the cell's own output. A real
compile error surfaces as a real Jupyter error, not swallowed — same "honest, not faked"
verification discipline every other real integration in this monorepo holds itself to.

This is the same general shape a number of real, existing niche-language Jupyter kernels use
(shell out to the language's own real compiler/interpreter per cell) — not a novel pattern
invented here, the honest right-sized approach for a from-scratch compiled language with no
REPL of its own yet.

## Status

Real, working v0: a real PARENA cell compiles, links, and runs, with real stdout/stderr/error
output. Not yet done, scoped honestly:
- No persistent state across cells (each cell is a fresh, independent compile+run — PARENA has
  no REPL/incremental-compilation story yet for genuine cross-cell variable persistence).
- No rich display (plots, images) — plain text output only.
- HTTP Basic Auth in front of the Jupyter server itself (founder: "just use basic auth to
  protect it for now until we get google oauthg to work") — a real, deliberate stopgap, not the
  final story; IDUNA's own Google OAuth devportal gate is the intended long-term auth, blocked
  on a genuine human-only GCP Console step (see `EMILY/BACKLOG.md`'s own OAuth Client ID entry).

## Running It

```bash
# One-time: install the kernel into the shared jupyter venv's kernelspec directory
/home/fatbaby/.venvs/jupyter/bin/python install_kernel.py

# Start JupyterLab (bound to localhost only -- nginx is the real internet-facing edge,
# see /home/fatbaby/sudo-queue's own JEWEL basic-auth entry)
/home/fatbaby/.venvs/jupyter/bin/jupyter lab --ip=127.0.0.1 --port=8890 --no-browser
```

## Related Repos

- `PARENA` — the compiler this kernel drives (`parena build`, `runtime/parena_runtime.c`).
- `IDUNA` — the developer portal (`/portal`) that links here; also the long-term Google-OAuth
  auth story once the GCP Console setup is done by a human.
- `EMILY` — RSI loop / backlog coordination for cross-repo work.

## Founder Real-Time Direction

Whenever the founder gives real-time direction — a new ask, a correction, a "can we also..." —
route it through `emily observe -s info "Founder real-time: <summary>"` first, even if it isn't
this repo's usual domain, then sprint-plan it into `EMILY/BACKLOG.md` (`emily backlog curate`,
scoped into a real SECTION/sub-item, not just a one-line log), and only then implement. See
`EMILY/docs/THE_EMILY_WAY.md` Principle 18 ("Pave the Cow Paths").

## Frame-Break Reframing

Founder-sourced prompting technique (REDGARDEN/NORTHSTAR.md §28, full origin in
REDGARDEN/docs2/MULTI_AGENT_RD_RESEARCH_NOTES.md §5): given a request, name the underlying
structural/systemic pattern it's one instance of — one level of abstraction up — as an added
lens during planning/triage/judgment calls. Use it to spot the general case behind a specific
ask. It augments judgment, it does not replace doing the work: direct, concrete execution of
the literal task asked for still happens every time.

## Commit Protocol (standing instruction)

Always commit and push completed work immediately — don't wait to be asked. This is the default for every repo in this monorepo.

Every commit — human-written or produced by automated code paths (git-commit helpers in emily-agent, emily.cli, IDUNA handlers, etc.) — must carry the active `emily session` fingerprint as a `session: <tag>` trailer (blank line, then the trailer). This was silently missing from several independently-implemented automated commit helpers across the monorepo until an audit on 2026-08-10 (founder, real-time: "where in the fuck is my llm session id anywhere"). If you add a new automated git-commit code path anywhere, wire in the session tag the same way — don't assume an existing helper already does it.
