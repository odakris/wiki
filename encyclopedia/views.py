from django import forms
from django.shortcuts import render

from . import util

class NewSearchForm(forms.Form):
    query = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "search", "placeholder": "Search Encyclopedia", "autocomplete":"off"}))


def index(request):
    form = NewSearchForm()
    return render(request, "encyclopedia/index.html", {
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
    
    
