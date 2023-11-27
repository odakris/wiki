from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
import random

from . import util

class NewSearchForm(forms.Form):
    query = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search Encyclopedia", "autocomplete":"off"}))

class NewWikiForm(forms.Form):
    wiki_title = forms.CharField(label=False, widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Wiki Title", "autocomplete": "off"}))
    wiki_content = forms.CharField(label=False, initial=util.default_textarea, widget=forms.Textarea(attrs={"class":"form-control"}))

def homepage(request):
    search_form = NewSearchForm()
    return render(request, "encyclopedia/homepage.html", {
        "homepage_title": "Encyclopedia - HomePage",
        "search_form": search_form
    })
    

def index(request):
    search_form = NewSearchForm()
    return render(request, "encyclopedia/index.html", {
        "title": "All Wiki Pages",
        "search_form": search_form,
        "entries": util.list_entries()
    })


def get_wiki(request, title):
    search_form = NewSearchForm()
    try:    
        html = util.markdown_to_html_converter(title)
        return render(request, "encyclopedia/wiki.html", {
            "search_form": search_form,
            "wiki_title": title,
            "wiki_content": html
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "search_form": search_form,
            "wiki_title": title
        })
    

def wiki_search(request):
    # if request.method == "GET":
    search_form = NewSearchForm(request.GET)

    full_list = util.list_entries()
    full_list_lowercase = [item.lower() for item in full_list]

    if search_form.is_valid():
        query = search_form.cleaned_data["query"]
        sub_list = [ query_match for query_match in full_list if query.lower() in query_match.lower() ]

        if query.lower() in full_list_lowercase:
            # If query is found redirect to query wiki page
            return redirect(f"/wiki/{query}")
        elif len(sub_list) == 0:
            # if there is no matching elements in sub_list return error page
            return get_wiki(request, query)
        else:
            # If query not found then render matching elements list
            search_form = NewSearchForm()
            return render(request, "encyclopedia/index.html", {
                "title": "All Matching Wiki Pages",
                "search_form": search_form,
                "entries": sub_list
            })
    else:
        return index(request)


def add_wiki(request):
    search_form = NewSearchForm()
    add_form = NewWikiForm()

    full_list = util.list_entries()
    full_list_lowercase = [item.lower() for item in full_list]

    if request.method == "POST":
        add_form=NewWikiForm(request.POST)
        if add_form.is_valid():
            wiki_title = add_form.cleaned_data["wiki_title"]
            wiki_content= add_form.cleaned_data["wiki_content"]
            
            if wiki_title.lower() in full_list_lowercase:
                # If wiki already exist, prompt alert
                messages.error(request,"Sorry, this Wiki already exist!")

            else:
                # If wiki does not exist yet, redirect to new wiki page
                util.save_entry(wiki_title, wiki_content)
                messages.success(request, f"Your {wiki_title} Wiki page has been created!")
                return redirect(f"/wiki/{wiki_title}")        

    return render(request, "encyclopedia/add.html", {
        "title": "Add New Wiki",
        "search_form": search_form,
        "add_form": add_form
    })

def edit_wiki(request, title):
    search_form=NewSearchForm()
    edit_form=NewWikiForm(initial={"wiki_content": util.get_entry(title), "wiki_title": title})

    full_list = util.list_entries()
    full_list_lowercase = [item.lower() for item in full_list]

    if request.method == "POST":
        edit_form=NewWikiForm(request.POST)
        if edit_form.is_valid():
            edited_wiki_title = edit_form.cleaned_data["wiki_title"]
            edited_wiki_content = edit_form.cleaned_data["wiki_content"]
            util.save_entry(edited_wiki_title, edited_wiki_content)

            if edited_wiki_title.lower() in full_list_lowercase:
                messages.success(request, f"{edited_wiki_title} page has been updated!")            
            else: 
                messages.success(request, f"{edited_wiki_title} page has been created!")

        return redirect(f"/wiki/{edited_wiki_title}")  
    
    return render(request, "encyclopedia/edit.html", {
        "wiki_title": f"Edit Wiki {title}",
        "search_form": search_form,
        "edit_form": edit_form
    })

def delete_wiki(request, title):
    util.delete_entry(title)
    messages.error(request, f"{title} page has been deleted!")
    return redirect(f"/wiki")


def random_wiki(request):
    random_page =  random.choice(util.list_entries())
    return redirect(f"/wiki/{random_page}")
    
            