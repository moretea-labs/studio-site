#!/usr/bin/env python3
"""Static bilingual site acceptance, without dependencies or network."""
from pathlib import Path
from html.parser import HTMLParser
import json
import sys
import struct
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent


class SitePage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.ids = []
        self.sections = []
        self.h1 = 0
        self.titles = 0
        self.canonical = []
        self.languages = {}
        self.meta = {}
        self.schemas = []
        self.json_script = False
        self.json_buffer = ""

    def handle_starttag(self, tag, attrs):
        p = dict(attrs)
        if p.get("id"):
            self.ids.append(p["id"])
        if tag == "section":
            self.sections.append(p)
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.titles += 1
        if tag == "a":
            self.links.append(p)
        if tag == "img":
            self.images.append(p)
        if tag == "link":
            if p.get("rel") == "canonical":
                self.canonical.append(p.get("href"))
            if p.get("rel") == "alternate":
                self.languages[p.get("hreflang")] = p.get("href")
        if tag == "meta":
            self.meta[p.get("name") or p.get("property")] = p.get("content")
        if tag == "script" and p.get("type") == "application/ld+json":
            self.json_script = True
            self.json_buffer = ""

    def handle_data(self, data):
        if self.json_script:
            self.json_buffer += data

    def handle_endtag(self, tag):
        if tag == "script" and self.json_script:
            self.schemas.append(json.loads(self.json_buffer))
            self.json_script = False


def check(value, label):
    if not value:
        raise AssertionError(label)


def check_home(path, lang):
    html = (ROOT / path / "index.html").read_text(encoding="utf8")
    parsed = SitePage()
    parsed.feed(html)
    check('href="/styles.css?v=20261118-portfolio"' in html, "versioned shared stylesheet: " + path)
    url = "https://moretea-lab.tech/" + path
    check('lang="' + lang + '"' in html, "html lang: " + path)
    check(parsed.h1 == 1 and parsed.titles == 1, "headings: " + path)
    check(parsed.canonical == [url], "canonical: " + path)
    check({"zh-CN", "en", "x-default"} <= set(parsed.languages), "hreflang: " + path)
    check(len(parsed.meta.get("description", "")) >= 40, "description: " + path)
    check(parsed.meta.get("og:url") == url, "Open Graph canonical: " + path)
    social_image = "https://moretea-lab.tech/assets/og-products-zh.png" if lang == "zh-CN" else "https://moretea-lab.tech/assets/og-products-en.png"
    check(parsed.meta.get("og:image") == social_image, "localized product social image: " + path)
    check(parsed.meta.get("og:image:alt"), "social image alt: " + path)
    check(parsed.meta.get("og:image:width") == "1200" and parsed.meta.get("og:image:height") == "630", "social image dimensions metadata: " + path)
    check(parsed.meta.get("twitter:image") == social_image, "Twitter social image: " + path)
    check(len(parsed.schemas) == 2 and all(s.get("@context") == "https://schema.org" for s in parsed.schemas), "JSON-LD: " + path)
    organization = next((s for s in parsed.schemas if s.get("@type") == "Organization"), None)
    item_list = next((s for s in parsed.schemas if s.get("@type") == "ItemList"), None)
    check(organization and organization.get("url") == "https://moretea-lab.tech/", "Organization schema: " + path)
    check(item_list and len(item_list.get("itemListElement", [])) == 2, "released App Store product schema: " + path)
    check('class="product-stage product-avela"' in html, "Avela featured stage: " + path)
    check('class="product-stage product-tempo"' in html, "TempoVela featured stage: " + path)
    check('class="product-stage product-forge"' in html, "Forge open-source stage: " + path)
    check('id="forge" data-state="open-source"' in html, "Forge status: " + path)
    for project_id in ("leafspan", "veilspace", "translatedesk", "agentmail", "tinymoments", "shenbaobao"):
        check(f'id="{project_id}" data-state="in-development"' in html, "in-development portfolio project: " + project_id + " in " + path)
    check('id="avela" data-state="released"' in html and 'id="tempo" data-state="released"' in html, "released product statuses: " + path)
    check('class="work-grid"' in html, "additional products index: " + path)
    public_project_urls = {
        "https://github.com/moretea-labs/personal-knowledge-assistant/issues/37",
        "https://github.com/moretea-labs/FluentTranslate",
    }
    work_links = {a.get("href") for a in parsed.links if "work-link" in a.get("class", "").split()}
    check(work_links == public_project_urls, "only anonymously accessible development references are linked: " + path)
    for project_id in ("veilspace", "agentmail", "tinymoments", "shenbaobao"):
        card_start = html.index(f'id="{project_id}"')
        card_end = html.index("</article>", card_start)
        card = html[card_start:card_end]
        check('class="work-link"' not in card and 'class="work-art-corner"' not in card, "private project cards have no dead external action: " + project_id + " in " + path)
    tempo_store_url = "https://apps.apple.com/cn/app/id6831952477" if lang == "zh-CN" else "https://apps.apple.com/us/app/id6831952477"
    check(any(a.get("href") == tempo_store_url for a in parsed.links), "TempoVela regional App Store URL: " + path)
    check(any(i.get("url") == tempo_store_url for i in item_list.get("itemListElement", [])), "TempoVela canonical App Store URL: " + path)
    check(any("id6775778505" in a.get("href", "") for a in parsed.links), "Avela App Store: " + path)
    check(any("avela.moretea-lab.tech" in a.get("href", "") for a in parsed.links), "Avela site: " + path)
    check(any(a.get("href") == "/veilspace/privacy/" for a in parsed.links), "privacy link: " + path)
    check(any(a.get("href") == "/veilspace/support/" for a in parsed.links), "support link: " + path)
    required_images = {
        "/assets/avela-icon.jpg",
        "/assets/avela-reminder.webp",
        "/assets/avela-today.webp",
        "/assets/tempovela-icon.jpg",
        "/assets/tempovela-courses.jpg",
        "/assets/tempovela-metronome.jpg",
    }
    actual_images = {i.get("src") for i in parsed.images}
    check(required_images <= actual_images, "first-party product imagery: " + path)
    for i in parsed.images:
        check(i.get("alt") and i.get("width") and i.get("height"), "image alt/dimensions: " + path)
        check((ROOT / i.get("src", "").lstrip("/")).is_file(), "image file: " + str(i))
    check(any(i.get("src") == "/assets/avela-today.webp" and i.get("fetchpriority") == "high" and i.get("loading") == "eager" for i in parsed.images), "priority image loading: " + path)
    for image_path in ("/assets/tempovela-courses.jpg", "/assets/tempovela-metronome.jpg"):
        check(any(i.get("src") == image_path and i.get("loading") == "lazy" for i in parsed.images), "deferred TempoVela image loading: " + image_path + " in " + path)
    check('class="featured wrap" id="products"' in html, "featured product stages: " + path)
    check(len(parsed.ids) == len(set(parsed.ids)), "duplicate anchor id: " + path)
    check(any(a.get("href") == ("/en/" if lang == "zh-CN" else "/") for a in parsed.links), "language switch: " + path)
    for a in parsed.links:
        href = a.get("href", "")
        check(href.startswith(("/", "#", "https://", "mailto:")), "unsafe href: " + str(a))
        if href.startswith("#"):
            check(href[1:] in parsed.ids, "broken in-page navigation: " + href + " in " + path)
        if a.get("target") == "_blank":
            check("noopener" in a.get("rel", ""), "noopener: " + str(a))
    print("PASS", url, "nine-product portfolio, released/open-source/development states, bilingual SEO and first-party imagery")


