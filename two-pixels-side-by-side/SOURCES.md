# Interaction of Color source trail for the two-pixel experiment

The historical fixture to investigate first is **Plate IV-1** from Josef Albers's *Interaction of Color*: one physical color is shown in different surrounds so that it appears to change.

This file records sources and reproduction/access status. It deliberately does **not** vendor plate images whose reuse rights are not open.

## Plate IV-1

### Yale A&AePortal

- Plate page: https://aaeportal.com/images/51807/interaction-of-color-plate-iv-1
- Title: `Interaction of Color: plate IV-1`
- Creator description: `Student of Josef Albers`
- Date: 1963
- The A&AePortal record places the plate in Chapter IV, `A color has many faces—the relativity of color`.
- The electronic edition is marked `Copyright © 2013 by Yale University`.

The plate is publicly discoverable/viewable on the web, but that is not an open-content license. Do not treat the hosted image as a repository asset unless a separate reuse license is established.

### Metropolitan Museum of Art

- Object record: https://www.metmuseum.org/art/collection/search/737721
- Folder IV-1 is visible in the Met's copy of the 1963 portfolio.
- The Met record states `Rights and Reproduction: © 2026 Artists Rights Society (ARS), New York`.
- The site also states that the image cannot be enlarged, viewed full-screen, or downloaded.

This is strong evidence that the plate image should be used as a research reference rather than vendored into this repository.

### Josef & Anni Albers Foundation

- Background on the course and book: https://www.albersfoundation.org/alberses/teaching/interaction-of-color
- The Foundation describes *Interaction of Color* as the culmination of Albers's experimental color teaching and explains that many reproductions were based on student exercises.

## Internet Archive

Two relevant digitized editions were found.

### 1971 selected-plates edition

- Item: https://archive.org/details/interactionofcol00albe
- Identifier: `interactionofcol00albe`
- Title: *Interaction of color : text of the original edition with selected plates*
- Publication date: 1971
- Collection includes `printdisabled`.
- `Access-restricted-item: true`.
- The public item page currently reports `No suitable files to display here` under download options.

### 1975 revised-plate edition

- Item: https://archive.org/details/interactionofcol0000albe
- Identifier: `interactionofcol0000albe`
- Title: *Interaction of color : text of the original edition with revised plate section*
- Publication date: 1975
- Collection includes `printdisabled`.
- `Access-restricted-item: true`.
- The public item page currently reports `No suitable files to display here` under download options.

These are useful catalog/search references, but neither is an openly downloadable full scan from the unauthenticated item page.

## Our Internet Archive CLI fork

The repository `isomorphisms/internetarchive` is a fork of jjjjake's `internetarchive` package. It installs the command-line program `ia`.

Relevant commands documented by the fork include:

```text
ia search '<query>'
ia metadata <identifier>
ia download <identifier>
```

The fork's configuration documentation says IA-S3 access/secret keys are used for operations including search, upload, and metadata modification. **Access-restricted downloads use logged-in archive.org cookies**, not merely an S3 API key.

Therefore an API key alone is not the missing piece for these print-disabled books. If we later want to test authenticated access, the relevant question is whether an archive.org account is entitled to access/borrow the item and whether its logged-in cookies can be supplied to `ia`.

## Next computational step

Do not assign authoritative hexadecimal colors merely by eyeballing one web reproduction.

For the eventual RGB8 fixture, record all of the following separately:

1. the historical source (`Plate IV-1`);
2. the exact digital reproduction sampled (Met, Yale, a legally obtained scan, etc.);
3. the pixel coordinates/regions used for sampling;
4. the resulting RGB8 values;
5. any color-profile or conversion assumptions.

That makes the RGB values reproducible claims about a specified digital source rather than claims about the original physical paper/ink.