from django.http import HttpResponse
from django.utils.dateformat import format as date_format

from .sitemaps import all_entries


def sitemap_view(request):
    """Render the XML sitemap as well-indented XML.

    Built directly in Python (not via Django template) so the output is
    cleanly indented and human-readable in browsers' XML viewer. XML parsers
    don't care about whitespace, but it makes debugging trivial.
    """
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    for entry in all_entries():
        parts.append("  <url>")
        parts.append(f"    <loc>{entry['loc']}</loc>")

        lastmod = entry.get("lastmod")
        if lastmod is not None:
            # ISO 8601 with timezone, e.g. 2026-04-21T09:56:50+00:00
            parts.append(f"    <lastmod>{date_format(lastmod, 'c')}</lastmod>")

        if entry.get("changefreq"):
            parts.append(f"    <changefreq>{entry['changefreq']}</changefreq>")

        if entry.get("priority"):
            parts.append(f"    <priority>{entry['priority']}</priority>")

        for alt in entry.get("alternates") or []:
            parts.append(
                f'    <xhtml:link rel="alternate" '
                f'hreflang="{alt["hreflang"]}" href="{alt["href"]}"/>'
            )

        parts.append("  </url>")

    parts.append("</urlset>")
    parts.append("")  # trailing newline

    return HttpResponse("\n".join(parts), content_type="application/xml")
