# Archive

Empty by design. The original upload contained several files with browser
download–style numeric suffixes (e.g. `artifact_loader (3).py` through
`artifact_loader (6).py`, `hotspot_service (1).py` / `(2).py`, `config
(2).py`, `schemas (1).py`, `dependencies (1).py`, `requirements (1).txt`,
`env (1).example`).

Before restructuring, every suffixed file was compared against its
siblings with `md5sum` and `diff`. In every case the duplicates were
**byte-for-byte identical** — repeated downloads of the same file, not
divergent versions — so there was nothing to reconcile:

| Base name | Copies found | Result |
|---|---|---|
| `artifact_loader (3–6).py` | 4 identical copies | one copy used, exact duplicates discarded |
| `hotspot_service (1–2).py` | 2 identical copies | one copy used, exact duplicate discarded |
| `config (2).py`, `schemas (1).py`, `dependencies (1).py`, `requirements (1).txt`, `env (1).example` | single numbered copy each (no unnumbered sibling present) | used as-is |

No file's purpose was ambiguous and no two files implemented the same
thing differently, so nothing was moved here. This directory — and this
explanation of why it's empty — is kept so a future contributor doesn't
have to re-run that audit from scratch.
