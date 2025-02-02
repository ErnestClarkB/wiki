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
        print("The requested page was not found.")
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "message": "The requested page was not found."
        })
    
    html = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html.strip()
    })

def search(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        entry = util.get_entry(query)
        if entry:  
            return redirect('entry', title=query)
        entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
    else:
        entries = []
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": entries
    })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title").lower().strip()
        content = request.POST.get("content").lower().strip()
        if not title or not content:
            return render(request, "encyclopedia/create.html", {
                "message": "Title and content are required.",
                "title": title,
                "content": content
            })
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html", {
                "message": "An entry with this title already exists.",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    content = util.get_entry(title).strip()

    if content is None:
        return render(request, "encyclopedia/index.html",{
            "entries" : util.list_entries(), 
            "message" : "The requested page was not found"
        })
    
    if request.method == "POST":
        new_content = request.POST.get("content").strip()
        util.save_entry(title, new_content.strip())
        return redirect('entry', title=title)
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content.strip()
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect('entry', title=title)