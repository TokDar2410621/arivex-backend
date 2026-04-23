from django.shortcuts import render

from .sitemaps import all_entries


def sitemap_view(request):
    """Render the XML sitemap.

    Served at ``/sitemap.xml``; content-type is set by the template's
    rendering pipeline via the ``content_type`` arg.
    """
    return render(
        request,
        "sitemap.xml",
        {"entries": all_entries()},
        content_type="application/xml",
    )
