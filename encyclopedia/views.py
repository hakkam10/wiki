from django.shortcuts import render

import markdown2
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):
    markdowner = Markdown()
    return render(request, "encyclopedia/content.html", {
        "entry": markdowner.convert(util.get_entry(title))
    })
