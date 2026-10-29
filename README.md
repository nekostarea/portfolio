# Nannan Fu — UX portfolio

A four-page, static portfolio combining handwritten typography, paper-inspired layouts, and readable project summaries. It uses local fonts and needs no Node packages or external services.

## Develop

Use the existing checkout; cloud tasks are already isolated, so no Git worktree is needed.

```bash
cd /workspace/portfolio
python3 scripts/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory _site
```

Python 3.10+ is sufficient. Rebuild after editing. `_site/` is generated and ignored. The build preserves the original project folders and copies their JPGs in numeric page order, alongside the local assets.

- `scripts/projects.json`: project descriptions, categories, labels, and metadata.
- `scripts/build.py`: page templates and build logic.
- `scripts/hero.html`: the powder-blue homepage opening and photography card.
- `assets/style.css`: base typography, responsive layouts, and reduced-motion styles.
- `assets/refinement.css`: powder-blue palette, flowing display type, and decorative refinements.
- `assets/textile.css`: Mazzy display headings, translucent layering, original floral embroidery, lace edging, and dashed stitching.
- `assets/materials.css`: physical lace, canvas texture, Courier labels, and Apple Garamond reading text and captions.
- `assets/pastels.css`: blush, lavender, cream, and powder blue; the four-family font system and garden gate motif.
- `assets/handdrawn.css`: uneven pencil borders, gentle card rotations, and sketched separators.
- `assets/materials/`: locally hosted, AI-generated ivory cotton lace (with transparency) and canvas texture. Generated originals are retained separately in the workspace.
- `assets/site.js`: native-dialog gallery viewer with keyboard navigation.
- `assets/fonts/`: self-hosted Caveat and DM Sans (Fontsource 5.2.8), Pinyon Script (Fontsource 5.3.0), with their OFL licenses, and a DejaVu Sans symbol subset with its license.
- The active site uses only four font families: Mazzy, Apple Garamond (Light / Bold Italic), P22 Folk Art Cross, and Courier (self-hosted Courier Prime, Fontsource 5.3.0, OFL). Earlier font assets are retained but no longer registered or used. Arrow icons are SVGs rather than characters from a fifth font.
- `assets/fonts/mazzy-regular.ttf`: the Mazzy TM Regular font supplied by the user for this design.
- `assets/fonts/apple-garamond-*.ttf`: the Apple Garamond Light and Bold Italic fonts supplied by the user.
- `assets/Nannan-Fu-Resume.pdf`: downloadable résumé supplied for the portfolio.

## Validate

Build, start the loopback server, and request all four pages: `index.html`, `psychology.html`, `usability.html`, and `human-ai.html`. Check project links, original images, résumé, mobile layout, keyboard focus, gallery disclosure, and the viewer’s Escape/arrow keys and focus return. The underlying original-image links and native disclosure elements also work without JavaScript.

The JPG documents are image-based source material. Every project has a readable HTML overview, but the complete documents do not yet have accessible text transcripts. Original decks may depict multimedia controls; these exports are static images and do not play embedded audio/video. Graphic design descriptions are intentionally brief pending additional project context.

## Publish on GitHub Pages

The included workflow builds the site and deploys it using GitHub Pages. Nothing is published until these changes are pushed and Pages is enabled. In the repository’s **Settings → Pages**, select **GitHub Actions** as the build source, then run the **Deploy portfolio** workflow or push to `main`. The workflow uses relative URLs, so deployment under `/portfolio/` is supported.

Do not commit `_site`, authentication values, or browser-test artifacts. All public résumé details should be reviewed before publication.