def run():
    check_home("", "zh-CN")
    check_home("en/", "en")
    css = (ROOT / "styles.css").read_text(encoding="utf8")
    check("prefers-reduced-motion: reduce" in css, "reduced motion support")
    check(":focus-visible" in css, "visible keyboard focus")
    check("@media (max-width: 760px)" in css and "grid-template-columns: 1fr" in css, "single-column mobile product stages")
    check(".product-tempo" in css and ".product-avela" in css, "distinct product art direction")
    check(".eyebrow {" in css, "shared legal page eyebrow style")
    check(".product-stage" in css and ".work-grid" in css and ".product-link" in css, "featured stages, project directory and direct product links")
    def css_rule(selector):
        start = css.index(selector + " {")
        return css[start:css.index("}", start) + 1]

    for selector, label in (
        (".site-nav a", "header navigation"),
        (".product-link", "product actions"),
        (".footer-inner nav a", "footer navigation"),
        (".policy footer a, .support footer a", "legal-page footer navigation"),
    ):
        rule = css_rule(selector)
        check("min-width: 44px;" in rule and "min-height: 44px;" in rule, "44x44px " + label + " targets")
    for selector, label in ((".brand", "header brand"), (".footer-brand", "footer brand"), (".skip-link", "skip link")):
        check("min-height: 44px;" in css_rule(selector), "44px " + label + " target height")
    check("min-height: 34px !important" not in css, "language switch retains shared navigation target")
    check("@media (hover: hover)" in css, "hover-only product motion")

    page_specs = [
        ("veilspace/privacy/index.html", "https://moretea-lab.tech/veilspace/privacy/", "Veilspace Privacy Policy — Moretea Lab", "privacy"),
        ("veilspace/support/index.html", "https://moretea-lab.tech/veilspace/support/", "Veilspace Support — Moretea Lab", "support"),
    ]
    for source, url, title, kind in page_specs:
        html = (ROOT / source).read_text(encoding="utf8")
        check('href="/styles.css?v=20261118-portfolio"' in html, "versioned shared stylesheet: " + url)
        parsed = SitePage()
        parsed.feed(html)
        description = parsed.meta.get("description", "")
        check('lang="en"' in html, "html lang: " + source)
        check('class="site-header wrap"' in html and 'class="site-nav"' in html, "shared site header: " + source)
        check('class="brand-mark"' in html and 'class="brand-name"' in html, "shared brand styling: " + source)
        check(parsed.h1 == 1 and parsed.titles == 1, "headings: " + source)
        check(parsed.canonical == [url], "canonical: " + source)
        check(90 <= len(description) <= 160, "description length: " + source)
        check(parsed.meta.get("og:type") == "website", "Open Graph type: " + source)
        check(parsed.meta.get("og:title") == title, "Open Graph title: " + source)
        check(parsed.meta.get("og:description") == description, "Open Graph description: " + source)
        check(parsed.meta.get("og:url") == url, "Open Graph canonical: " + source)
        check(parsed.meta.get("og:image") == "https://moretea-lab.tech/assets/og-studio.png", "social image: " + source)
        check('lang="zh-CN"' in html, "Chinese language section: " + source)
        if kind == "privacy":
            check("Chrome Web Store Limited Use" in html, "privacy disclosure: " + source)
            check(any(a.get("href") == "/veilspace/support/" for a in parsed.links), "privacy support link")
            check('id="中文"' in html and 'class="language-title"' in html, "Chinese policy heading")
        else:
            check("中文支持" in html, "Chinese support content")
            check(any(a.get("href") == "/veilspace/privacy/" for a in parsed.links), "support privacy link")
            support_actions = [a for a in parsed.links if "github.com/moretea-labs/studio-site/issues/new" in a.get("href", "")]
            check(len(support_actions) == 2 and all("action" in a.get("class", "").split() for a in support_actions), "bilingual support CTAs")
            check("Do not include passwords, private URLs, personal health information" in html, "support privacy warning")
        for a in parsed.links:
            href = a.get("href", "")
            check(href.startswith(("/", "#", "https://", "mailto:")), "unsafe href: " + str(a))
            if href.startswith("#"):
                check(href[1:] in parsed.ids, "broken in-page navigation: " + href + " in " + source)
            if a.get("target") == "_blank":
                check("noopener" in a.get("rel", ""), "noopener: " + str(a))
        print("PASS", url, "SEO, bilingual content, links")

    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    check(sitemap.tag.endswith("urlset"), "sitemap root")
    check(all(node.tag.endswith("url") for node in sitemap), "sitemap URL entries")
    check(not (sitemap.text or "").strip() and all(not (node.tail or "").strip() for node in sitemap), "sitemap whitespace")
    sitemap_ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
    sitemap_urls = {node.text for node in sitemap.iter(sitemap_ns)}
    required_urls = {
        "https://moretea-lab.tech/",
        "https://moretea-lab.tech/en/",
        "https://moretea-lab.tech/veilspace/privacy/",
        "https://moretea-lab.tech/veilspace/support/",
    }
    check(required_urls <= sitemap_urls, "sitemap page coverage")
    robots = (ROOT / "robots.txt").read_text(encoding="utf8").splitlines()
    check("User-agent: *" in robots and "Allow: /" in robots and "Sitemap: https://moretea-lab.tech/sitemap.xml" in robots, "robots")
    check((ROOT / "favicon.svg").is_file() and (ROOT / "assets/og-studio.png").is_file(), "legal social assets")
    for lang in ("zh", "en"):
        social_path = ROOT / f"assets/og-products-{lang}.png"
        social_data = social_path.read_bytes()
        check(len(social_data) >= 24 and social_data[:8] == bytes.fromhex("89504e470d0a1a0a") and struct.unpack(">II", social_data[16:24]) == (1200, 630), "product social image dimensions: " + lang)
    vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf8"))
    expected_asset_cache = "public, max-age=86400, s-maxage=604800, stale-while-revalidate=86400"
    expected_css_cache = "public, max-age=0, must-revalidate"

    def has_cache_rule(source, expected_cache):
        return any(
            rule.get("source") == source and any(
                header.get("key", "").lower() == "cache-control" and header.get("value") == expected_cache
                for header in rule.get("headers", [])
            )
            for rule in vercel.get("headers", [])
        )

    for source in ["/assets/(.*)", "/favicon.svg"]:
        check(has_cache_rule(source, expected_asset_cache), "static asset cache policy: " + source)
    check(has_cache_rule("/styles.css", expected_css_cache), "stylesheet revalidation cache policy")
    print("PASS sitemap, robots, static asset cache headers, social image")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except (AssertionError, OSError, ET.ParseError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
