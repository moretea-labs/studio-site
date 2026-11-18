# Moretea Lab

The official bilingual product showcase for https://moretea-lab.tech/.

## Product catalogue

The homepage is a visual product portfolio, not a studio manifesto or an individual app landing page. It presents the currently published Moretea Lab apps together in one catalogue:

- **Avela / Avela Meds** — medication companion, with its own independent product website and App Store destination.
- **TempoVela** — metronome and tuner for focused music practice, with its official App Store destination.

Each product keeps its own identity, palette, first-party icon and real app screenshots. The catalogue gives both products equal visual weight and direct paths to their official destinations. Unreleased or retired work is not presented as a public product or download.

## Source authority

- This repository owns the shared studio homepage and product directory.
- Avela keeps its existing independent website at https://avela.moretea-lab.tech/.
- TempoVela remains a separate published iOS application.
- Product sites and apps retain their own design and release authority.

## Design and engineering

- Bilingual static HTML/CSS at `/` and `/en/`.
- Two-column product catalogue on desktop; a readable single-column sequence on narrow screens.
- Real first-party product assets, semantic headings, descriptive alt text, keyboard focus and reduced-motion support.
- Canonical, reciprocal hreflang, sitemap, robots, Open Graph and JSON-LD.
- No framework, database, CMS, login, analytics or third-party trackers.

Run: `python3 scripts/check_site.py`

Before accepting production, verify at 320 / 390 / 768 / 1280 px, keyboard focus, reduced motion, product links, sitemap/canonical and externally reachable HTTPS.

## Domain and deployment

Deploy to the dedicated Vercel project with the GitHub `main` integration. Cloudflare owns DNS for moretea-lab.tech; do not edit Avela or any other existing subdomain. Build no new backend.

Forge Requirement: REQ-MORETEA-STUDIO-WEBSITE-20261113
Forge Plan: PLAN-MORETEA-STUDIO-WEBSITE-20261113
GitHub is the task progress authority.
