#!/usr/bin/env python3
"""Static bilingual site acceptance, without dependencies or network."""
from pathlib import Path
from html.parser import HTMLParser
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent

class SitePage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]; self.images=[]; self.ids=[]; self.h1=0; self.titles=0
        self.canonical=[]; self.languages={}; self.meta={}; self.schemas=[]
        self.json_script=False; self.json_buffer=""

    def handle_starttag(self, tag, attrs):
        p=dict(attrs)
        if p.get("id"): self.ids.append(p["id"])
        if tag=="h1": self.h1+=1
        if tag=="title": self.titles+=1
        if tag=="a": self.links.append(p)
        if tag=="img": self.images.append(p)
        if tag=="link":
            if p.get("rel")=="canonical": self.canonical.append(p.get("href"))
            if p.get("rel")=="alternate": self.languages[p.get("hreflang")]=p.get("href")
        if tag=="meta": self.meta[p.get("name") or p.get("property")]=p.get("content")
        if tag=="script" and p.get("type")=="application/ld+json":
            self.json_script=True; self.json_buffer=""

    def handle_data(self, data):
        if self.json_script: self.json_buffer+=data

    def handle_endtag(self, tag):
        if tag=="script" and self.json_script:
            self.schemas.append(json.loads(self.json_buffer))
            self.json_script=False

def check(value, label):
    if not value: raise AssertionError(label)

def run():
    for path, lang in [("", "zh-CN"),("en/", "en")]:
        html=(ROOT/path/"index.html").read_text(encoding="utf8")
        parsed=SitePage();parsed.feed(html)
        url="https://moretea-lab.tech/"+path
        check('lang="'+lang+'"' in html, "html lang: "+path)
        check(parsed.h1==1 and parsed.titles==1, "headings: "+path)
        check(parsed.canonical==[url], "canonical: "+path)
        check({"zh-CN","en","x-default"} <= set(parsed.languages), "hreflang: "+path)
        check(len(parsed.meta.get("description",""))>55, "description: "+path)
        check(parsed.meta.get("og:url")==url, "Open Graph canonical: "+path)
        check(parsed.meta.get("og:image")=="https://moretea-lab.tech/assets/og-studio.png", "social image: "+path)
        check(len(parsed.schemas)==2 and all(s.get("@context")=="https://schema.org" for s in parsed.schemas), "JSON-LD: "+path)
        check(any("id6831952477" in a.get("href","") for a in parsed.links),"TempoVela App Store: "+path)
        check(any("id6775778505" in a.get("href","") for a in parsed.links),"Avela App Store: "+path)
        check(any("avela.moretea-lab.tech" in a.get("href","") for a in parsed.links),"Avela site: "+path)
        check("TranslateDesk" in html and "COMING SOON" in html,"unreleased product: "+path)
        check(any(a.get("href")=="https://github.com/moretea-labs/FluentTranslate" for a in parsed.links), "TranslateDesk source link: "+path)
        check("Public download not yet available" in html if lang=="en" else "安装包尚未公开发布" in html,"unreleased download disclosure: "+path)
        for i in parsed.images:
            check(i.get("alt") and i.get("width") and i.get("height"),"image alt/dimensions: "+path)
            check((ROOT/i.get("src","").lstrip("/")).is_file(),"image file: "+str(i))
        check(len(parsed.ids)==len(set(parsed.ids)), "duplicate anchor id: "+path)
        check(any(a.get("href")==("/en/" if lang=="zh-CN" else "/") for a in parsed.links), "language switch: "+path)
        for a in parsed.links:
            href=a.get("href","")
            check(href.startswith(("/","#","https://","mailto:")),"unsafe href: "+str(a))
            if href.startswith("#"):
                check(href[1:] in parsed.ids, "broken in-page navigation: "+href+" in "+path)
            if a.get("target")=="_blank":
                check("noopener" in a.get("rel",""),"noopener: "+str(a))
        print("PASS",url,"SEO, links, accessibility, images")
    ET.parse(ROOT/"sitemap.xml")
    check((ROOT/"robots.txt").read_text().strip().endswith("sitemap.xml"),"robots")
    check((ROOT/"favicon.svg").is_file() and (ROOT/"assets/og-studio.png").is_file(),"social assets")
    print("PASS sitemap, robots, social image")
    return 0
if __name__=="__main__":
    try: sys.exit(run())
    except (AssertionError, OSError, ET.ParseError) as exc:
        print("FAIL:",exc,file=sys.stderr);sys.exit(1)
