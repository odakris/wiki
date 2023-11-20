from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages

from . import util

full_list = util.list_entries()
full_list_lowercase = [item.lower() for item in full_list]

class NewSearchForm(forms.Form):
    query = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search Encyclopedia", "autocomplete":"off"}))

class NewCreateFrom(forms.Form):
    wiki_title = forms.CharField(label=False, widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Wiki Title", "autocomplete": "off"}))
    wiki_content = forms.CharField(label=False, initial=util.default_textarea, widget=forms.Textarea(attrs={"class":"form-control"}))


def index(request):
    search_form = NewSearchForm()
    return render(request, "encyclopedia/index.html", {
        "page_title": "All Pages",
        "search_form": search_form,
        "entries": util.list_entries()
    })


def get_page(request, title):
    search_form = NewSearchForm()
    try:    
        html = util.markdown_to_html_converter(title)
        return render(request, "encyclopedia/page.html", {
            "search_form": search_form,
            "title": title,
            "page": html
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "search_form": search_form,
            "title": title
        })
    

def query_search(request):
    # if request.method == "GET":
    search_form = NewSearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data["query"]
        sub_list = [ query_match for query_match in full_list if query.lower() in query_match.lower() ]

        if query.lower() in full_list_lowercase:
            # If query is found redirect to query page
            return redirect(f"/wiki/{query}")
        elif len(sub_list) == 0:
            # if there is no matching elements in sub_list return error page
            return get_page(request, query)
        else:
            # If query not found then render matching elements list
            search_form = NewSearchForm()
            return render(request, "encyclopedia/index.html", {
                "page_title": "All Matching Pages",
                "search_form": search_form,
                "entries": sub_list
            })
    else:
        return index(request)


def create(request):
    search_form = NewSearchForm()
    create_form = NewCreateFrom()

    if request.method == "POST":
        create_form=NewCreateFrom(request.POST)
        if create_form.is_valid():
            wiki_title = create_form.cleaned_data["wiki_title"]
            wiki_content= create_form.cleaned_data["wiki_content"]
            
            if wiki_title.lower() in full_list_lowercase:
                # If wiki already exist, prompt alert
                messages.error(request,"This Wiki already exist!")

            else:
                # If wiki does not exist yet, redirect to new wiki page
                util.save_entry(wiki_title, wiki_content)
                messages.success(request,"Your Wiki has been created!")
                return redirect(f"/wiki/{wiki_title}")        

    return render(request, "encyclopedia/create.html", {
        "title": "Create a new wiki",
        "search_form": search_form,
        "create_form": create_form
    })
    
            