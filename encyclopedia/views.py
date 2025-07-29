from django.shortcuts import render, redirect
from django import forms
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convertMdHTML(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def entry(request, title):
    html_content = convertMdHTML(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def search(request):
    query = request.GET.get("q")
    if query:
        entries = util.list_entries()

        # Case-insensitive exact match
        for entry in entries:
            if entry.lower() == query.lower():
                return redirect("entry", title=entry)

        # Partial matches
        matches = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "matches": matches
        })
    else:
        return redirect("index")
    
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea)

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": "An entry with this title already exists."
                })

            util.save_entry(title, content)
            html_content = convertMdHTML(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })

    else:
        form = NewPageForm()

    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })