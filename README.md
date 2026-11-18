# Moretea Lab studio website

Public bilingual static product directory for https://moretea-lab.tech/.

## Source authority

- This repository owns only the common studio homepage and product directory.
- Avela keeps its existing independent website at https://avela.moretea-lab.tech/.
- TempoVela remains a separate published iOS application.
- Unreleased or retired work is not presented as a public product or download.

## Product and design acceptance

The homepage is a product-first portfolio: Avela's calm light interface and TempoVela's dark music-practice interface are presented with first-party app screenshots and distinct visual stages. Product websites and apps keep their own design authority. The site remains static HTML/CSS, without a framework, database, CMS, login, analytics or third-party trackers.

Run: python3 scripts/check_site.py

Before accepting production, verify at 320 / 390 / 768 / 1280 px, keyboard focus, reduced motion, actual App Store links, sitemap/canonical, and externally reachable HTTPS.

## Domain and deployment

Deploy to a dedicated Vercel project with a GitHub main integration. Cloudflare owns DNS for moretea-lab.tech; do not edit Avela or any other existing subdomain. Verify the production cert after DNS mapping. Build no new backend.

Forge Requirement: REQ-MORETEA-STUDIO-WEBSITE-20261113
Forge Plan: PLAN-MORETEA-STUDIO-WEBSITE-20261113
GitHub is the task progress authority.
