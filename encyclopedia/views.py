from django import forms
from django.shortcuts import render

from . import util

class NewSearchForm(forms.Form):
    query = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "search", "placeholder": "Search Encyclopedia", "autocomplete":"off"}))


def index(request):
    form = NewSearchForm()
    return render(request, "encyclopedia/index.html", {
        "page_title": "All Pages",
        "form": form,
        "entries": util.list_entries()
    })


def get_page(request, title):
    form = NewSearchForm()
    try:    
        html = util.markdown_to_html_converter(title)
        return render(request, "encyclopedia/page.html", {
            "form": form,
            "title": title,
            "page": html
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "form": form,
            "title": title
        })
    

def query_search(request):
    # if request.method == "GET":
    form = NewSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data["query"]
        full_list = util.list_entries()
        sub_list = [ query_match for query_match in full_list if query.lower() in query_match.lower() ]

        if query.lower() in [item.lower() for item in full_list] or len(sub_list) == 0:
            # If query is found OR if there is no matching elements in sub_list
            return get_page(request, query)
        
        else:
            # If query not found then render matching elements list
            form = NewSearchForm()
            return render(request, "encyclopedia/index.html", {
                "page_title": "All Matching Pages",
                "form": form,
                "entries": sub_list
            })
    else:
        return index(request)


    
