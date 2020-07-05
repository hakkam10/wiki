from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import markdown2
from markdown2 import Markdown

from . import util

class EditEntry(forms.Form):
    content = forms.CharField(label="content", widget=forms.Textarea)

class NewEntry(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'form-control'})) 
    content = forms.CharField(label="content", widget=forms.Textarea)
   
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def content(request, title):
    markdowner = Markdown()
    try:
        return render(request, "encyclopedia/content.html", {
        "entry": markdowner.convert(util.get_entry(title)),
        "title": str(title),
        "entries": util.list_entries(),
        "edit": "Edit this page"
    })
    except TypeError:
        return render(request, "encyclopedia/content.html", {
        "entry": "Page does not exist",
        "title": "Error",
        "entries": util.list_entries()
    })

def edit(request, title):
    if request.method == "POST":
        entry = EditEntry(request.POST)
        if entry.is_valid():
            content = entry.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:content", args=(title,)))
        else:
            return render(request, "encyclopedia/edit.html", {
            "message":"Error",
            "title":title,
            "form":entry,
            "entries": util.list_entries()
            })
    else:
        return render(request, "encyclopedia/edit.html", {
        "title":title,
        "content":util.get_entry(title),
        "form":EditEntry(initial={"title":title, "content":util.get_entry(title)}),
        "entries": util.list_entries()
        })
    
def new(request):
    filenames = util.list_entries()
    if request.method == "POST":
        entry = NewEntry(request.POST)
        if entry.is_valid():
            title = entry.cleaned_data['title']
            content = entry.cleaned_data['content']
            if title.casefold() not in [filename.casefold() for filename in filenames]:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:content", args=(title,)))
            else:
                return render(request, "encyclopedia/new.html", {
                "form":entry,
                "entries": util.list_entries(),
                "message": "Title already exists!"
        })
        else:
            return render(request, "encyclopedia/new.html", {
            "form":entry,
            "entries": util.list_entries()
        })
    else:
        return render(request, "encyclopedia/new.html", {
            "form":NewEntry(),
            "entries": util.list_entries()
        })

def result(request):
    entries = util.list_entries()
    query = str(request.GET.get('q', None))
    results = [entry for entry in entries if query.casefold() in entry.casefold()]
    context = {
                "results":results,
                "query":query,
                "len":len(results),
                "entries": util.list_entries()
            }
    if len(results) == 1:
        if results[0].casefold() == query.casefold():
            return HttpResponseRedirect(reverse("encyclopedia:content", args=(query,)))
        else:
            return render(request, "encyclopedia/result.html", context)
    elif len(results) > 1:
        return render(request, "encyclopedia/result.html", context)
    else:
        return render(request, "encyclopedia/result.html", context)
