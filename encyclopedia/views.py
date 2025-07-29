from django.shortcuts import render, redirect
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