#!/usr/bin/env python3
"""Check WCAG AA contrast for small text in the shared Moretea stylesheet."""
from pathlib import Path
import re
import sys

CSS = (Path(__file__).resolve().parent.parent / "styles.css").read_text(encoding="utf8")


def rule(selector):
    match = re.search(r"(?m)^\s*" + re.escape(selector) + r"\s*\{([^}]*)\}", CSS)
    if not match:
        raise AssertionError(f"missing CSS rule: {selector}")
    return match.group(1)


def declaration(selector, name):
    match = re.search(r"(?:^|;)\s*" + re.escape(name) + r"\s*:\s*(#[0-9a-fA-F]{6})", rule(selector))
    if not match:
        raise AssertionError(f"missing {name} in {selector}")
    return match.group(1)


def linear_channel(value):
    value = int(value, 16) / 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(color):
    channels = [linear_channel(color[index:index + 2]) for index in (1, 3, 5)]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(foreground, background):
    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def main():
    paper = declaration(":root", "--paper")
    checks = [
        ("legal eyebrow", declaration(".eyebrow", "color"), paper),
        ("brand mark", declaration(".brand-mark", "color"), paper),
        ("brand accent", declaration(".brand-dot, .footer-brand span", "color"), paper),
        ("brand descriptor", declaration(".brand-name small", "color"), paper),
        ("footer supporting copy", declaration(".footer-inner p, .footer-inner small", "color"), paper),
        ("section label", declaration(".section-label", "color"), paper),
        ("intro year", declaration(".intro-year", "color"), paper),
        ("section bar", declaration(".section-bar", "color"), paper),
        ("legal body text", declaration(":root", "--muted"), paper),
        ("intro description", declaration(".intro-body > p", "color"), paper),
        ("footer links", declaration(".footer-inner nav a", "color"), paper),
        ("Avela supporting copy", declaration(".product-avela", "--stage-muted"), declaration(".product-avela", "background")),
        ("TempoVela supporting copy", declaration(".product-tempo", "--stage-muted"), declaration(".product-tempo", "background")),
        ("Forge supporting copy", declaration(".product-forge", "--stage-muted"), declaration(".product-forge", "background")),
        ("work heading description", declaration(".work-heading > p", "color"), paper),
        ("work metadata", declaration(".work-meta", "color"), paper),
        ("work status", declaration(".work-meta span:last-child", "color"), paper),
        ("work descriptions", declaration(".work-card p", "color"), paper),
        ("portfolio note", declaration(".portfolio-note", "color"), paper),
    ]
    failures = []
    for label, foreground, background in checks:
        ratio = contrast(foreground, background)
        print(f"{'PASS' if ratio >= 4.5 else 'FAIL'} {label}: {ratio:.2f}:1")
        if ratio < 4.5:
            failures.append(label)
    if failures:
        raise AssertionError("WCAG AA contrast below 4.5:1: " + ", ".join(failures))
    print(f"PASS {len(checks)} small-text contrast pairs meet WCAG AA (4.5:1)")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError) as error:
        print("FAIL:", error, file=sys.stderr)
        sys.exit(1)
