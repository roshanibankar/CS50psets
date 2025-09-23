from django.shortcuts import render, redirect 
import markdown2
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Entry '{title}' not found."
        })
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })


def search(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return render(request, "encyclopedia/search.html", {
            "results": [],
            "query": query
        })
    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]
    for entry in entries:
        if entry.lower() == query.lower():
            return redirect(f"/wiki/{entry}")
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content")

        if not title or not content:
            return render(request, "encyclopedia/error.html", {
                "message": "Title and content must not be empty."
            })

        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": f"An entry with the title '{title}' already exists."
            })

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry", title=title)
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })


def random_page(request):
    entries = util.list_entries()
    if entries:
        title = random.choice(entries)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/error.html", {
        "message": "No entries available."
    })

