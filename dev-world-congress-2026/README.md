# Dev World Congress 2026

A talk on type systems beyond the static/dynamic dichotomy: a ladder of
five claims a type can make, climbed from the familiar (Rust ownership,
the warmup) to the strange (dependent types). The full title is "Type
Systems You Might Not Know (But Will Love)". 30-minute slot.

See [the abstract](./abstract.md).

## Build

    make

Produces `talk.pdf` (23 slides). Requires `xelatex`, the Cyberwitchery
beamer theme (`beamerthemeCyberwitchery.sty` on the TEXINPUTS path), and
the JetBrains Mono / Hanken Grotesk fonts.

## Presenting

    make && open talk.pdf

There is exactly **one** live context switch: building a refinement
checker, at the refinement rung. It's flagged by a full-bleed cue slide
(a big "→ live") so it reads from the back of the room. Cmd+Tab between
the editor/terminal and the PDF for that segment.

## Livecode

- `livecode/refinement/` is **the live demo.** `live.py` is the on-stage
  template (scaffold pre-filled, two `...` stubs to fill: `subtype` and
  `infer`); `demo.py` is the finished reference; `script.md` is the
  five-beat build order. `python3.12 live.py`.
- `livecode/whirlwind/` is a bestiary of five standalone Python
  typecheckers (refinement, effects, rows, sessions, gradual) for further
  study, not shown live. See its own README.
