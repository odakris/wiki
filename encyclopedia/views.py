from django.shortcuts import render



from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request, title):
    try:    
        html = util.markdown_to_html_converter(title)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "page": html
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    
