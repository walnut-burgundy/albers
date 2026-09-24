# Authenticated Internet Archive recheck

`SOURCES.md` records two *Interaction of Color* editions whose public item pages are `printdisabled` / access restricted:

- `interactionofcol00albe` — 1971 selected-plates edition
- `interactionofcol0000albe` — 1975 revised-plate edition

The earlier check was unauthenticated. A local archive.org login can change what the account is allowed to read, so test the actual configured account rather than inferring access from the public item page.

```sh
python two-pixels-side-by-side/probe_ia_access.py \
  --config /path/to/ia.ini \
  > two-pixels-side-by-side/ia_authenticated_access.tsv
```

The probe reads authenticated metadata and requests only byte `0` from likely PDF/text/EPUB derivatives. It does not download a full scan. `readable` means the configured account could read that derivative at probe time; it does not establish permission to redistribute the plate or book in Git.

The byte-range check requires `ia download --range` (internetarchive 5.10.0 or newer). The `isomorphisms/internetarchive` fork contains that support.
