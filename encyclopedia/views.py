from django.shortcuts import render
from markdown2 import Markdown


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request, title):
    markdowner = Markdown()
    
    try:    
        html = markdowner.convert(util.get_entry(title))
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "page": html
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

