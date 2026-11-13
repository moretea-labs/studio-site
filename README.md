# Moretea Lab studio website

Public bilingual static product directory for https://moretea-lab.tech/.

## Source authority

- This repository owns only the common studio homepage and product directory.
- Avela keeps its existing independent website at https://avela.moretea-lab.tech/.
- TempoVela remains a separate published iOS application.
- TranslateDesk appears only as an upcoming product until its GitHub release is accepted.

## Product and design acceptance

Original first-party app screenshots are copied from the existing Avela and TempoVela repositories. The studio homepage is deliberately minimal: HTML, CSS, no framework, database, CMS, login, analytics or third-party trackers. Different products retain separate visual styles.

Run: python3 scripts/check_site.py

Before accepting production, verify at 320 / 390 / 768 / 1280 px, keyboard focus, reduced motion, actual App Store links, sitemap/canonical, and externally reachable HTTPS.

## Domain and deployment

Deploy to a dedicated Vercel project with a GitHub main integration. Cloudflare owns DNS for moretea-lab.tech; do not edit Avela or any other existing subdomain. Verify the production cert after DNS mapping. Build no new backend.

Forge Requirement: REQ-MORETEA-STUDIO-WEBSITE-20261113
Forge Plan: PLAN-MORETEA-STUDIO-WEBSITE-20261113
GitHub is the task progress authority.
