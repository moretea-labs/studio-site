# Moretea Lab

The official bilingual portfolio for https://moretea-lab.tech/.

## Products and release authority

The homepage is a visual software portfolio, not a two-app landing page. The public catalogue distinguishes three real states:

- **Published on the App Store:** Avela / Avela Meds and TempoVela. Both retain first-party app icons, authentic screenshots and verified regional store links. Avela also retains its own product site.
- **Open-source:** Forge, with its GitHub repository and documentation as the public destinations.
- **In development (no download or release-date claims):** Leafspan, Veilspace, TranslateDesk, AgentMail, TinyMoments and 肾宝宝 / Shenbaobao. Their public project or development links are labelled accordingly. Being in the portfolio does not imply the work has been released.

The site owns its presentation, not any other product's release state, support, source or App Store listing. Do not automatically resurrect retired projects or claim a development project is publicly installable.

## Layout and design

- Editorial studio introduction followed by **three full-width product features**, each with its own visual identity. Avela and TempoVela use first-party screenshots; the Forge feature uses a typographic treatment, not a fabricated screenshot.
- An additional **six-project index** uses typography and distinct color surfaces with no invented product UI.
- Responsive single-column featured product flows; a three/two/one-column project index on desktop/tablet/phone.
- Bilingual static HTML/CSS, accessible navigation, 44px links, keyboard focus, alt text and reduced-motion support.
- Canonical, reciprocal hreflang, sitemap, robots, Open Graph and a JSON-LD **released-product-only** list. The two-item JSON-LD does not represent the full portfolio: it only covers verified public App Store products.
- No backend, CMS, tracking, third-party UI libraries, product status provider or duplicated release authority.

## Acceptance

Run `python3 scripts/check_site.py`. Verify the exact new source at 320 / 390 / 768 / 1280px, images and text, links, language switch, reduced motion, accessibility, production HTTPS, sitemap and canonical. Visual design acceptance is a separate user gate.

## Domain and deployment

Continue the existing Vercel `moretea-studio` project and Cloudflare DNS for `moretea-lab.tech`; do not alter the Avela subdomain, unrelated domains or private credentials.

Forge Requirement: `REQ-MORETEA-STUDIO-WEBSITE-20261113`
Forge Plan: `PLAN-MORETEA-STUDIO-WEBSITE-20261113`
Progress authority: https://github.com/moretea-labs/studio-site/issues/1
